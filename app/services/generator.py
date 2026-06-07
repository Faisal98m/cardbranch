import os
import uuid
import re
import qrcode
from reportlab.lib.pagesizes import mm
from reportlab.lib.units import mm as mm_unit
from reportlab.pdfgen import canvas
from app.services.r2 import upload_file


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
    tmp_path = f'/tmp/{filename}'
    file.save(tmp_path)
    r2_key = f'uploads/{filename}'
    upload_file(tmp_path, r2_key)
    os.remove(tmp_path)
    return r2_key


def generate_qr(slug, site_url):
    url = f'{site_url.rstrip("/")}/c/{slug}'
    qr = qrcode.make(url)
    tmp_path = f'/tmp/{slug}_qr.png'
    qr.save(tmp_path)
    r2_key = f'generated/{slug}/qr.png'
    upload_file(tmp_path, r2_key)
    return tmp_path


def generate_pdf(slug, brand_name, tagline, site_url, logo_path=None):
    card_w = 85 * mm_unit
    card_h = 55 * mm_unit
    pdf_path = f'/tmp/{slug}_card.pdf'
    qr_img_path = f'/tmp/{slug}_qr.png'

    c = canvas.Canvas(pdf_path, pagesize=(card_w, card_h))

    oxblood = (0.420, 0.122, 0.165)
    linen = (0.941, 0.922, 0.894)
    linen_dark = (0.859, 0.839, 0.808)
    off_white = (0.980, 0.973, 0.957)
    off_white_dim = (0.980, 0.973, 0.957, 0.45)

    has_tagline = bool(tagline and tagline.strip())
    initial = brand_name[0].upper() if brand_name else 'B'

    def draw_front():
        # Full oxblood background
        c.setFillColorRGB(*oxblood)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        if has_tagline:
            # A1 layout — centred logo box, name, divider, tagline
            logo_box_size = 14 * mm_unit
            logo_box_x = (card_w - logo_box_size) / 2
            logo_box_y = card_h - 18 * mm_unit

            # Logo border box
            c.setStrokeColorRGB(0.980, 0.973, 0.957)
            c.setLineWidth(0.4)
            c.setFillColorRGB(*oxblood)
            c.roundRect(logo_box_x, logo_box_y, logo_box_size, logo_box_size, 1.5 * mm_unit, fill=1, stroke=1)

            # Initial inside box
            c.setFillColorRGB(0.980, 0.973, 0.957)
            c.setFont('Helvetica', 11)
            c.drawCentredString(
                logo_box_x + logo_box_size / 2,
                logo_box_y + logo_box_size / 2 - 4,
                initial
            )

            # Brand name
            c.setFillColorRGB(0.980, 0.973, 0.957)
            c.setFont('Helvetica', 12)
            name_y = logo_box_y - 6 * mm_unit
            c.drawCentredString(card_w / 2, name_y, brand_name)

            # Divider line
            divider_w = 12 * mm_unit
            divider_y = name_y - 3 * mm_unit
            c.setStrokeColorRGB(0.980, 0.973, 0.957)
            c.setLineWidth(0.3)
            c.line(
                card_w / 2 - divider_w / 2, divider_y,
                card_w / 2 + divider_w / 2, divider_y
            )

            # Tagline
            c.setFillColorRGB(0.980, 0.973, 0.957)
            c.setFont('Helvetica', 6)
            c.drawCentredString(card_w / 2, divider_y - 3.5 * mm_unit, tagline.upper())

        else:
            # A3 layout — large logo box centred, brand name small below
            logo_box_size = 20 * mm_unit
            logo_box_x = (card_w - logo_box_size) / 2
            logo_box_y = (card_h - logo_box_size) / 2 + 4 * mm_unit

            # Logo border box
            c.setStrokeColorRGB(0.980, 0.973, 0.957)
            c.setLineWidth(0.4)
            c.setFillColorRGB(*oxblood)
            c.roundRect(logo_box_x, logo_box_y, logo_box_size, logo_box_size, 2 * mm_unit, fill=1, stroke=1)

            # Initial inside box — larger
            c.setFillColorRGB(0.980, 0.973, 0.957)
            c.setFont('Helvetica', 16)
            c.drawCentredString(
                logo_box_x + logo_box_size / 2,
                logo_box_y + logo_box_size / 2 - 5,
                initial
            )

            # Brand name small below
            c.setFillColorRGB(0.980, 0.973, 0.957)
            c.setFont('Helvetica', 7)
            name_y = logo_box_y - 5 * mm_unit
            c.drawCentredString(card_w / 2, name_y, brand_name.upper())

    def draw_back():
        # Linen background
        c.setFillColorRGB(*linen)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        # QR code centred
        if os.path.exists(qr_img_path):
            qr_size = 28 * mm_unit
            qr_x = (card_w - qr_size) / 2
            qr_y = (card_h - qr_size) / 2
            c.drawImage(qr_img_path, qr_x, qr_y, width=qr_size, height=qr_size, mask='auto')

    draw_front()
    c.showPage()
    draw_back()
    c.save()

    upload_file(pdf_path, f'generated/{slug}/card.pdf')
    return pdf_path


def generate_assets(slug, brand_name, tagline, site_url):
    qr_tmp = generate_qr(slug, site_url)
    pdf_tmp = generate_pdf(slug, brand_name, tagline, site_url)
    if os.path.exists(qr_tmp):
        os.remove(qr_tmp)
    if os.path.exists(pdf_tmp):
        os.remove(pdf_tmp)
