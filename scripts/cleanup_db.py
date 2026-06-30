"""
Cleanup script: deletes test/development users, cards, orders, and links
from the production database, keeping only faisal.maroof791@gmail.com
and the cardbranch card.

Two safety gates required:
  1. --confirm-delete-test-data CLI flag
  2. Typed DELETE confirmation at the prompt

Usage:
  python scripts/cleanup_db.py --confirm-delete-test-data
"""
import sys
import os
import re

# ── Parse CLI flag before any app import ──
if '--confirm-delete-test-data' not in sys.argv:
    print('ABORT: --confirm-delete-test-data flag is required.')
    print('Usage: python scripts/cleanup_db.py --confirm-delete-test-data')
    sys.exit(1)

# ── DATABASE_URL safety check (must run before create_app) ──
# If Production config is requested but DATABASE_URL is unset/empty,
# the config would silently fall back to SQLite. Catch that here.
flask_config = os.environ.get('FLASK_CONFIG', '')
db_url = os.environ.get('DATABASE_URL', '')
if flask_config == 'Production' and not db_url.strip():
    print('ABORT: FLASK_CONFIG=Production but DATABASE_URL is unset or empty.')
    print('Set DATABASE_URL to the production PostgreSQL connection string.')
    print('Do not hardcode it in source — pass it via the environment.')
    sys.exit(1)

from app import create_app, db
from app.models import User, Client, Link, Order
from sqlalchemy import text

KEEP_USER_EMAIL = 'faisal.maroof791@gmail.com'
KEEP_CARD_SLUG = 'cardbranch'

app = create_app()

with app.app_context():
    # ══════════════════════════════════════════════════════════
    # FIX 2 — Backend check: must be PostgreSQL
    # ══════════════════════════════════════════════════════════
    backend = db.engine.url.get_backend_name()
    if backend != 'postgresql':
        print(f'ABORT: connected database backend is "{backend}", not PostgreSQL.')
        print('This script is designed for PostgreSQL production only.')
        print('Refusing to proceed.')
        sys.exit(1)

    dialect_display = 'postgresql'
    raw_host = db.engine.url.host or 'unknown'
    raw_db = db.engine.url.database or 'unknown'
    masked_host = re.sub(r'^[^.]+', '****', raw_host)
    print(f'Connected: dialect={dialect_display}, host={masked_host}, database={raw_db}')
    print()

    # ══════════════════════════════════════════════════════════
    # Resolve keep user and client by ID at runtime
    # ══════════════════════════════════════════════════════════
    keep_user = User.query.filter_by(email=KEEP_USER_EMAIL).first()
    if not keep_user:
        print(f'ABORT: keep user "{KEEP_USER_EMAIL}" not found in database.')
        sys.exit(1)

    keep_client = Client.query.filter_by(slug=KEEP_CARD_SLUG).first()
    if not keep_client:
        print(f'ABORT: keep card slug "{KEEP_CARD_SLUG}" not found in database.')
        sys.exit(1)

    if keep_client.user_id != keep_user.id:
        print(f'ABORT: keep card slug "{KEEP_CARD_SLUG}" (owner user_id={keep_client.user_id})')
        print(f'       does not belong to keep user "{KEEP_USER_EMAIL}" (id={keep_user.id}).')
        sys.exit(1)

    KEEP_USER_ID = keep_user.id
    KEEP_CLIENT_ID = keep_client.id

    print(f'KEEP_USER_ID = {KEEP_USER_ID}')
    print(f'KEEP_CLIENT_ID = {KEEP_CLIENT_ID}')
    print()

    # ── Record pre-deletion keep-card order/link counts ──
    pre_keep_order_count = Order.query.filter_by(client_id=KEEP_CLIENT_ID).count()
    pre_keep_link_count = Link.query.filter_by(client_id=KEEP_CLIENT_ID).count()
    print(f'Keep card (slug="{KEEP_CARD_SLUG}"): {pre_keep_link_count} links, {pre_keep_order_count} orders')
    print()

    # ══════════════════════════════════════════════════════════
    # Live-payment check (must pass before deletion)
    # ══════════════════════════════════════════════════════════
    all_orders = Order.query.all()
    for o in all_orders:
        sid = (o.stripe_session_id or '').strip()
        if sid and not sid.startswith('cs_test_'):
            client_obj = Client.query.get(o.client_id)
            client_slug = client_obj.slug if client_obj else 'N/A'
            user_obj = User.query.get(o.user_id)
            user_email = user_obj.email if user_obj else 'N/A'
            print('=' * 72)
            print('DANGER: LIVE PAYMENT FOUND')
            print('=' * 72)
            print(f'  Order #{o.id}')
            print(f'  Card slug: {client_slug}')
            print(f'  Owner: {user_email}')
            print(f'  Status: {o.status}')
            print(f'  Amount: £{o.amount_paid:.2f}')
            print(f'  Stripe session: {sid}')
            print(f'  Stripe payment: {o.stripe_payment_id or "N/A"}')
            print()
            print('Halting — not safe to proceed. Manual review required.')
            sys.exit(1)

    print('Live-mode payment check: PASSED (all sessions are cs_test_ test mode)')
    print()

    # ══════════════════════════════════════════════════════════
    # Build deletion scope
    # ══════════════════════════════════════════════════════════
    users_to_delete = User.query.filter(User.id != KEEP_USER_ID).all()
    clients_to_delete = Client.query.filter(
        Client.user_id == KEEP_USER_ID, Client.id != KEEP_CLIENT_ID
    ).all()
    # Also delete clients owned by other users (cascaded when their owner is deleted)
    # We list them here for the deletion plan

    # Build the deletion-plan display lists
    all_candidate_clients = list(clients_to_delete)
    for u in users_to_delete:
        for c in Client.query.filter_by(user_id=u.id).all():
            if c not in all_candidate_clients:
                all_candidate_clients.append(c)

    print('=' * 72)
    print('DELETION PLAN')
    print('=' * 72)
    print(f'  Users to delete: {len(users_to_delete)}')
    for u in users_to_delete:
        owned = Client.query.filter_by(user_id=u.id).count()
        print(f'    User #{u.id}: {u.email} ({owned} card(s))')
    print(f'  Cards to delete: {len(all_candidate_clients)}')
    for c in all_candidate_clients:
        order_n = Order.query.filter_by(client_id=c.id).count()
        link_n = Link.query.filter_by(client_id=c.id).count()
        print(f'    Card #{c.id}: slug="{c.slug}" brand="{c.brand_name}" '
              f'({link_n} links, {order_n} orders)')
    total_candidate_order_count = sum(
        Order.query.filter_by(client_id=c.id).count() for c in all_candidate_clients
    )
    total_candidate_link_count = sum(
        Link.query.filter_by(client_id=c.id).count() for c in all_candidate_clients
    )
    print(f'  Orders to delete: {total_candidate_order_count}')
    print(f'  Links to delete: {total_candidate_link_count}')
    print(f'  Keep: User #{KEEP_USER_ID} "{KEEP_USER_EMAIL}", '
          f'Card #{KEEP_CLIENT_ID} slug="{KEEP_CARD_SLUG}"')
    print()

    # ══════════════════════════════════════════════════════════
    # Confirmation prompt
    # ══════════════════════════════════════════════════════════
    print('Type DELETE (all caps) to confirm permanent deletion:')
    try:
        response = input('> ')
    except (EOFError, KeyboardInterrupt):
        print()
        print('Aborted.')
        sys.exit(1)

    if response != 'DELETE':
        print('Aborted — did not receive exactly "DELETE".')
        print('No data was modified.')
        sys.exit(1)

    # ══════════════════════════════════════════════════════════
    # Execute deletion in a single transaction
    # Order: delete other users first (cascade handles their
    # cards/links/orders), then delete keep-user's extra cards.
    # ══════════════════════════════════════════════════════════
    try:
        # Delete other users first — cascade removes their clients/links/orders
        for u in users_to_delete:
            db.session.delete(u)
        # Then delete keep-user's extra cards (those not the keep card)
        for c in clients_to_delete:
            db.session.delete(c)

        print(f'Committing against: dialect={dialect_display}, host={masked_host}, database={raw_db}')
        db.session.commit()
        print('Deletion committed successfully.')
    except Exception as e:
        db.session.rollback()
        print(f'ERROR during deletion: {e}')
        print('Transaction rolled back. No data was modified.')
        sys.exit(1)

    # ══════════════════════════════════════════════════════════
    # Verification
    # ══════════════════════════════════════════════════════════
    print()
    print('=' * 72)
    print('POST-DELETION VERIFICATION')
    print('=' * 72)

    remaining_users = User.query.count()
    remaining_clients = Client.query.count()
    remaining_orders = Order.query.count()
    remaining_links = Link.query.count()

    post_keep_order_count = Order.query.filter_by(client_id=KEEP_CLIENT_ID).count()
    post_keep_link_count = Link.query.filter_by(client_id=KEEP_CLIENT_ID).count()

    print(f'  Users remaining:  {remaining_users} (expected 1)')
    print(f'  Cards remaining:  {remaining_clients} (expected 1)')
    print(f'  Orders remaining: {remaining_orders}')
    print(f'  Links remaining:  {remaining_links}')
    print()
    print(f'  Keep card (slug="{KEEP_CARD_SLUG}"):')
    print(f'    Orders: {post_keep_order_count} (pre-deletion: {pre_keep_order_count})')
    print(f'    Links:  {post_keep_link_count} (pre-deletion: {pre_keep_link_count})')

    if remaining_users == 1 and remaining_clients == 1 \
            and post_keep_order_count == pre_keep_order_count \
            and post_keep_link_count == pre_keep_link_count:
        print()
        print('Verification PASSED — keep card data fully intact.')
    else:
        print()
        print('Verification WARNING — counts do not match expectations.')
        print('Investigate before further action.')

    print()
    print('Done.')
