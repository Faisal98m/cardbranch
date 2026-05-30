import stripe
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Client, Order, db

checkout_bp = Blueprint('checkout', __name__)

TIERS = {
    'basic':    {'label': 'Basic',    'price': 4900,  'quantity': 50,   'display': '£49'},
    'standard': {'label': 'Standard', 'price': 8500,  'quantity': 1000, 'display': '£85'},
    'premium':  {'label': 'Premium',  'price': 12000, 'quantity': 2000, 'display': '£120'},
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

        delivery_name = request.form.get('delivery_name', '').strip()
        delivery_line1 = request.form.get('delivery_line1', '').strip()
        delivery_line2 = request.form.get('delivery_line2', '').strip()
        delivery_city = request.form.get('delivery_city', '').strip()
        delivery_postcode = request.form.get('delivery_postcode', '').strip()

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
                    'order_id': order.id,
                    'client_id': client.id,
                    'tier': tier,
                },
                customer_email=current_user.email,
            )
            order.stripe_session_id = session.id
            db.session.commit()
            return redirect(session.url, code=303)

        except stripe.error.StripeError as e:
            db.session.delete(order)
            db.session.commit()
            flash(f'Payment error: {str(e)}', 'error')
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
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config['STRIPE_WEBHOOK_SECRET']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return '', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order = Order.query.filter_by(stripe_session_id=session['id']).first()
        if order:
            order.status = 'paid'
            order.stripe_payment_id = session.get('payment_intent', '')
            db.session.commit()

    return '', 200
