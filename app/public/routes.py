from flask import Blueprint, render_template, abort
from app.models import Client

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    return render_template('public/index.html')


@public_bp.route('/c/<slug>')
def card_links(slug):
    client = Client.query.filter_by(slug=slug).first_or_404()
    links = client.links.order_by('display_order').all()
    return render_template('public/links.html', client=client, links=links)
