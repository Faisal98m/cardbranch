"""
Verify independent card design field completeness.

Usage:
    python scripts/backfill_card_design_fields.py
"""
import os
import sys

os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_CONFIG'] = 'Debug'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.services.themes import CARD_COLOURS, CARD_BORDERS, CARD_FONTS
import sqlalchemy as sa

def main():
    app = create_app('Debug')
    with app.app_context():
        rows = db.session.execute(
            sa.text('SELECT id, card_colour, card_border, card_font FROM clients ORDER BY id')
        ).all()

        total = len(rows)
        complete = 0
        null_any = 0
        bad_colour = 0
        bad_border = 0
        bad_font = 0

        print(f'Total clients: {total}')
        print()
        print(f'{"id":>4s}  {"colour":14s}  {"border":14s}  {"font":14s}  status')
        print('-' * 55)
        for row in rows:
            co = row.card_colour
            bo = row.card_border
            fo = row.card_font
            co_ok = co is not None and co in CARD_COLOURS
            bo_ok = bo is not None and bo in CARD_BORDERS
            fo_ok = fo is not None and fo in CARD_FONTS
            all_ok = co_ok and bo_ok and fo_ok
            if all_ok:
                complete += 1
            else:
                null_any += 1
            if not co_ok:
                bad_colour += 1
            if not bo_ok:
                bad_border += 1
            if not fo_ok:
                bad_font += 1
            status = 'OK' if all_ok else 'MISSING/INVALID'
            print(f'{row.id:>4d}  {str(co or "-"):14s}  {str(bo or "-"):14s}  {str(fo or "-"):14s}  {status}')

        print()
        print(f'Complete valid:  {complete}')
        print(f'Missing/invalid: {null_any}')
        print(f'Bad colour keys: {bad_colour}')
        print(f'Bad border keys: {bad_border}')
        print(f'Bad font keys:   {bad_font}')
        print()
        if null_any == 0 and bad_colour == 0 and bad_border == 0 and bad_font == 0:
            print('Database is ready for card_style column removal.')
        else:
            print('WARNING: some rows have incomplete or invalid design data.')
            print('card_style column cannot be removed until all rows are complete.')

if __name__ == '__main__':
    main()
