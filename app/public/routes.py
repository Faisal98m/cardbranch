from flask import Blueprint, render_template, abort, make_response, flash, redirect, url_for, current_app
from flask_login import current_user
from app import limiter
from app.models import Client, db
from app.services.links import build_href, should_open_new_tab
from app.services.themes import resolve_design, design_css, card_colour_options, card_border_options, card_font_options
from app.public.forms import ContactForm

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    return render_template(
        'public/index.html',
        card_colour_options=card_colour_options(),
        card_border_options=card_border_options(),
        card_font_options=card_font_options(),
    )


@public_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if form.website.data:
            flash('Thank you for your message. We will be in touch soon.', 'success')
            return redirect(url_for('public.contact'))

        from app.services.email import send_contact_email
        try:
            send_contact_email(
                name=form.name.data,
                email=form.email.data,
                message=form.message.data
            )
            flash('Thank you for your message. We will be in touch soon.', 'success')
        except Exception as e:
            current_app.logger.error(f"Contact form email failed: {e}")
            flash('Something went wrong sending your message. Please email admin@cardbranch.co.uk directly.', 'error')
        return redirect(url_for('public.contact'))

    return render_template('public/contact.html', form=form)


@public_bp.route('/c/<slug>')
def card_links(slug):
    client = Client.query.filter_by(slug=slug).first_or_404()
    is_owner = current_user.is_authenticated and current_user.id == client.user_id
    design = resolve_design(
        card_colour=client.card_colour,
        card_border=client.card_border,
        card_font=client.card_font,
    )
    theme = design_css(design)
    theme['colour_key'] = design['colour_key']
    if not client.is_published:
        if is_owner:
            return render_template('public/links.html', client=client, links=client.links.order_by('display_order').all(),
                                   build_href=build_href, should_open_new_tab=should_open_new_tab,
                                   preview_mode=True, theme=theme)
        abort(404)
    return render_template('public/links.html', client=client, links=client.links.order_by('display_order').all(),
                           build_href=build_href, should_open_new_tab=should_open_new_tab,
                           preview_mode=False, theme=theme)


@public_bp.route('/robots.txt')
def robots():
    resp = make_response("User-agent: *\nAllow: /\n\nSitemap: https://www.cardbranch.co.uk/sitemap.xml\n")
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


@public_bp.route('/sitemap.xml')
def sitemap():
    published = Client.query.filter_by(is_published=True).all()
    urls = ['https://www.cardbranch.co.uk/']
    for c in published:
        urls.append(f'https://www.cardbranch.co.uk/c/{c.slug}')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>{url}</loc></url>\n'
    xml += '</urlset>'
    resp = make_response(xml)
    resp.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return resp
