import os
import uuid
import re
import qrcode
from flask import current_app
from reportlab.lib.pagesizes import mm
from reportlab.lib.units import mm as mm_unit
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image


def slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug or 'brand'


def unique_slug(brand_name):
    from app.models import Client
    base = slugify(brand_name)
    slug = base
    counter = 2
    while Client.query.filter_by(slug=slug).first():
        slug = f'{base}-{counter}'
        counter += 1
    return slug


def save_logo(file):
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'png'
    filename = f'{uuid.uuid4().hex}.{ext}'
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(uploads_dir, exist_ok=True)
    filepath = os.path.join(uploads_dir, filename)
    file.save(filepath)
    return filename


def generate_qr(slug, site_url):
    gen_dir = os.path.join(current_app.static_folder, 'generated')
    os.makedirs(gen_dir, exist_ok=True)
    output_dir = os.path.join(gen_dir, slug)
    os.makedirs(output_dir, exist_ok=True)

    url = f'{site_url.rstrip("/")}/c/{slug}'
    qr = qrcode.make(url)
    qr_path = os.path.join(output_dir, 'qr.png')
    qr.save(qr_path)
    return qr_path


def generate_pdf(slug, brand_name, tagline, site_url, logo_path=None):
    gen_dir = os.path.join(current_app.static_folder, 'generated')
    os.makedirs(gen_dir, exist_ok=True)
    output_dir = os.path.join(gen_dir, slug)
    os.makedirs(output_dir, exist_ok=True)

    card_w = 85 * mm_unit
    card_h = 55 * mm_unit
    pdf_path = os.path.join(output_dir, 'card.pdf')

    c = canvas.Canvas(pdf_path, pagesize=(card_w, card_h))

    gold = (0.788, 0.663, 0.431)
    silver = (0.753, 0.753, 0.753)
    cream = (0.941, 0.925, 0.894)
    dark_bg = (0.043, 0.043, 0.043)
    grey = (0.5, 0.5, 0.5)

    def draw_front():
        c.setFillColor(dark_bg)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        words = brand_name.split()
        first_word = words[0] if words else brand_name

        if len(first_word) >= 2:
            first_letter = first_word[0]
            rest_first = first_word[1:]
            rest_name = ' '.join(words[1:])

            c.setFillColor(gold)
            c.setFont('Helvetica-Bold', 18)
            c.drawString(10 * mm_unit, card_h - 15 * mm_unit, first_letter)

            x_offset = 10 * mm_unit + c.stringWidth(first_letter, 'Helvetica-Bold', 18)
            c.setFillColor(silver)
            c.drawString(x_offset, card_h - 15 * mm_unit, rest_first)

            if rest_name:
                c.drawString(10 * mm_unit, card_h - 22 * mm_unit, rest_name)
        else:
            c.setFillColor(gold)
            c.setFont('Helvetica-Bold', 18)
            c.drawString(10 * mm_unit, card_h - 15 * mm_unit, brand_name)

        if tagline:
            c.setFillColor(gold)
            c.setFont('Helvetica', 8)
            c.drawString(10 * mm_unit, card_h - 28 * mm_unit, tagline)

        c.setStrokeColor(gold)
        c.setLineWidth(0.5)
        c.line(10 * mm_unit, 8 * mm_unit, card_w - 10 * mm_unit, 8 * mm_unit)

        qr_img_path = os.path.join(output_dir, 'qr.png')
        if os.path.exists(qr_img_path):
            c.setFillColor(cream)
            qr_box_x = card_w - 32 * mm_unit
            qr_box_y = card_h - 38 * mm_unit
            qr_box_size = 26 * mm_unit
            c.rect(qr_box_x, qr_box_y, qr_box_size, qr_box_size, fill=1, stroke=0)

            c.drawImage(qr_img_path,
                        qr_box_x + 2 * mm_unit,
                        qr_box_y + 2 * mm_unit,
                        width=22 * mm_unit, height=22 * mm_unit)

            c.setFillColor(gold)
            c.setFont('Helvetica', 5)
            c.drawCentredString(qr_box_x + qr_box_size / 2, qr_box_y - 2 * mm_unit, 'SCAN TO CONNECT')

    def draw_back():
        c.setFillColor(dark_bg)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        c.setFillColor(gold)
        c.setFont('Helvetica-Bold', 14)
        c.drawString(10 * mm_unit, card_h - 15 * mm_unit, brand_name)

        if tagline:
            c.setFillColor(grey)
            c.setFont('Helvetica', 7)
            c.drawString(10 * mm_unit, card_h - 22 * mm_unit, tagline)

        url = f'{site_url.rstrip("/")}/c/{slug}'
        c.setFillColor(gold)
        c.setFont('Helvetica', 6)
        c.drawString(10 * mm_unit, card_h - 30 * mm_unit, url)

        qr_img_path = os.path.join(output_dir, 'qr.png')
        if os.path.exists(qr_img_path):
            qr_size = 30 * mm_unit
            qr_x = card_w - qr_size - 10 * mm_unit
            qr_y = (card_h - qr_size) / 2
            c.drawImage(qr_img_path, qr_x, qr_y, width=qr_size, height=qr_size)

    draw_front()
    c.showPage()
    draw_back()
    c.save()
    return pdf_path


def generate_assets(slug, brand_name, tagline, site_url):
    qr_path = generate_qr(slug, site_url)
    pdf_path = generate_pdf(slug, brand_name, tagline, site_url)
    return qr_path, pdf_path
