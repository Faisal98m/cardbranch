import json
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Client, Link, Order, db
from app.dashboard.forms import CardForm, LinkForm
from app.services.generator import unique_slug, save_logo, generate_assets
from app.services.themes import resolve_design, design_css, card_colour_options, card_border_options, card_font_options, SELECTABLE_COLOUR_KEYS, SELECTABLE_BORDER_KEYS, SELECTABLE_FONT_KEYS
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
    design_map = {}
    for c in clients:
        d = resolve_design(c.card_colour, c.card_border, c.card_font, legacy_card_style=c.card_style)
        design_map[c.id] = design_css(d)
    return render_template('dashboard/index.html', clients=clients, design_map=design_map)


@dashboard_bp.route('/card/new', methods=['GET', 'POST'])
@login_required
def card_new():
    form = CardForm()

    default_colour = 'oxblood'
    default_border = 'keyline'
    default_font = SELECTABLE_FONT_KEYS[0]

    submitted_colour = request.form.get('card_colour') if request.method == 'POST' else None
    submitted_border = request.form.get('card_border') if request.method == 'POST' else None
    submitted_font = request.form.get('card_font') if request.method == 'POST' else None

    seed_colour = submitted_colour if submitted_colour in SELECTABLE_COLOUR_KEYS else default_colour
    seed_border = submitted_border if submitted_border in SELECTABLE_BORDER_KEYS else default_border
    seed_font = submitted_font if submitted_font in SELECTABLE_FONT_KEYS else default_font

    if form.validate_on_submit():
        card_colour = request.form.get('card_colour')
        card_border = request.form.get('card_border')
        card_font = request.form.get('card_font')

        errors = {}
        if card_colour not in SELECTABLE_COLOUR_KEYS:
            errors['colour'] = card_colour
        if card_border not in SELECTABLE_BORDER_KEYS:
            errors['border'] = card_border
        if card_font not in SELECTABLE_FONT_KEYS:
            errors['font'] = card_font

        if errors:
            invalid_names = ', '.join(errors.keys())
            flash(f'Invalid card design value(s) for: {invalid_names}', 'error')
            return render_template('dashboard/card_new.html', form=form, seed_colour=seed_colour, seed_border=seed_border, seed_font=seed_font), 400

        brand_name = form.brand_name.data.strip()
        tagline = form.tagline.data.strip() if form.tagline.data else ''
        slug = unique_slug(brand_name)

        logo_filename = ''
        if form.logo.data:
            try:
                logo_filename = save_logo(form.logo.data)
            except ValueError as e:
                flash(str(e), 'error')
                return render_template('dashboard/card_new.html', form=form, seed_colour=card_colour, seed_border=card_border, seed_font=card_font)

        client = Client(
            user_id=current_user.id,
            brand_name=brand_name,
            tagline=tagline,
            slug=slug,
            logo_filename=logo_filename,
            card_colour=card_colour,
            card_border=card_border,
            card_font=card_font,
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
                return render_template('dashboard/card_new.html', form=form, seed_colour=card_colour, seed_border=card_border, seed_font=card_font)
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

    return render_template('dashboard/card_new.html', form=form, seed_colour=seed_colour, seed_border=seed_border, seed_font=seed_font)


@dashboard_bp.route('/card/<int:id>')
@login_required
def card_view(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    design = resolve_design(
        client.card_colour,
        client.card_border,
        client.card_font,
        legacy_card_style=client.card_style,
    )
    theme = design_css(design)
    theme['layout'] = {
        'none': 'minimal',
        'keyline': 'framed',
        'corner_marks': 'corner_brackets',
        'split_edge': 'split_edge',
        'top_bottom_rule': 'top_bottom_rule',
    }[design['border_renderer']]
    return render_template('dashboard/card_view.html', client=client, links=links, theme=theme)


@dashboard_bp.route('/card/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def card_edit(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CardForm(obj=client)

    design = resolve_design(
        client.card_colour,
        client.card_border,
        client.card_font,
        legacy_card_style=client.card_style,
    )
    current_preview = design_css(design)
    current_preview['colour_key'] = design['colour_key']
    current_preview['border_key'] = design['border_key']
    current_preview['font_key'] = design['font_key']

    def _seed_if_valid(value, allowed, default):
        return value if value in allowed else default

    seed_colour = _seed_if_valid(design['colour_key'], SELECTABLE_COLOUR_KEYS, 'oxblood')
    seed_border = _seed_if_valid(design['border_key'], SELECTABLE_BORDER_KEYS, 'keyline')
    seed_font = _seed_if_valid(design['font_key'], SELECTABLE_FONT_KEYS, SELECTABLE_FONT_KEYS[0])

    if form.validate_on_submit():
        card_colour = request.form.get('card_colour')
        card_border = request.form.get('card_border')
        card_font = request.form.get('card_font')

        errors = {}
        if card_colour not in SELECTABLE_COLOUR_KEYS:
            errors['colour'] = card_colour
        if card_border not in SELECTABLE_BORDER_KEYS:
            errors['border'] = card_border
        if card_font not in SELECTABLE_FONT_KEYS:
            errors['font'] = card_font

        if errors:
            invalid_names = ', '.join(errors.keys())
            flash(f'Invalid card design value(s) for: {invalid_names}', 'error')
            links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
            re_seed_colour = card_colour if card_colour in SELECTABLE_COLOUR_KEYS else seed_colour
            re_seed_border = card_border if card_border in SELECTABLE_BORDER_KEYS else seed_border
            re_seed_font = card_font if card_font in SELECTABLE_FONT_KEYS else seed_font
            return render_template('dashboard/card_edit.html', form=form, client=client, links=links, current_preview=current_preview, card_colour_options=card_colour_options(), card_border_options=card_border_options(), card_font_options=card_font_options(), selectable_colour_keys=SELECTABLE_COLOUR_KEYS, selectable_border_keys=SELECTABLE_BORDER_KEYS, selectable_font_keys=SELECTABLE_FONT_KEYS, seed_colour=re_seed_colour, seed_border=re_seed_border, seed_font=re_seed_font), 400

        brand_name = form.brand_name.data.strip()
        client.brand_name = brand_name
        client.tagline = form.tagline.data.strip() if form.tagline.data else ''

        client.card_colour = card_colour
        client.card_border = card_border
        client.card_font = card_font

        submitted_seed_colour = card_colour
        submitted_seed_border = card_border
        submitted_seed_font = card_font

        if form.logo.data:
            try:
                client.logo_filename = save_logo(form.logo.data)
            except ValueError as e:
                flash(str(e), 'error')
                links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
                return render_template('dashboard/card_edit.html', form=form, client=client, links=links, current_preview=current_preview, card_colour_options=card_colour_options(), card_border_options=card_border_options(), card_font_options=card_font_options(), selectable_colour_keys=SELECTABLE_COLOUR_KEYS, selectable_border_keys=SELECTABLE_BORDER_KEYS, selectable_font_keys=SELECTABLE_FONT_KEYS, seed_colour=submitted_seed_colour, seed_border=submitted_seed_border, seed_font=submitted_seed_font)

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
                client.pdf_r2_key = generate_assets(client.slug, client.brand_name, client.tagline, site_url, logo_filename=client.logo_filename, card_colour=client.card_colour, card_border=client.card_border, card_font=client.card_font)
                db.session.commit()

            flash('Card updated successfully!', 'success')
            return redirect(url_for('dashboard.card_view', id=client.id))

    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    return render_template('dashboard/card_edit.html', form=form, client=client, links=links, current_preview=current_preview, card_colour_options=card_colour_options(), card_border_options=card_border_options(), card_font_options=card_font_options(), selectable_colour_keys=SELECTABLE_COLOUR_KEYS, selectable_border_keys=SELECTABLE_BORDER_KEYS, selectable_font_keys=SELECTABLE_FONT_KEYS, seed_colour=seed_colour, seed_border=seed_border, seed_font=seed_font)


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
