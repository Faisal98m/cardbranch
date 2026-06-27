from flask import Blueprint, render_template, abort, make_response
from app.models import Client, db

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    return render_template('public/index.html')


@public_bp.route('/c/<slug>')
def card_links(slug):
    client = Client.query.filter_by(slug=slug).first_or_404()
    links = client.links.order_by('display_order').all()
    return render_template('public/links.html', client=client, links=links)


@public_bp.route('/robots.txt')
def robots():
    resp = make_response("User-agent: *\nAllow: /\n\nSitemap: https://www.cardbranch.co.uk/sitemap.xml\n")
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


@public_bp.route('/sitemap.xml')
def sitemap():
    clients = Client.query.with_entities(Client.slug).all()
    urls = ['https://www.cardbranch.co.uk/']
    for (slug,) in clients:
        urls.append(f'https://www.cardbranch.co.uk/c/{slug}')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>{url}</loc></url>\n'
    xml += '</urlset>'
    resp = make_response(xml)
    resp.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return resp
