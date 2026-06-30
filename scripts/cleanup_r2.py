"""
R2 cleanup: deletes 132 test/dev objects, keeps the 3 cardbranch objects.
No DB writes. Only R2 delete_objects after both safety gates pass.
"""
import sys
import os
import re

if '--confirm-delete-r2-test-assets' not in sys.argv:
    print('ABORT: --confirm-delete-r2-test-assets flag is required.')
    print('Usage: python scripts/cleanup_r2.py --confirm-delete-r2-test-assets')
    sys.exit(1)

from app import create_app, db
from app.models import Client
from app.services.r2 import get_r2_client

KEEP_SLUG = 'cardbranch'
EXPECTED_LOGO_KEY = 'uploads/c574e35e65e045aca72e9cc366bce367.png'
KEEP_KEYS = {
    'generated/cardbranch/card.pdf',
    'generated/cardbranch/qr.png',
    EXPECTED_LOGO_KEY,
}

app = create_app()

with app.app_context():
    # ── Confirm PostgreSQL ──
    backend = db.engine.url.get_backend_name()
    if backend != 'postgresql':
        print(f'ABORT: database backend is "{backend}", not PostgreSQL.')
        sys.exit(1)

    raw_host = db.engine.url.host or 'unknown'
    masked_host = re.sub(r'^[^.]+', '****', raw_host)
    print(f'Connected: dialect={backend}, host={masked_host}')

    # ── Verify cardbranch logo_filename ──
    keep_client = Client.query.filter_by(slug=KEEP_SLUG).first()
    if not keep_client:
        print(f'ABORT: keep card slug "{KEEP_SLUG}" not found in database.')
        sys.exit(1)

    actual_logo = keep_client.logo_filename or ''
    print(f'Cardbranch logo_filename: "{actual_logo}"')

    if actual_logo != EXPECTED_LOGO_KEY:
        print(f'ABORT: logo_filename mismatch.')
        print(f'  Expected: "{EXPECTED_LOGO_KEY}"')
        print(f'  Actual:   "{actual_logo}"')
        sys.exit(1)

    print('Logo_filename check: PASSED')
    print()

    # ── List all R2 objects ──
    r2 = get_r2_client()
    bucket = os.environ.get('R2_BUCKET_NAME', 'cardbranch-assets')
    print(f'R2 bucket: {bucket}')

    all_keys = []
    paginator = r2.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get('Contents', []):
            all_keys.append(obj['Key'])

    print(f'Total objects in bucket: {len(all_keys)}')

    keep_list = []
    delete_list = []
    unknown_list = []

    for key in all_keys:
        if key in KEEP_KEYS:
            keep_list.append(key)
        else:
            delete_list.append(key)

    # Verify no keep key appears in delete list
    for k in keep_list:
        if k in delete_list:
            print(f'ERROR: keep key "{k}" also in delete list!')
            sys.exit(1)

    # Verify keep count vs expectations
    print(f'  KEEP:              {len(keep_list)}')
    print(f'  DELETE_CANDIDATE:  {len(delete_list)}')
    print(f'  UNKNOWN:           {len(unknown_list)}')
    print()

    # Pre-deletion validation checks
    checks_ok = True

    if len(keep_list) != 3:
        print(f'Pre-check FAIL: expected 3 keep keys, found {len(keep_list)}')
        checks_ok = False

    if len(delete_list) != 132:
        print(f'Pre-check FAIL: expected 132 delete candidates, found {len(delete_list)}')
        checks_ok = False

    if unknown_list:
        print(f'Pre-check FAIL: {len(unknown_list)} unknown keys')
        checks_ok = False

    for keep_key in KEEP_KEYS:
        if keep_key not in keep_list:
            print(f'Pre-check FAIL: keep key "{keep_key}" not found in bucket')
            checks_ok = False
        if keep_key in delete_list:
            print(f'Pre-check FAIL: keep key "{keep_key}" in delete list!')
            checks_ok = False

    if not checks_ok:
        print()
        print('Pre-deletion checks failed. Aborting.')
        sys.exit(1)

    print('Pre-deletion checks: PASSED')
    print()

    # ── Print deletion plan ──
    print('=' * 60)
    print('DELETION PLAN')
    print('=' * 60)
    print(f'Total objects: {len(all_keys)}')
    print(f'KEEP ({len(keep_list)}):')
    for k in sorted(keep_list):
        print(f'  {k}')
    print(f'DELETE ({len(delete_list)}):')
    for k in sorted(delete_list):
        print(f'  {k}')
    print()

    # ── Confirmation prompt ──
    print('Type DELETE (all caps) to confirm permanent R2 deletion:')
    try:
        response = input('> ')
    except (EOFError, KeyboardInterrupt):
        print()
        print('Aborted.')
        sys.exit(1)

    if response != 'DELETE':
        print('Aborted — did not receive exactly "DELETE".')
        print('No objects were deleted.')
        sys.exit(1)

    # ── Execute deletion ──
    batch_size = 1000
    deleted_count = 0
    for i in range(0, len(delete_list), batch_size):
        batch = delete_list[i:i + batch_size]
        objects_to_delete = [{'Key': k} for k in batch]
        r2.delete_objects(Bucket=bucket, Delete={'Objects': objects_to_delete})
        deleted_count += len(batch)
        print(f'Deleted {deleted_count}/{len(delete_list)} objects...')

    print(f'\nDeletion complete: {deleted_count} objects removed.')

    # ── Post-deletion verification ──
    print()
    print('=' * 60)
    print('POST-DELETION VERIFICATION')
    print('=' * 60)

    remaining_keys = []
    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get('Contents', []):
            remaining_keys.append(obj['Key'])

    print(f'Objects remaining in bucket: {len(remaining_keys)}')

    if len(remaining_keys) != 3:
        print(f'FAIL: expected 3 remaining objects, found {len(remaining_keys)}')

    all_keep_present = True
    for keep_key in KEEP_KEYS:
        if keep_key in remaining_keys:
            print(f'  PRESENT: {keep_key}')
        else:
            print(f'  MISSING: {keep_key} ***')
            all_keep_present = False

    if len(remaining_keys) == 3 and all_keep_present:
        print()
        print('Verification PASSED — all 3 keep keys intact, 132 candidates removed.')
    else:
        print()
        print('Verification FAILED — investigate immediately.')

    print()
    print('Done.')
