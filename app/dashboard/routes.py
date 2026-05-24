import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from app.models import Client, Link, Order, db
from app.dashboard.forms import CardForm, LinkForm
from app.services.generator import unique_slug, save_logo, generate_assets
from app.services.email import send_order_confirmation

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.created_at.desc()).all()
    return render_template('dashboard/index.html', clients=clients)


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

        client = Client(
            user_id=current_user.id,
            brand_name=brand_name,
            tagline=tagline,
            slug=slug,
            logo_filename=logo_filename,
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
        generate_assets(slug, brand_name, tagline, site_url)

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
        generate_assets(client.slug, brand_name, client.tagline, site_url)

        flash('Card updated successfully!', 'success')
        return redirect(url_for('dashboard.card_view', id=client.id))

    links = Link.query.filter_by(client_id=client.id).order_by(Link.display_order).all()
    return render_template('dashboard/card_edit.html', form=form, client=client, links=links)


@dashboard_bp.route('/orders')
@login_required
def orders():
    all_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('dashboard/orders.html', orders=all_orders)


@dashboard_bp.route('/card/<int:id>/download/pdf')
@login_required
def download_pdf(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return send_from_directory(
        current_app.config['GENERATED_FOLDER'],
        f'{client.slug}/card.pdf',
        as_attachment=True,
        download_name=f'{client.slug}-card.pdf'
    )


@dashboard_bp.route('/card/<int:id>/download/qr')
@login_required
def download_qr(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return send_from_directory(
        current_app.config['GENERATED_FOLDER'],
        f'{client.slug}/qr.png',
        as_attachment=True,
        download_name=f'{client.slug}-qr.png'
    )
