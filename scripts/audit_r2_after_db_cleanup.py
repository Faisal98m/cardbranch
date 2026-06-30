"""
Read-only R2 audit based on current production DB state.
Classifies every R2 object as KEEP, DELETE_CANDIDATE, or UNKNOWN_MANUAL_REVIEW.
No deletions. No DB writes. No R2 writes.
"""
import sys
import os
import re

from app import create_app, db
from app.models import Client
from app.services.r2 import get_r2_client

KEEP_SLUG = 'cardbranch'

app = create_app()

with app.app_context():
    # ── Confirm PostgreSQL ──
    backend = db.engine.url.get_backend_name()
    if backend != 'postgresql':
        print(f'ABORT: database backend is "{backend}", not PostgreSQL.')
        sys.exit(1)

    raw_host = db.engine.url.host or 'unknown'
    raw_db = db.engine.url.database or 'unknown'
    masked_host = re.sub(r'^[^.]+', '****', raw_host)
    print(f'Connected: dialect={backend}, host={masked_host}, database={raw_db}')
    print()

    # ── Query remaining card ──
    keep_client = Client.query.filter_by(slug=KEEP_SLUG).first()
    if not keep_client:
        print(f'ABORT: keep card slug "{KEEP_SLUG}" not found in database.')
        sys.exit(1)

    print('Keep card:')
    print(f'  client id:     {keep_client.id}')
    print(f'  slug:          {keep_client.slug}')
    print(f'  logo_filename: {keep_client.logo_filename or "(none)"}')
    print()

    # ── List R2 objects ──
    r2 = get_r2_client()
    bucket = os.environ.get('R2_BUCKET_NAME', 'cardbranch-assets')
    print(f'R2 bucket: {bucket}')
    print()

    keep_keys = []
    delete_candidate_keys = []
    unknown_keys = []

    def paginate_list(bucket_name):
        """Yield all object keys and sizes from the bucket, handling pagination."""
        paginator = r2.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get('Contents', []):
                yield obj['Key'], obj['Size']

    slug_pattern = re.compile(r'^generated/([^/]+)/(card\.pdf|qr\.png)$')
    upload_pattern = re.compile(r'^uploads/(.+)')

    for key, size in paginate_list(bucket):
        slug_match = slug_pattern.match(key)
        upload_match = upload_pattern.match(key)

        if slug_match:
            slug = slug_match.group(1)
            if slug == KEEP_SLUG:
                keep_keys.append((key, size))
            else:
                delete_candidate_keys.append((key, size))

        elif upload_match:
            filename = upload_match.group(1)
            if keep_client.logo_filename and key == keep_client.logo_filename:
                keep_keys.append((key, size))
            else:
                delete_candidate_keys.append((key, size))

        else:
            unknown_keys.append((key, size))

    # ── Print classifications ──
    print('R2 key naming patterns found:')
    print('  generated/{slug}/card.pdf')
    print('  generated/{slug}/qr.png')
    print('  uploads/{uuid}.{ext}')
    if unknown_keys:
        for key, size in unknown_keys:
            print(f'  {key} (unknown pattern)')
    print()

    # KEEP
    print(f'KEEP ({len(keep_keys)}):')
    keep_keys.sort(key=lambda x: x[0])
    for key, size in keep_keys:
        label = 'logo' if key.startswith('uploads/') else 'generated'
        print(f'  [{label}] {key} ({size} bytes)')

    # DELETE_CANDIDATE
    print(f'\nDELETE_CANDIDATE ({len(delete_candidate_keys)}):')
    delete_candidate_keys.sort(key=lambda x: x[0])
    for key, size in delete_candidate_keys:
        print(f'  {key} ({size} bytes)')

    # UNKNOWN_MANUAL_REVIEW
    if unknown_keys:
        print(f'\nUNKNOWN_MANUAL_REVIEW ({len(unknown_keys)}):')
        unknown_keys.sort(key=lambda x: x[0])
        for key, size in unknown_keys:
            print(f'  {key} ({size} bytes)')
    else:
        print(f'\nUNKNOWN_MANUAL_REVIEW: none (all keys matched known patterns)')

    # ── Summary ──
    total = len(keep_keys) + len(delete_candidate_keys) + len(unknown_keys)
    print()
    print('=' * 60)
    print('SUMMARY')
    print('=' * 60)
    print(f'  Total R2 objects:     {total}')
    print(f'  KEEP:                 {len(keep_keys)}')
    print(f'  DELETE_CANDIDATE:     {len(delete_candidate_keys)}')
    print(f'  UNKNOWN_MANUAL_REVIEW: {len(unknown_keys)}')
    print()
    print('Read-only audit complete. No data was modified.')
