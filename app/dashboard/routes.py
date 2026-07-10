import json
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Client, Link, Order, db
from app.dashboard.forms import CardForm, LinkForm
from app.services.generator import unique_slug, save_logo, generate_assets
from app.services.links import normalize_uk_phone

dashboard_bp = Blueprint('dashboard', __name__)

LINK_TYPE_LABELS = {
    'website': 'Website',
    'phone': 'Call',
    'whatsapp': 'WhatsApp',
    'email': 'Email',
    'instagram': 'Instagram',
    'tiktok': 'TikTok',
    'linkedin': 'LinkedIn',
    'custom': 'Link',
}


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
            try:
                logo_filename = save_logo(form.logo.data)
            except ValueError as e:
                flash(str(e), 'error')
                return render_template('dashboard/card_new.html', form=form)

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
            link_type = link_data.get('link_type', 'custom')
            value = link_data.get('url', '').strip()
            if link_type in ('phone', 'whatsapp') and value and not normalize_uk_phone(value):
                db.session.rollback()
                flash(f'"{value}" is not a valid UK phone number. Use a format like 07400 123456 or +447400123456.', 'error')
                return render_template('dashboard/card_new.html', form=form)
            link = Link(
                client_id=client.id,
                platform=LINK_TYPE_LABELS.get(link_type, 'Link'),
                link_type=link_type,
                url=value,
                display_order=i,
            )
            db.session.add(link)

        db.session.commit()

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
            try:
                client.logo_filename = save_logo(form.logo.data)
            except ValueError as e:
                flash(str(e), 'error')
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

        Link.query.filter_by(client_id=client.id).delete()

        links_data = json.loads(request.form.get('links', '[]'))
        for i, link_data in enumerate(links_data):
            link_type = link_data.get('link_type', 'custom')
            value = link_data.get('url', '').strip()
            if link_type in ('phone', 'whatsapp') and value and not normalize_uk_phone(value):
                db.session.rollback()
                flash(f'"{value}" is not a valid UK phone number. Use a format like 07400 123456 or +447400123456.', 'error')
                break
            link = Link(
                client_id=client.id,
                platform=LINK_TYPE_LABELS.get(link_type, 'Link'),
                link_type=link_type,
                url=value,
                display_order=i,
            )
            db.session.add(link)
        else:
            db.session.commit()

            if client.is_published:
                site_url = current_app.config['SITE_URL']
                client.pdf_r2_key = generate_assets(client.slug, client.brand_name, client.tagline, site_url, logo_filename=client.logo_filename, card_style=client.card_style)
                db.session.commit()

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
        return redirect(url_for('checkout.order', id=client.id))
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    pdf_key = client.pdf_r2_key or f'generated/{client.slug}/card.pdf'
    return redirect(f"{public_url}/{pdf_key}")


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
        return redirect(url_for('checkout.order', id=client.id))
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    return redirect(f"{public_url}/generated/{client.slug}/qr.png")
