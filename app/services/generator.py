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


def download_logo(logo_filename):
    import boto3
    from botocore.config import Config
    if not logo_filename:
        return None
    try:
        client = boto3.client(
            's3',
            endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
            aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY'],
            config=Config(signature_version='s3v4'),
            region_name='auto',
        )
        ext = logo_filename.rsplit('.', 1)[-1].lower() if '.' in logo_filename else 'png'
        tmp_path = f'/tmp/logo_{uuid.uuid4().hex}.{ext}'
        client.download_file(os.environ['R2_BUCKET_NAME'], logo_filename, tmp_path)
        return tmp_path
    except Exception:
        return None


def generate_pdf(slug, brand_name, tagline, site_url, logo_path=None):
    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    card_w = 85 * mm_unit
    card_h = 55 * mm_unit
    pdf_path = f'/tmp/{slug}_card.pdf'
    qr_img_path = f'/tmp/{slug}_qr.png'

    candidate_dirs = [
        os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'fonts'),
        os.path.join(os.path.dirname(__file__), '..', 'static', 'fonts'),
        os.path.join(os.getcwd(), 'static', 'fonts'),
    ]
    fonts_dir = None
    for d in candidate_dirs:
        d = os.path.abspath(d)
        if os.path.exists(os.path.join(d, 'PlayfairDisplaySC-Bold.ttf')):
            fonts_dir = d
            break

    name_font = 'Helvetica-Bold'
    tag_font = 'Helvetica'
    if fonts_dir:
        try:
            pdfmetrics.registerFont(TTFont('PlayfairBold', os.path.join(fonts_dir, 'PlayfairDisplaySC-Bold.ttf')))
            pdfmetrics.registerFont(TTFont('PlayfairRegular', os.path.join(fonts_dir, 'PlayfairDisplaySC-Regular.ttf')))
            name_font = 'PlayfairBold'
            tag_font = 'PlayfairRegular'
        except Exception:
            pass

    c = canvas.Canvas(pdf_path, pagesize=(card_w, card_h))

    oxblood = (0.420, 0.122, 0.165)
    linen = (0.941, 0.922, 0.894)
    off_white = (0.980, 0.973, 0.957)

    has_tagline = bool(tagline and tagline.strip())
    initial = brand_name[0].upper() if brand_name else 'B'

    def draw_front():
        c.setFillColorRGB(*oxblood)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        if has_tagline:
            # A1 layout — logo box, name, divider, tagline — vertically centred as a group
            logo_box_size = 12 * mm_unit
            gap_logo_name = 5 * mm_unit
            name_h = 5 * mm_unit
            gap_name_div = 4 * mm_unit
            gap_div_tag = 4 * mm_unit
            tag_h = 2 * mm_unit
            group_h = logo_box_size + gap_logo_name + name_h + gap_name_div + tag_h
            group_y_start = (card_h / 2) + (group_h / 2)

            logo_box_x = (card_w - logo_box_size) / 2
            logo_box_y = group_y_start - logo_box_size

            # Logo border box
            c.setStrokeColorRGB(*off_white)
            c.setLineWidth(0.35)
            c.setFillColorRGB(*oxblood)
            c.roundRect(logo_box_x, logo_box_y, logo_box_size, logo_box_size, 1.2 * mm_unit, fill=1, stroke=1)

            # Logo or initial inside box
            if logo_path and os.path.exists(logo_path):
                padding = 1.5 * mm_unit
                c.drawImage(
                    logo_path,
                    logo_box_x + padding,
                    logo_box_y + padding,
                    width=logo_box_size - 2 * padding,
                    height=logo_box_size - 2 * padding,
                    mask='auto' if logo_path.endswith('.png') else None,
                    preserveAspectRatio=True
                )
            else:
                c.setFillColorRGB(*off_white)
                c.setFont(name_font, 9)
                c.drawCentredString(
                    logo_box_x + logo_box_size / 2,
                    logo_box_y + logo_box_size / 2 - 3,
                    initial
                )

            # Brand name
            name_y = logo_box_y - 6 * mm_unit
            c.setFillColorRGB(*off_white)
            c.setFont(name_font, 13)
            c.drawCentredString(card_w / 2, name_y, brand_name)

            # Divider
            divider_w = 10 * mm_unit
            divider_y = name_y - 3.5 * mm_unit
            c.setStrokeColorRGB(0.980, 0.973, 0.957)
            c.setLineWidth(0.25)
            c.line(card_w / 2 - divider_w / 2, divider_y, card_w / 2 + divider_w / 2, divider_y)

            # Tagline
            c.setFillColorRGB(0.980, 0.973, 0.957)
            c.setFont(tag_font, 5.5)
            c.drawCentredString(card_w / 2, divider_y - 3.5 * mm_unit, tagline.upper())

        else:
            # A3 layout — large logo box centred, brand name small below
            logo_box_size = 18 * mm_unit
            logo_box_x = (card_w - logo_box_size) / 2
            logo_box_y = (card_h - logo_box_size) / 2 + 3 * mm_unit

            c.setStrokeColorRGB(*off_white)
            c.setLineWidth(0.35)
            c.setFillColorRGB(*oxblood)
            c.roundRect(logo_box_x, logo_box_y, logo_box_size, logo_box_size, 2 * mm_unit, fill=1, stroke=1)

            if logo_path and os.path.exists(logo_path):
                padding = 2 * mm_unit
                c.drawImage(
                    logo_path,
                    logo_box_x + padding,
                    logo_box_y + padding,
                    width=logo_box_size - 2 * padding,
                    height=logo_box_size - 2 * padding,
                    mask='auto' if logo_path.endswith('.png') else None,
                    preserveAspectRatio=True
                )
            else:
                c.setFillColorRGB(*off_white)
                c.setFont(name_font, 14)
                c.drawCentredString(
                    logo_box_x + logo_box_size / 2,
                    logo_box_y + logo_box_size / 2 - 5,
                    initial
                )

            c.setFillColorRGB(*off_white)
            c.setFont(tag_font, 6.5)
            c.drawCentredString(card_w / 2, logo_box_y - 4.5 * mm_unit, brand_name.upper())

    def draw_back():
        c.setFillColorRGB(*linen)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        if os.path.exists(qr_img_path):
            qr_size = 32 * mm_unit
            qr_x = round((card_w - qr_size) / 2)
            qr_y = round((card_h - qr_size) / 2)
            c.drawImage(qr_img_path, qr_x, qr_y, width=qr_size, height=qr_size)

    draw_front()
    c.showPage()
    draw_back()
    c.save()

    upload_file(pdf_path, f'generated/{slug}/card.pdf')
    return pdf_path


def generate_assets(slug, brand_name, tagline, site_url, logo_filename=None):
    qr_tmp = generate_qr(slug, site_url)
    logo_tmp = download_logo(logo_filename)
    pdf_tmp = generate_pdf(slug, brand_name, tagline, site_url, logo_path=logo_tmp)
    if os.path.exists(qr_tmp):
        os.remove(qr_tmp)
    if pdf_tmp and os.path.exists(pdf_tmp):
        os.remove(pdf_tmp)
    if logo_tmp and os.path.exists(logo_tmp):
        os.remove(logo_tmp)
