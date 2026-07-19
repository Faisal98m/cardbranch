"""
Dry-run: identifies what a future DB cleanup would delete.
Read-only — no commit, no delete, no R2 calls.
"""
import sys
import os

from app import create_app, db
from app.models import User, Client, Link, Order

KEEP_USER_EMAIL = 'faisal.maroof791@gmail.com'
KEEP_CARD_SLUG = 'cardbranch'

DISPUTED_SLUGS = [
    'da-workforce-5', 'new-workforce', 'da-workforce11',
    'test-checkout', 'cardbrancheew', 'brandnew',
    'new-workforce-2', 'loadingfeature',
]


def fmt_ts(val):
    return val.strftime('%Y-%m-%d %H:%M UTC') if val else 'N/A'


app = create_app()

with app.app_context():
    # ── DANGER CHECK: scan EVERY order for live-mode Stripe sessions ──
    all_orders = Order.query.all()
    for o in all_orders:
        sid = (o.stripe_session_id or '').strip()
        if sid and not sid.startswith('cs_test_'):
            client = Client.query.get(o.client_id)
            client_slug = client.slug if client else 'N/A'
            user = User.query.get(o.user_id)
            user_email = user.email if user else 'N/A'
            print('=' * 72)
            print('DANGER: LIVE PAYMENT FOUND')
            print('=' * 72)
            print(f'  Order #{o.id}')
            print(f'  Card slug: {client_slug}')
            print(f'  Owner: {user_email}')
            print(f'  Status: {o.status}')
            print(f'  Amount: {o.amount_paid}')
            print(f'  Stripe session: {sid}')
            print(f'  Stripe payment: {o.stripe_payment_id or "N/A"}')
            print()
            print('Halting — not safe to proceed. Manual review required.')
            sys.exit(1)

    # ── DANGER passed ──
    print('Live-mode payment check: PASSED (all sessions are cs_test_ test mode)')
    print()

    # ── USERS TO DELETE (everyone except keep user) ──
    delete_users = User.query.filter(User.email != KEEP_USER_EMAIL).order_by(User.id).all()

    # ── CLIENTS TO REVIEW (all except cardbranch) ──
    all_except_keep = Client.query.filter(Client.slug != KEEP_CARD_SLUG).order_by(Client.id).all()

    disputed_clients = []
    candidate_clients = []

    for c in all_except_keep:
        if c.slug in DISPUTED_SLUGS:
            disputed_clients.append(c)
        else:
            candidate_clients.append(c)

    # ── DISPUTED SECTION ──
    print('=' * 72)
    print('DISPUTED — DO NOT AUTO-DELETE (full detail)')
    print('=' * 72)
    print()
    print(f'These {len(disputed_clients)} cards require human review before any deletion.')
    print(f'A human must confirm each card is safe to delete.')
    print()

    for c in disputed_clients:
        owner = User.query.get(c.user_id)
        owner_email = owner.email if owner else 'N/A'
        print(f'--- Card #{c.id}: slug="{c.slug}" brand="{c.brand_name}" ---')
        print(f'  Owner: {owner_email}')
        print(f'  Created: {fmt_ts(c.created_at)}')
        print(f'  Colour: {c.card_colour} / Border: {c.card_border} / Font: {c.card_font}')

        links = Link.query.filter_by(client_id=c.id).order_by(Link.display_order).all()
        if links:
            print(f'  Links ({len(links)}):')
            for l in links:
                print(f'    [{l.platform}] {l.url}')
        else:
            print(f'  Links: none')

        orders = Order.query.filter_by(client_id=c.id).order_by(Order.id).all()
        if orders:
            print(f'  Orders ({len(orders)}):')
            for o in orders:
                print(f'    Order #{o.id}: status={o.status} amount={o.amount_paid} tier={o.tier}')
                print(f'      stripe_session={o.stripe_session_id or "N/A"}')
                print(f'      stripe_payment={o.stripe_payment_id or "N/A"}')
                print(f'      created={fmt_ts(o.created_at)}')
        else:
            print(f'  Orders: none')
        print()

    # ── CANDIDATE FOR DELETION SECTION ──
    print('=' * 72)
    print('CANDIDATE FOR DELETION (summary)')
    print('=' * 72)
    print()

    for c in candidate_clients:
        owner = User.query.get(c.user_id)
        owner_email = owner.email if owner else 'N/A'
        link_count = Link.query.filter_by(client_id=c.id).count()
        order_count = Order.query.filter_by(client_id=c.id).count()
        print(f'  Card #{c.id}: slug="{c.slug}" brand="{c.brand_name}" owner={owner_email}')
        print(f'    orders={order_count}, links={link_count}')

    # Deleted users who would lose their remaining cards
    print()
    for u in delete_users:
        remaining = Client.query.filter_by(user_id=u.id).count()
        print(f'  User "{u.email}" — {remaining} card(s) to be cascaded')

    # ── SUMMARY ──
    print()
    print('=' * 72)
    print('SUMMARY')
    print('=' * 72)

    # Users
    total_users = User.query.count()
    keep_user = User.query.filter_by(email=KEEP_USER_EMAIL).first()
    print(f'  Users: {total_users} total')
    print(f'    KEEP:     1 ({KEEP_USER_EMAIL})')
    print(f'    DELETE:   {len(delete_users)} ({", ".join(u.email for u in delete_users)})')

    # Cards
    keep_card = Client.query.filter_by(slug=KEEP_CARD_SLUG).first()
    total_cards = Client.query.count()
    print(f'  Cards: {total_cards} total')
    print(f'    KEEP:         1 (slug="{KEEP_CARD_SLUG}")')
    print(f'    DISPUTED:     {len(disputed_clients)} (listed above — human review)')
    print(f'    CANDIDATE:    {len(candidate_clients)} (ready for deletion)')

    # Orders
    keep_order_ids = set()
    if keep_card:
        for o in Order.query.filter_by(client_id=keep_card.id).all():
            keep_order_ids.add(o.id)
    disputed_order_ids = set()
    for c in disputed_clients:
        for o in Order.query.filter_by(client_id=c.id).all():
            disputed_order_ids.add(o.id)
    candidate_order_ids = set()
    for c in candidate_clients:
        for o in Order.query.filter_by(client_id=c.id).all():
            candidate_order_ids.add(o.id)

    print(f'  Orders: {len(all_orders)} total')
    print(f'    KEEP ({len(keep_order_ids)}): belong to {KEEP_CARD_SLUG}')
    print(f'    DISPUTED ({len(disputed_order_ids)}): belong to disputed cards')
    print(f'    CANDIDATE ({len(candidate_order_ids)}): would be deleted with their cards')

    # Links
    keep_link_count = Link.query.filter(Link.client_id == (keep_card.id if keep_card else -1)).count() if keep_card else 0
    disputed_link_count = 0
    candidate_link_count = 0
    for c in disputed_clients:
        disputed_link_count += Link.query.filter_by(client_id=c.id).count()
    for c in candidate_clients:
        candidate_link_count += Link.query.filter_by(client_id=c.id).count()

    print(f'  Links: {Link.query.count()} total')
    print(f'    KEEP ({keep_link_count}): belong to {KEEP_CARD_SLUG}')
    print(f'    DISPUTED ({disputed_link_count}): belong to disputed cards')
    print(f'    CANDIDATE ({candidate_link_count}): would be deleted with their cards')

    print()
    print(f'  Untouched: User "{KEEP_USER_EMAIL}", card slug "{KEEP_CARD_SLUG}",')
    print(f'             and that card\'s {keep_link_count} links + {len(keep_order_ids)} orders.')
    print()

    print('Dry-run complete. No data was modified.')
    print('=' * 72)
