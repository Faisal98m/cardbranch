import stripe
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Client, Order, db
from app import csrf

checkout_bp = Blueprint('checkout', __name__)

TIERS = {
    'digital': {
        'label': 'Digital',
        'price': 1900,
        'quantity': 0,
        'display': '£19',
        'description': 'QR code + print-ready PDF. No physical cards.',
        'includes': ['Hosted links page', 'QR code download', 'Print-ready PDF (85×55mm)'],
    },
    'standard': {
        'label': 'Standard',
        'price': 5900,
        'quantity': 250,
        'display': '£59',
        'description': '250 printed cards delivered to your door.',
        'includes': ['Everything in Digital', '250 printed cards', 'Matt laminate finish', 'Delivered in 5–7 days'],
    },
    'premium': {
        'label': 'Premium',
        'price': 8500,
        'quantity': 500,
        'display': '£85',
        'description': '500 printed cards delivered to your door.',
        'includes': ['Everything in Digital', '500 printed cards', 'Matt laminate finish', 'Delivered in 5–7 days'],
    },
}


@checkout_bp.route('/card/<int:id>/order', methods=['GET', 'POST'])
@login_required
def order(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        tier = request.form.get('tier', 'standard')
        if tier not in TIERS:
            flash('Invalid tier selected.', 'error')
            return redirect(url_for('checkout.order', id=id))

        delivery_name = delivery_line1 = delivery_line2 = delivery_city = delivery_postcode = ''
        if tier != 'digital':
            delivery_name = request.form.get('delivery_name', '')
            delivery_line1 = request.form.get('delivery_line1', '')
            delivery_line2 = request.form.get('delivery_line2', '')
            delivery_city = request.form.get('delivery_city', '')
            delivery_postcode = request.form.get('delivery_postcode', '')

            if not all([delivery_name, delivery_line1, delivery_city, delivery_postcode]):
                flash('Please fill in all required delivery fields.', 'error')
                return redirect(url_for('checkout.order', id=id))

        tier_data = TIERS[tier]

        order = Order(
            user_id=current_user.id,
            client_id=client.id,
            tier=tier,
            quantity=tier_data['quantity'],
            amount_paid=tier_data['price'] / 100,
            status='pending',
            delivery_name=delivery_name,
            delivery_line1=delivery_line1,
            delivery_line2=delivery_line2,
            delivery_city=delivery_city,
            delivery_postcode=delivery_postcode,
        )
        db.session.add(order)
        db.session.commit()

        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        site_url = current_app.config['SITE_URL']

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount': tier_data['price'],
                        'product_data': {
                            'name': f"CardBranch {tier_data['label']} — {client.brand_name}",
                            'description': f"{tier_data['quantity']} premium business cards printed and delivered",
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{site_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{site_url}/card/{id}",
                metadata={
                    'order_id': str(order.id),
                    'client_id': str(client.id),
                    'user_id': str(current_user.id),
                    'tier': tier,
                },
                customer_email=current_user.email,
            )
            order.stripe_session_id = session.id
            db.session.commit()
            return redirect(session.url, code=303)

        except stripe.error.StripeError as e:
            current_app.logger.error(f"Stripe error during checkout: {e}")
            db.session.delete(order)
            db.session.commit()
            flash('Something went wrong processing your payment. Please try again or contact support.', 'error')
            return redirect(url_for('checkout.order', id=id))

    return render_template('checkout/order.html', client=client, tiers=TIERS)


@checkout_bp.route('/checkout/success')
@login_required
def success():
    session_id = request.args.get('session_id')
    order = Order.query.filter_by(stripe_session_id=session_id, user_id=current_user.id).first_or_404()
    client = Client.query.get(order.client_id)
    return render_template('checkout/success.html', order=order, client=client, tiers=TIERS)


@checkout_bp.route('/checkout/cancel')
@login_required
def cancel():
    flash('Payment cancelled.', 'info')
    return redirect(url_for('dashboard.index'))


@checkout_bp.route('/webhooks/stripe', methods=['POST'])
@csrf.exempt
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config['STRIPE_WEBHOOK_SECRET']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        current_app.logger.error(f"Stripe webhook signature verification failed: {e}")
        return '', 400

    current_app.logger.info(f"Stripe webhook received: {event['type']} (id={event['id']})")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        try:
            order = Order.query.filter_by(stripe_session_id=session['id']).first()
            if order:
                client = order.client
                from app.services.generator import generate_assets
                client.pdf_r2_key = generate_assets(client.slug, client.brand_name, client.tagline,
                                                    current_app.config['SITE_URL'],
                                                    logo_filename=client.logo_filename,
                                                    card_colour=client.card_colour,
                                                    card_border=client.card_border,
                                                    card_font=client.card_font)
                order.status = 'paid'
                order.stripe_payment_id = session.get('payment_intent', '')
                client.is_published = True
                from datetime import datetime
                client.published_at = datetime.utcnow()
                db.session.commit()
                current_app.logger.info(f"Order {order.id} status updated to '{order.status}' via webhook; card {client.id} published")
                from app.services.email import send_order_confirmation, send_admin_notification
                from app.models import User
                user = User.query.get(order.user_id)
                send_order_confirmation(order, client, user)
                send_admin_notification(order, client, user)
            else:
                current_app.logger.warning(f"Order not found for stripe_session_id={session['id']}")
        except Exception as e:
            current_app.logger.error(f"Error processing checkout.session.completed: {e}")
            return '', 500
    else:
        current_app.logger.info(f"Unhandled event type: {event['type']}")

    return '', 200
