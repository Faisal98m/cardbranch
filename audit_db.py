"""
Audit script: read-only inventory of all Users, Clients, Orders, Links, and R2 objects.
Flags KEEP (faisal.maroof791@gmail.com / cardbranch slug) vs CANDIDATE FOR DELETION.
"""
import os
import sys

os.environ['FLASK_CONFIG'] = 'Debug'

from app import create_app, db
from app.models import User, Client, Link, Order

app = create_app()

KEEP_USER_EMAIL = 'faisal.maroof791@gmail.com'
KEEP_SLUG = 'cardbranch'


def fmt_ts(val):
    return val.strftime('%Y-%m-%d %H:%M UTC') if val else 'N/A'


def flag(email, slug):
    """Return KEEP or CANDIDATE label."""
    if email == KEEP_USER_EMAIL and slug == KEEP_SLUG:
        return '** KEEP **'
    return 'CANDIDATE FOR DELETION'


with app.app_context():
    # ── 1. USERS ──
    print('=' * 72)
    print('1. USERS')
    print('=' * 72)
    users = User.query.order_by(User.id).all()
    for u in users:
        card_count = Client.query.filter_by(user_id=u.id).count()
        label = '** KEEP **' if u.email == KEEP_USER_EMAIL else 'CANDIDATE FOR DELETION'
        print(f'  [{label}] User #{u.id}: {u.email}')
        print(f'           admin={u.is_admin}, created={fmt_ts(u.created_at)}, cards={card_count}')

    # ── 2. CLIENTS / CARDS ──
    print()
    print('=' * 72)
    print('2. CLIENTS / CARDS')
    print('=' * 72)
    clients = Client.query.order_by(Client.user_id, Client.id).all()
    for c in clients:
        owner = User.query.get(c.user_id)
        owner_email = owner.email if owner else 'N/A'
        order_count = Order.query.filter_by(client_id=c.id).count()
        label = flag(owner_email, c.slug)
        print(f'  [{label}] Card #{c.id}: slug={c.slug}, brand="{c.brand_name}"')
        print(f'           owner={owner_email}, created={fmt_ts(c.created_at)}, orders={order_count}')

    # ── 3. ORDERS ──
    print()
    print('=' * 72)
    print('3. ORDERS')
    print('=' * 72)
    orders = Order.query.order_by(Order.id).all()
    for o in orders:
        client = Client.query.get(o.client_id)
        client_slug = client.slug if client else 'N/A'
        owner = User.query.get(o.user_id)
        owner_email = owner.email if owner else 'N/A'
        print(f'  Order #{o.id}: client_slug={client_slug}, owner={owner_email}')
        print(f'           status={o.status}, amount=£{o.amount_paid:.2f}, tier={o.tier}')
        print(f'           stripe_session={o.stripe_session_id or "N/A"}')
        print(f'           stripe_payment={o.stripe_payment_id or "N/A"}')
        print(f'           created={fmt_ts(o.created_at)}')

        # Flag if live-mode payment outside keep list
        if o.status in ('paid', 'dispatched', 'delivered'):
            if not o.stripe_session_id or not o.stripe_session_id.startswith('cs_test_'):
                # Session IDs starting with cs_live_ indicate live mode, cs_test_ is test
                if o.stripe_session_id and o.stripe_session_id.startswith('cs_live_'):
                    parent_ok = flag(owner_email, client_slug) == '** KEEP **'
                    if not parent_ok:
                        print(f'  *** WARNING: Live payment Order #{o.id} for non-keep card! ***')
                        print(f'      stripe_session={o.stripe_session_id}')
                        print(f'      stripe_payment={o.stripe_payment_id}')

    # ── 4. LINKS (counts by card) ──
    print()
    print('=' * 72)
    print('4. LINKS (count by card)')
    print('=' * 72)
    clients2 = Client.query.order_by(Client.id).all()
    for c in clients2:
        link_count = Link.query.filter_by(client_id=c.id).count()
        if link_count:
            owner = User.query.get(c.user_id)
            owner_email = owner.email if owner else 'N/A'
            print(f'  Card #{c.id} slug={c.slug} (owner={owner_email}): {link_count} links')

    # ── 5. R2 OBJECTS ──
    print()
    print('=' * 72)
    print('5. R2 OBJECTS (cardbranch-assets bucket)')
    print('=' * 72)
    try:
        from app.services.r2 import get_r2_client
        r2 = get_r2_client()
        bucket = os.environ.get('R2_BUCKET_NAME', 'cardbranch-assets')
        response = r2.list_objects_v2(Bucket=bucket)
        objects = response.get('Contents', [])
        print(f'  Total objects in bucket: {len(objects)}')
        print()

        # Collect all known slugs from the DB
        known_slugs = set(c.slug for c in Client.query.all())
        # Collect all stored logo keys
        known_logos = set(c.logo_filename for c in Client.query.all() if c.logo_filename)

        for obj in objects:
            key = obj['Key']
            size = obj['Size']
            # Determine if this key belongs to a keep or candidate card
            keep = False

            # Pattern: generated/{slug}/card.pdf or generated/{slug}/qr.png
            if key.startswith('generated/'):
                parts = key.split('/')
                if len(parts) >= 2:
                    slug_part = parts[1]
                    owner = None
                    for c in clients:
                        if c.slug == slug_part:
                            owner = User.query.get(c.user_id)
                            break
                    owner_email = owner.email if owner else 'UNKNOWN'
                    if slug_part == KEEP_SLUG:
                        keep = True
                        label = '** KEEP **'
                    else:
                        label = 'CANDIDATE FOR DELETION'
                    print(f'  [{label}] {key} ({size} bytes) — slug="{slug_part}" owner={owner_email}')

            # Pattern: uploads/{uuid}.{ext}
            elif key.startswith('uploads/'):
                if key in known_logos:
                    # Find which card uses this logo
                    for c in clients:
                        if c.logo_filename == key:
                            owner = User.query.get(c.user_id)
                            owner_email = owner.email if owner else 'N/A'
                            label = flag(owner_email, c.slug)
                            print(f'  [{label}] {key} ({size} bytes) — used by card #{c.id} slug={c.slug}')
                            break
                else:
                    print(f'  [ORPHAN] {key} ({size} bytes) — not referenced by any card in DB')

            else:
                print(f'  [UNKNOWN PATTERN] {key} ({size} bytes)')

        # Check if there are more pages of objects
        while response.get('IsTruncated'):
            token = response.get('NextContinuationToken')
            response = r2.list_objects_v2(Bucket=bucket, ContinuationToken=token)
            for obj in response.get('Contents', []):
                key = obj['Key']
                size = obj['Size']
                if key.startswith('generated/'):
                    parts = key.split('/')
                    if len(parts) >= 2:
                        slug_part = parts[1]
                        owner = None
                        for c in clients:
                            if c.slug == slug_part:
                                owner = User.query.get(c.user_id)
                                break
                        owner_email = owner.email if owner else 'UNKNOWN'
                        keep = slug_part == KEEP_SLUG
                        label = '** KEEP **' if keep else 'CANDIDATE FOR DELETION'
                        print(f'  [{label}] {key} ({size} bytes) — slug="{slug_part}" owner={owner_email}')
                elif key.startswith('uploads/'):
                    if key in known_logos:
                        for c in clients:
                            if c.logo_filename == key:
                                owner = User.query.get(c.user_id)
                                owner_email = owner.email if owner else 'N/A'
                                label = flag(owner_email, c.slug)
                                print(f'  [{label}] {key} ({size} bytes) — used by card #{c.id} slug={c.slug}')
                                break
                    else:
                        print(f'  [ORPHAN] {key} ({size} bytes) — not referenced by any card in DB')
                else:
                    print(f'  [UNKNOWN PATTERN] {key} ({size} bytes)')

    except Exception as e:
        print(f'  Error listing R2 objects: {e}')
        print('  (R2 may not be configured or accessible from this environment)')

    # ── SUMMARY ──
    print()
    print('=' * 72)
    print('SUMMARY')
    print('=' * 72)
    all_users = User.query.all()
    all_clients = Client.query.all()
    all_orders = Order.query.all()

    keep_user_ids = {u.id for u in all_users if u.email == KEEP_USER_EMAIL}
    keep_client_ids = {c.id for c in all_clients if c.slug == KEEP_SLUG and c.user_id in keep_user_ids}

    candidate_users = [u for u in all_users if u.id not in keep_user_ids]
    candidate_clients = [c for c in all_clients if c.id not in keep_client_ids]
    candidate_orders = [o for o in all_orders if o.client_id not in keep_client_ids]

    print(f'  Users:     {len(all_users)} total, {len(candidate_users)} candidates for deletion')
    print(f'  Cards:     {len(all_clients)} total, {len(candidate_clients)} candidates for deletion')
    print(f'  Orders:    {len(all_orders)} total, {len(candidate_orders)} candidates for deletion')

    # Check if any order has live-mode stripe session
    live_outside_keep = []
    for o in all_orders:
        if o.status in ('paid', 'dispatched', 'delivered') and o.client_id not in keep_client_ids:
            if o.stripe_session_id and o.stripe_session_id.startswith('cs_live_'):
                live_outside_keep.append(o)
    if live_outside_keep:
        print()
        print('  *** WARNING: LIVE PAYMENTS OUTSIDE KEEP LIST ***')
        for o in live_outside_keep:
            print(f'    Order #{o.id}: stripe_session={o.stripe_session_id}, amount=£{o.amount_paid:.2f}')
    else:
        print()
        print('  No live-mode payments found outside the keep list.')

    print()
    print('Script is read-only. No data was modified.')
    print('=' * 72)
