# scripts/regen_pdf_keys.py
# Pass 1 — regenerate PDF/QR assets and write unguessable pdf_r2_key for a
# whitelisted set of clients. ADDITIVE ONLY. No deletes. Old R2 objects untouched.
#
# Usage:
#   python scripts/regen_pdf_keys.py            # dry run, no writes
#   python scripts/regen_pdf_keys.py --commit   # real run
#
# Requires prod DATABASE_URL + R2 env vars set in the shell before running.

import sys
from app import create_app, db
from app.models import Client
from app.services.generator import generate_assets

# Explicit whitelist — the ONLY rows to touch. Everything else is test data
# scheduled for DB cleanup and is deliberately excluded.
KEEP_IDS = {49, 52}  # 49=cardbranch (demo), 52=da-workforce (DA Workforce Demo)

SITE_URL = 'https://cardbranch.co.uk'  # base used to build the QR target

def main():
    commit = '--commit' in sys.argv
    app = create_app()
    with app.app_context():
        clients = Client.query.filter(Client.id.in_(KEEP_IDS)).order_by(Client.id).all()

        found_ids = {c.id for c in clients}
        missing = KEEP_IDS - found_ids
        if missing:
            print(f'ABORT: expected client ids {sorted(KEEP_IDS)}, missing {sorted(missing)}')
            return

        if len(clients) != len(KEEP_IDS):
            print(f'ABORT: matched {len(clients)} rows, expected {len(KEEP_IDS)}')
            return

        print(f'{"COMMIT" if commit else "DRY RUN"} — {len(clients)} client(s)')
        print('-' * 60)
        for c in clients:
            print(f'id={c.id} slug={c.slug!r} brand={c.brand_name!r}')
            print(f'  logo_filename = {c.logo_filename!r}')
            print(f'  old pdf_r2_key = {c.pdf_r2_key!r}')
            if not commit:
                print('  -> would regenerate assets and write a new tokenised key')
                print()
                continue

            new_key = generate_assets(
                slug=c.slug,
                brand_name=c.brand_name,
                tagline=c.tagline,
                site_url=SITE_URL,
                logo_filename=c.logo_filename,
                card_colour=c.card_colour,
                card_border=c.card_border,
                card_font=c.card_font,
            )
            c.pdf_r2_key = new_key
            db.session.commit()
            print(f'  -> committed new pdf_r2_key = {new_key!r}')
            print()

        print('-' * 60)
        print('Done.' if commit else 'Dry run complete. No writes.')

if __name__ == '__main__':
    main()