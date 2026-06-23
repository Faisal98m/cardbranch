import json
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Client, Link, Order, db
from app.dashboard.forms import CardForm, LinkForm
from app.services.generator import unique_slug, save_logo, generate_assets

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.created_at.desc()).all()
    colour_map = {
        'oxblood': {'bg': '#6b1f2a', 'text': '#faf8f4'},
        'navy': {'bg': '#1a2744', 'text': '#faf8f4'},
        'forest': {'bg': '#1a3d2b', 'text': '#faf8f4'},
        'slate': {'bg': '#2d3748', 'text': '#faf8f4'},
        'charcoal': {'bg': '#1a1714', 'text': '#faf8f4'},
        'linen': {'bg': '#f0ebe4', 'text': '#1a1714'},
        'sage': {'bg': '#e8ede8', 'text': '#1a1714'},
        'blush': {'bg': '#f5ece8', 'text': '#1a1714'},
    }
    return render_template('dashboard/index.html', clients=clients, colour_map=colour_map)


@dashboard_bp.route('/card/new', methods=['GET', 'POST'])
@login_required
def card_new():
    form = CardForm()
    if form.validate_on_submit():
        brand_name = form.brand_name.data.strip()
        tagline = form.tagline.data.strip() if form.tagline.data else ''
        slug = unique_slug(brand_name)

        logo_filename = ''
        if form.logo.data:
            logo_filename = save_logo(form.logo.data)

        card_style = request.form.get('card_style', 'oxblood')

        client = Client(
            user_id=current_user.id,
            brand_name=brand_name,
            tagline=tagline,
            slug=slug,
            logo_filename=logo_filename,
            card_style=card_style,
        )
        db.session.add(client)
        db.session.flush()

        links_data = json.loads(request.form.get('links', '[]'))
        for i, link_data in enumerate(links_data):
            link = Link(
                client_id=client.id,
                platform=link_data.get('platform', 'custom'),
                url=link_data.get('url', ''),
                display_order=i,
            )
            db.session.add(link)

        db.session.commit()

        site_url = current_app.config['SITE_URL']
        generate_assets(slug, brand_name, tagline, site_url, logo_filename=logo_filename, card_style=card_style)

        flash('Card created successfully!', 'success')
        return redirect(url_for('dashboard.card_view', id=client.id))

    return render_template('dashboard/card_new.html', form=form)


@dashboard_bp.route('/card/<int:id>')
@login_required
def card_view(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    return render_template('dashboard/card_view.html', client=client, links=links)


@dashboard_bp.route('/card/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def card_edit(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CardForm(obj=client)

    if form.validate_on_submit():
        brand_name = form.brand_name.data.strip()
        client.brand_name = brand_name
        client.tagline = form.tagline.data.strip() if form.tagline.data else ''
        client.card_style = request.form.get('card_style', client.card_style)

        if form.logo.data:
            client.logo_filename = save_logo(form.logo.data)

        Link.query.filter_by(client_id=client.id).delete()

        links_data = json.loads(request.form.get('links', '[]'))
        for i, link_data in enumerate(links_data):
            link = Link(
                client_id=client.id,
                platform=link_data.get('platform', 'custom'),
                url=link_data.get('url', ''),
                display_order=i,
            )
            db.session.add(link)

        db.session.commit()

        site_url = current_app.config['SITE_URL']
        generate_assets(client.slug, brand_name, client.tagline, site_url, logo_filename=client.logo_filename, card_style=client.card_style)

        flash('Card updated successfully!', 'success')
        return redirect(url_for('dashboard.card_view', id=client.id))

    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    colour_map = {
        'oxblood': {'bg_hex': '#6b1f2a', 'light': False},
        'navy':    {'bg_hex': '#1a2744', 'light': False},
        'forest':  {'bg_hex': '#1a3d2b', 'light': False},
        'slate':   {'bg_hex': '#2d3748', 'light': False},
        'charcoal':{'bg_hex': '#1a1714', 'light': False},
        'linen':   {'bg_hex': '#f0ebe4', 'light': True},
        'sage':    {'bg_hex': '#e8ede8', 'light': True},
        'blush':   {'bg_hex': '#f5ece8', 'light': True},
    }
    return render_template('dashboard/card_edit.html', form=form, client=client, links=links, colour_map=colour_map)


@dashboard_bp.route('/card/<int:id>/delete', methods=['POST'])
@login_required
def card_delete(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    order_count = Order.query.filter_by(client_id=client.id).count()
    if order_count > 0:
        flash('This card has existing orders and cannot be deleted.', 'error')
        return redirect(url_for('dashboard.card_view', id=client.id))
    db.session.delete(client)
    db.session.commit()
    flash('Card deleted.', 'success')
    return redirect(url_for('dashboard.index'))


@dashboard_bp.route('/card/<int:id>/order')
@login_required
def card_order(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    tiers = [
        {
            'key': 'digital',
            'name': 'Digital',
            'price': '£19',
            'description': 'QR code + print-ready PDF. No physical cards.',
            'includes': ['Hosted links page', 'QR code download', 'Print-ready PDF (85×55mm)'],
            'quantity': None,
        },
        {
            'key': 'standard',
            'name': 'Standard',
            'price': '£59',
            'description': '250 printed cards delivered to your door.',
            'includes': ['Everything in Digital', '250 printed cards', 'Matt laminate finish', 'Delivered in 5–7 days'],
            'quantity': 250,
        },
        {
            'key': 'premium',
            'name': 'Premium',
            'price': '£85',
            'description': '500 printed cards delivered to your door.',
            'includes': ['Everything in Digital', '500 printed cards', 'Matt laminate finish', 'Delivered in 5–7 days'],
            'quantity': 500,
        },
    ]
    return render_template('dashboard/card_order.html', client=client, tiers=tiers)


@dashboard_bp.route('/orders')
@login_required
def orders():
    all_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('dashboard/orders.html', orders=all_orders)


@dashboard_bp.route('/card/<int:id>/download/pdf')
@login_required
def download_pdf(id):
    import os
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    has_paid = Order.query.filter_by(
        client_id=client.id,
        user_id=current_user.id
    ).filter(Order.status != 'pending').first()
    if not has_paid:
        flash('Purchase a plan to download your PDF.', 'info')
        return redirect(url_for('dashboard.card_order', id=client.id))
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    return redirect(f"{public_url}/generated/{client.slug}/card.pdf")


@dashboard_bp.route('/card/<int:id>/download/qr')
@login_required
def download_qr(id):
    import os
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    has_paid = Order.query.filter_by(
        client_id=client.id,
        user_id=current_user.id
    ).filter(Order.status != 'pending').first()
    if not has_paid:
        flash('Purchase a plan to download your QR code.', 'info')
        return redirect(url_for('dashboard.card_order', id=client.id))
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    return redirect(f"{public_url}/generated/{client.slug}/qr.png")
