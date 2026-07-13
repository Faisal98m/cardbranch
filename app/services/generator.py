import os
import uuid
import re
import secrets
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import mm
from reportlab.lib.units import mm as mm_unit
from reportlab.pdfgen import canvas
from app.services.r2 import upload_file
from app.services.themes import resolve_design



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
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    MAX_SIZE = 2 * 1024 * 1024

    orig_ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if orig_ext not in ALLOWED_EXTENSIONS:
        raise ValueError('Logo must be a PNG, JPG or WebP image.')
    ext = 'jpg' if orig_ext == 'jpeg' else orig_ext

    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > MAX_SIZE:
        raise ValueError('Logo must be under 2MB.')

    try:
        file.stream.seek(0)
        Image.open(file.stream).verify()
    except Exception:
        raise ValueError('Logo file is not a valid image.')
    file.stream.seek(0)

    filename = f'{uuid.uuid4().hex}.{ext}'
    tmp_path = f'/tmp/{filename}'
    file.save(tmp_path)
    r2_key = f'uploads/{filename}'
    try:
        upload_file(tmp_path, r2_key)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    return r2_key


def generate_qr(slug, site_url):
    url = f'{site_url.rstrip("/")}/c/{slug}'
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1F5C46", back_color="#FFFFFF")
    tmp_path = f'/tmp/{slug}_qr.png'
    img.save(tmp_path)
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


DEFAULT_FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'fonts')

REQUIRED_DESIGN_FONTS = {
    'PlayfairDisplay-Regular': os.path.join(DEFAULT_FONTS_DIR, 'playfair-display', 'PlayfairDisplay-Regular.ttf'),
    'PlayfairDisplay-Bold': os.path.join(DEFAULT_FONTS_DIR, 'playfair-display', 'PlayfairDisplay-Bold.ttf'),
    'Cormorant-Regular': os.path.join(DEFAULT_FONTS_DIR, 'cormorant', 'Cormorant-Regular.ttf'),
    'Cormorant-Bold': os.path.join(DEFAULT_FONTS_DIR, 'cormorant', 'Cormorant-Bold.ttf'),
    'Poppins-Regular': os.path.join(DEFAULT_FONTS_DIR, 'poppins', 'Poppins-Regular.ttf'),
    'Poppins-Bold': os.path.join(DEFAULT_FONTS_DIR, 'poppins', 'Poppins-Bold.ttf'),
}


def register_design_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    registered = pdfmetrics.getRegisteredFontNames()
    for name, path in REQUIRED_DESIGN_FONTS.items():
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Missing font file for {name}: {path}")
        if name not in registered:
            pdfmetrics.registerFont(TTFont(name, path))


def generate_pdf(slug, brand_name, tagline, site_url, logo_path=None, card_style='oxblood', pdf_r2_key=None, card_colour=None, card_border=None, card_font=None):
    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    card_w = 85 * mm_unit
    card_h = 55 * mm_unit
    pdf_path = f'/tmp/{slug}_card.pdf'
    qr_img_path = f'/tmp/{slug}_qr.png'

    register_design_fonts()

    c = canvas.Canvas(pdf_path, pagesize=(card_w, card_h))

    design = resolve_design(
        card_colour=card_colour,
        card_border=card_border,
        card_font=card_font,
        legacy_card_style=card_style,
    )
    name_font = design['pdf_bold']
    tag_font = design['pdf_regular']
    from reportlab.pdfbase import pdfmetrics as _pdfm
    if name_font not in _pdfm.getRegisteredFontNames():
        raise RuntimeError(f"PDF bold font {name_font!r} not registered")
    if tag_font not in _pdfm.getRegisteredFontNames():
        raise RuntimeError(f"PDF regular font {tag_font!r} not registered")
    front_bg = design['bg']
    text_colour = design['text']
    accent_colour = design['accent']
    is_light = design['light']
    has_tagline = bool(tagline and tagline.strip())
    initial = brand_name[0].upper() if brand_name else 'B'

    def draw_border_treatment(border_renderer):
        inset = 2.5 * mm_unit
        if border_renderer == 'keyline':
            c.setStrokeColorRGB(*accent_colour)
            c.setLineWidth(0.4)
            c.roundRect(inset, inset, card_w - 2*inset, card_h - 2*inset, 1.2*mm_unit, fill=0, stroke=1)
        elif border_renderer == 'corner_marks':
            c.setStrokeColorRGB(*accent_colour)
            c.setLineWidth(0.5)
            leg = 3 * mm_unit
            c.line(inset, inset, inset + leg, inset)
            c.line(inset, inset, inset, inset + leg)
            c.line(card_w - inset, inset, card_w - inset - leg, inset)
            c.line(card_w - inset, inset, card_w - inset, inset + leg)
            c.line(inset, card_h - inset, inset + leg, card_h - inset)
            c.line(inset, card_h - inset, inset, card_h - inset - leg)
            c.line(card_w - inset, card_h - inset, card_w - inset - leg, card_h - inset)
            c.line(card_w - inset, card_h - inset, card_w - inset, card_h - inset - leg)
        elif border_renderer == 'split_edge':
            c.setStrokeColorRGB(*accent_colour)
            c.setLineWidth(0.4)
            gap_half = 4 * mm_unit
            mid_y = card_h / 2
            c.line(inset, card_h - inset, inset, mid_y + gap_half)
            c.line(inset, mid_y - gap_half, inset, inset)
            c.line(card_w - inset, card_h - inset, card_w - inset, mid_y + gap_half)
            c.line(card_w - inset, mid_y - gap_half, card_w - inset, inset)
        elif border_renderer == 'top_bottom_rule':
            c.setStrokeColorRGB(*accent_colour)
            c.setLineWidth(0.4)
            c.line(inset, inset, card_w - inset, inset)
            c.line(inset, card_h - inset, card_w - inset, card_h - inset)
        elif border_renderer == 'none':
            pass
        else:
            raise ValueError(f'Unsupported border_renderer: {border_renderer!r}')

    def draw_front():
        c.setFillColorRGB(*front_bg)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        if has_tagline:
            # A1 layout — logo box, name, divider, tagline — vertically centred as a group
            logo_box_size = 12 * mm_unit
            gap_logo_name = 4 * mm_unit
            name_h = 5 * mm_unit
            gap_name_div = 3.5 * mm_unit
            gap_div_tag = 3.5 * mm_unit
            tag_h = 2 * mm_unit
            group_h = logo_box_size + gap_logo_name + name_h + gap_name_div + gap_div_tag + tag_h
            group_y_start = (card_h / 2) + (group_h / 2)

            logo_box_x = (card_w - logo_box_size) / 2
            logo_box_y = group_y_start - logo_box_size - (group_h * 0.05)

            # Logo border box
            c.setStrokeColorRGB(*text_colour)
            c.setLineWidth(0.35)
            c.setFillColorRGB(*front_bg)
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
                c.setFillColorRGB(*text_colour)
                c.setFont(name_font, 9)
                c.drawCentredString(
                    logo_box_x + logo_box_size / 2,
                    logo_box_y + logo_box_size / 2 - 3,
                    initial
                )

            # Brand name
            name_y = logo_box_y - 6 * mm_unit
            c.setFillColorRGB(*accent_colour)
            c.setFont(name_font, 13)
            c.drawCentredString(card_w / 2, name_y, brand_name)

            # Divider
            divider_w = 10 * mm_unit
            divider_y = name_y - 3.5 * mm_unit
            c.setStrokeColorRGB(*accent_colour)
            c.setLineWidth(0.7)
            c.line(card_w / 2 - divider_w / 2, divider_y, card_w / 2 + divider_w / 2, divider_y)

            # Tagline
            c.setFillColorRGB(*text_colour)
            c.setFont(tag_font, 5.5)
            c.drawCentredString(card_w / 2, divider_y - 3.5 * mm_unit, tagline.upper())

            # URL for cardbranch card
            if slug == "cardbranch":
                c.setFont(tag_font, 4)
                c.drawCentredString(card_w / 2, divider_y - 5.5 * mm_unit, "www.cardbranch.co.uk")

        else:
            # A3 layout — large logo box centred, brand name small below
            logo_box_size = 18 * mm_unit
            logo_box_x = (card_w - logo_box_size) / 2
            logo_box_y = (card_h - logo_box_size) / 2 + 3 * mm_unit

            c.setStrokeColorRGB(*text_colour)
            c.setLineWidth(0.35)
            c.setFillColorRGB(*front_bg)
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
                c.setFillColorRGB(*text_colour)
                c.setFont(name_font, 14)
                c.drawCentredString(
                    logo_box_x + logo_box_size / 2,
                    logo_box_y + logo_box_size / 2 - 5,
                    initial
                )

            c.setFillColorRGB(*text_colour)
            c.setFont(tag_font, 6.5)
            c.drawCentredString(card_w / 2, logo_box_y - 4.5 * mm_unit, brand_name.upper())

            # URL for cardbranch card
            if slug == "cardbranch":
                c.setFont(tag_font, 4)
                c.drawCentredString(card_w / 2, logo_box_y - 6.5 * mm_unit, "www.cardbranch.co.uk")

        draw_border_treatment(design['border_renderer'])

    def draw_back():
        c.setFillColorRGB(*front_bg)
        c.rect(0, 0, card_w, card_h, fill=1, stroke=0)

        qr_size = 26 * mm_unit
        label_gap = 2.5 * mm_unit
        url_gap = 1.5 * mm_unit
        scan_label = "SCAN TO CONNECT"
        url_text = f"cardbranch.co.uk/c/{slug}"

        scan_label_h = 2 * mm_unit
        url_h = 1.5 * mm_unit

        group_h = qr_size + label_gap + scan_label_h + url_gap + url_h
        group_y_top = (card_h / 2) + (group_h / 2)

        qr_y = group_y_top - qr_size
        qr_x = (card_w - qr_size) / 2

        if os.path.exists(qr_img_path):
            c.drawImage(qr_img_path, qr_x, qr_y, width=qr_size, height=qr_size)

        label_y = qr_y - label_gap - scan_label_h
        c.setFillColorRGB(*text_colour)
        c.setFont(name_font, 5)
        c.drawCentredString(card_w / 2, label_y, scan_label)

        url_y = label_y - url_gap - url_h
        c.setFont(tag_font, 4)
        c.drawCentredString(card_w / 2, url_y, url_text)

        draw_border_treatment(design['border_renderer'])

    draw_front()
    c.showPage()
    draw_back()
    c.save()

    upload_file(pdf_path, pdf_r2_key)
    return pdf_path


def generate_assets(slug, brand_name, tagline, site_url, logo_filename=None, card_style='oxblood', card_colour=None, card_border=None, card_font=None):
    token = secrets.token_urlsafe(16)
    pdf_r2_key = f'generated/{slug}/{token}/card.pdf'
    qr_tmp = generate_qr(slug, site_url)
    logo_tmp = download_logo(logo_filename)
    pdf_tmp = generate_pdf(slug, brand_name, tagline, site_url, logo_path=logo_tmp, card_style=card_style, pdf_r2_key=pdf_r2_key, card_colour=card_colour, card_border=card_border, card_font=card_font)
    if os.path.exists(qr_tmp):
        os.remove(qr_tmp)
    if pdf_tmp and os.path.exists(pdf_tmp):
        os.remove(pdf_tmp)
    if logo_tmp and os.path.exists(logo_tmp):
        os.remove(logo_tmp)
    return pdf_r2_key
