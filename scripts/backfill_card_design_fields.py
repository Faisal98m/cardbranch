"""
Backfill card_colour, card_border, card_font for every Client row.

Dry-run by default.  Pass --apply to write.

Usage:
    python scripts/backfill_card_design_fields.py          # read-only plan
    python scripts/backfill_card_design_fields.py --apply   # write (dev DB only)
"""

import os
import sys
import copy

# Bootstrap Flask app context before importing models/registries
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_CONFIG'] = 'Debug'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.services.themes import LEGACY_STYLE_MAP, _LEGACY_FALLBACK
import sqlalchemy as sa

# ── helpers ──────────────────────────────────────────────────────────────
_REDACT = object()


def redact_uri(uri):
    """Return a human-readable URI with credentials masked."""
    if uri is None:
        return '(none)'
    s = str(uri)
    # sqlite:///… is safe to show as-is
    if s.startswith('sqlite'):
        return s
    # postgresql://user:pass@host/db → postgresql://…@host/db
    if '@' in s:
        before, after = s.split('@', 1)
        return before.split(':')[0] + '://…@' + after
    return s


def resolve_from_legacy(card_style):
    """Return (colour_key, border_key, font_key) for a legacy card_style.

    This is stricter than resolve_design() — it does NOT apply the
    _LEGACY_FALLBACK for unrecognised values.  The caller handles
    fallback cases separately.
    """
    if card_style in LEGACY_STYLE_MAP:
        return LEGACY_STYLE_MAP[card_style]
    return None  # unrecognised


_KNOWN_FALLBACK_LEGACY = {None, '', 'default'}
_FALLBACK_RESOLVED = _LEGACY_FALLBACK  # ('oxblood', 'none', 'playfair')

# ── main ─────────────────────────────────────────────────────────────────
def main():
    apply_flag = '--apply' in sys.argv

    app = create_app('Debug')
    with app.app_context():
        engine = db.engine
        uri = engine.url

        print(f'Database URI (redacted): {redact_uri(uri)}')
        print(f'Mode: {"** APPLY **" if apply_flag else "dry-run (read-only)"}')
        print()

        # ---- guard: refuse --apply on non-SQLite ----
        if apply_flag:
            scheme = uri.drivername if hasattr(uri, 'drivername') else str(uri).split('://')[0]
            if 'sqlite' not in scheme.lower():
                print('ERROR: --apply is only allowed against a local SQLite database.')
                print(f'  Detected scheme: {scheme}')
                sys.exit(1)
            db_path = str(uri.database) if hasattr(uri, 'database') else ''
            if 'instance' not in db_path.replace('\\', '/').lower():
                print('WARNING: this does not appear to be the local instance/ database.')
                print(f'  Database path: {db_path}')
                resp = input('  Type YES to continue: ')
                if resp.strip() != 'YES':
                    print('Aborted.')
                    sys.exit(1)

        # ---- Step 1: build the plan ----
        rows = db.session.execute(
            sa.text(
                'SELECT id, card_style, card_colour, card_border, card_font, updated_at '
                'FROM clients ORDER BY id'
            )
        ).all()

        total = len(rows)
        planned_updates = []
        stop_rows = []
        backfill_count = 0
        already_count = 0

        for row in rows:
            style = row.card_style
            plan = {
                'id': row.id,
                'original_card_style': style,
                'colour': None,
                'border': None,
                'font': None,
                'classification': None,
                'updated_at_before': row.updated_at,
            }

            # ── classify card_style ──
            resolved = resolve_from_legacy(style)
            if resolved is not None:
                colour_key, border_key, font_key = resolved
            elif style in _KNOWN_FALLBACK_LEGACY:
                colour_key, border_key, font_key = _FALLBACK_RESOLVED
            else:
                # unrecognised string — STOP
                plan['classification'] = 'stop'
                plan['_stop_reason'] = (
                    f'Unrecognised card_style {repr(style)} '
                    f'— not in LEGACY_STYLE_MAP and not a known fallback value.'
                )
                stop_rows.append(plan)
                planned_updates.append(plan)
                continue

            plan['colour'] = colour_key
            plan['border'] = border_key
            plan['font'] = font_key

            # ── inspect destination fields ──
            db_colour = row.card_colour
            db_border = row.card_border
            db_font = row.card_font

            if db_colour is None and db_border is None and db_font is None:
                plan['classification'] = 'backfill'
                backfill_count += 1

            elif db_colour is not None and db_border is not None and db_font is not None:
                # already populated — verify consistency
                if (db_colour == colour_key and db_border == border_key and db_font == font_key):
                    plan['classification'] = 'already_populated'
                    already_count += 1
                else:
                    plan['classification'] = 'stop'
                    plan['_stop_reason'] = (
                        f'Mismatch: stored (colour={repr(db_colour)}, '
                        f'border={repr(db_border)}, font={repr(db_font)}) '
                        f'≠ expected (colour={repr(colour_key)}, '
                        f'border={repr(border_key)}, font={repr(font_key)})'
                    )
                    stop_rows.append(plan)

            else:
                # partially populated — STOP
                present = []
                missing = []
                for fname, val in [('card_colour', db_colour), ('card_border', db_border), ('card_font', db_font)]:
                    if val is not None:
                        present.append(f'{fname}={repr(val)}')
                    else:
                        missing.append(fname)
                plan['classification'] = 'stop'
                plan['_stop_reason'] = (
                    f'Partially populated: {", ".join(present)}; '
                    f'NULL fields: {", ".join(missing)}'
                )
                stop_rows.append(plan)

            planned_updates.append(plan)

        # ── report plan ──
        print(f'Total rows: {total}')
        print()

        header = f'{'id':>4s}  {'classification':20s}  {'style':30s}  {'colour':12s}  {'border':12s}  {'font':12s}'
        print(header)
        print('-' * len(header))
        for p in planned_updates:
            cls = p['classification']
            col = p['colour'] or '-'
            bor = p['border'] or '-'
            fon = p['font'] or '-'
            print(f'{p["id"]:>4d}  {cls:20s}  {repr(p["original_card_style"]):30s}  {str(col):12s}  {str(bor):12s}  {str(fon):12s}')
            if cls == 'stop' and '_stop_reason' in p:
                print(f'       STOP: {p["_stop_reason"]}')

        print()
        print(f'Backfill: {backfill_count}')
        print(f'Already populated (skipped): {already_count}')
        print(f'Stopped: {len(stop_rows)}')

        # ── stop condition ──
        if stop_rows:
            print()
            print('*** STOP CONDITION HIT — no write attempted ***')
            if not apply_flag:
                print('(dry-run — no rows were written)')
            sys.exit(1)

        # ── Step 3: write (--apply only) ──
        if not apply_flag:
            print()
            print('Dry-run complete.  Pass --apply to write.')
            sys.exit(0)

        # Confirm before writing
        print()
        resp = input('Type YES to backfill {} rows: '.format(backfill_count))
        if resp.strip() != 'YES':
            print('Aborted.')
            sys.exit(1)

        # Capture updated_at before any writes
        before_map = {}
        for p in planned_updates:
            if p['classification'] == 'backfill':
                before_map[p['id']] = p['updated_at_before']

        # Build the backfill plan rows (only backfill-classified)
        to_write = [p for p in planned_updates if p['classification'] == 'backfill']

        # Execute in a single transaction
        try:
            with engine.begin() as conn:
                for p in to_write:
                    conn.execute(
                        sa.text(
                            'UPDATE clients '
                            'SET card_colour = :colour, card_border = :border, card_font = :font '
                            'WHERE id = :id'
                        ),
                        {
                            'id': p['id'],
                            'colour': p['colour'],
                            'border': p['border'],
                            'font': p['font'],
                        }
                    )
        except Exception:
            print('ERROR: write failed, transaction rolled back.')
            raise

        # ── verify after write ──
        print()
        print('Verification — post-write state:')
        print()

        after_rows = db.session.execute(
            sa.text(
                'SELECT id, card_style, card_colour, card_border, card_font, updated_at '
                'FROM clients ORDER BY id'
            )
        ).all()

        h2 = f'{'id':>4s}  {'style':30s}  {'colour':12s}  {'border':12s}  {'font':12s}  {'updated_at unchanged?':22s}'
        print(h2)
        print('-' * len(h2))

        updated_at_ok = True
        card_style_ok = True
        all_match = True

        for ar in after_rows:
            colour_str = str(ar.card_colour) if ar.card_colour is not None else 'NULL'
            border_str = str(ar.card_border) if ar.card_border is not None else 'NULL'
            font_str = str(ar.card_font) if ar.card_font is not None else 'NULL'

            # find plan for this row
            plan = next(p for p in planned_updates if p['id'] == ar.id)
            expected_colour = plan['colour']
            expected_border = plan['border']
            expected_font = plan['font']

            colour_match = ar.card_colour == expected_colour
            border_match = ar.card_border == expected_border
            font_match = ar.card_font == expected_font
            row_ok = colour_match and border_match and font_match
            if not row_ok:
                all_match = False

            # updated_at check
            if plan['classification'] == 'backfill':
                if ar.updated_at != plan['updated_at_before']:
                    updated_at_ok = False
                    ua_label = 'CHANGED!'
                else:
                    ua_label = 'unchanged'
            else:
                ua_label = '(n/a)'

            # card_style check
            cs_ok = ar.card_style == plan['original_card_style']
            if not cs_ok:
                card_style_ok = False

            marker = '' if row_ok else '  <-- MISMATCH'
            print(f'{ar.id:>4d}  {repr(ar.card_style):30s}  {colour_str:12s}  {border_str:12s}  {font_str:12s}  {ua_label:22s}{marker}')

        print()
        print(f'Total rows:               {total}')
        print(f'Backfilled:               {backfill_count}')
        print(f'Already populated:        {already_count}')
        print(f'Stopped:                  {len(stop_rows)}')
        print(f'All values match plan:    {all_match}')
        print(f'updated_at unchanged:     {updated_at_ok}')
        print(f'card_style unchanged:     {card_style_ok}')

        if not (all_match and updated_at_ok and card_style_ok):
            print()
            print('WARNING: some checks failed — review output above.')
            sys.exit(1)

        print()
        print('Backfill complete.  All checks passed.')


if __name__ == '__main__':
    main()
