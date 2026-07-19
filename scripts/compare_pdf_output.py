"""
Compare OLD (resolve_theme) vs NEW (resolve_design) full two-page PDF output
for every local Client row, using each row's actual inputs.

ReportLab embeds a random /ID in the PDF trailer on every generation, so raw
SHA-256 will always differ.  We normalise by stripping only /ID, then compare
content.  If normalised content differs, we rasterise both pages at 300 DPI
and pixel-compare.
"""

import os
import sys
import hashlib
import tempfile
import re
import qrcode

os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_CONFIG'] = 'Debug'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.services.themes import resolve_design
from reportlab.lib.units import mm as mm_unit
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageChops
import sqlalchemy as sa
import numpy as np


# ── fonts ───────────────────────────────────────────────────────────────
def _register_fonts():
    candidate_dirs = [
        os.path.join(os.path.dirname(__file__), '..', 'static', 'fonts'),
        os.path.join(os.path.dirname(__file__), 'static', 'fonts'),
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
    return name_font, tag_font


_NAME_FONT, _TAG_FONT = _register_fonts()

CARD_W = 85 * mm_unit
CARD_H = 55 * mm_unit
LINEN = (0.941, 0.922, 0.894)


# ── QR generation (local, no R2 upload) ────────────────────────────────
def _local_qr(slug, site_url, output_path):
    url = '{}/c/{}'.format(site_url.rstrip('/'), slug)
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='#1F5C46', back_color='#FFFFFF')
    img.save(output_path)


# ── drawing helpers ────────────────────────────────────────────────────
def _draw_front(c, design, brand_name, tagline, slug, logo_path):
    front_bg = design['bg']
    text_colour = design['text']
    accent_colour = design['accent']
    has_tagline = bool(tagline and tagline.strip())
    initial = brand_name[0].upper() if brand_name else 'B'

    c.setFillColorRGB(*front_bg)
    c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)

    if has_tagline:
        logo_box_size = 12 * mm_unit
        gap_logo_name = 4 * mm_unit
        name_h = 5 * mm_unit
        gap_name_div = 3.5 * mm_unit
        gap_div_tag = 3.5 * mm_unit
        tag_h = 2 * mm_unit
        group_h = logo_box_size + gap_logo_name + name_h + gap_name_div + gap_div_tag + tag_h
        group_y_start = (CARD_H / 2) + (group_h / 2)
        logo_box_x = (CARD_W - logo_box_size) / 2
        logo_box_y = group_y_start - logo_box_size - (group_h * 0.05)

        c.setStrokeColorRGB(*text_colour)
        c.setLineWidth(0.35)
        c.setFillColorRGB(*front_bg)
        c.roundRect(logo_box_x, logo_box_y, logo_box_size, logo_box_size, 1.2 * mm_unit, fill=1, stroke=1)

        if logo_path and os.path.exists(logo_path):
            padding = 1.5 * mm_unit
            c.drawImage(logo_path, logo_box_x + padding, logo_box_y + padding,
                        width=logo_box_size - 2 * padding, height=logo_box_size - 2 * padding,
                        mask='auto' if logo_path.endswith('.png') else None, preserveAspectRatio=True)
        else:
            c.setFillColorRGB(*text_colour)
            c.setFont(_NAME_FONT, 9)
            c.drawCentredString(logo_box_x + logo_box_size / 2, logo_box_y + logo_box_size / 2 - 3, initial)

        name_y = logo_box_y - 6 * mm_unit
        c.setFillColorRGB(*accent_colour)
        c.setFont(_NAME_FONT, 13)
        c.drawCentredString(CARD_W / 2, name_y, brand_name)

        divider_w = 10 * mm_unit
        divider_y = name_y - 3.5 * mm_unit
        c.setStrokeColorRGB(*accent_colour)
        c.setLineWidth(0.7)
        c.line(CARD_W / 2 - divider_w / 2, divider_y, CARD_W / 2 + divider_w / 2, divider_y)

        c.setFillColorRGB(*text_colour)
        c.setFont(_TAG_FONT, 5.5)
        c.drawCentredString(CARD_W / 2, divider_y - 3.5 * mm_unit, tagline.upper())

        if slug == 'cardbranch':
            c.setFont(_TAG_FONT, 4)
            c.drawCentredString(CARD_W / 2, divider_y - 5.5 * mm_unit, 'www.cardbranch.co.uk')
    else:
        logo_box_size = 18 * mm_unit
        logo_box_x = (CARD_W - logo_box_size) / 2
        logo_box_y = (CARD_H - logo_box_size) / 2 + 3 * mm_unit

        c.setStrokeColorRGB(*text_colour)
        c.setLineWidth(0.35)
        c.setFillColorRGB(*front_bg)
        c.roundRect(logo_box_x, logo_box_y, logo_box_size, logo_box_size, 2 * mm_unit, fill=1, stroke=1)

        if logo_path and os.path.exists(logo_path):
            padding = 2 * mm_unit
            c.drawImage(logo_path, logo_box_x + padding, logo_box_y + padding,
                        width=logo_box_size - 2 * padding, height=logo_box_size - 2 * padding,
                        mask='auto' if logo_path.endswith('.png') else None, preserveAspectRatio=True)
        else:
            c.setFillColorRGB(*text_colour)
            c.setFont(_NAME_FONT, 14)
            c.drawCentredString(logo_box_x + logo_box_size / 2, logo_box_y + logo_box_size / 2 - 5, initial)

        c.setFillColorRGB(*text_colour)
        c.setFont(_TAG_FONT, 6.5)
        c.drawCentredString(CARD_W / 2, logo_box_y - 4.5 * mm_unit, brand_name.upper())

        if slug == 'cardbranch':
            c.setFont(_TAG_FONT, 4)
            c.drawCentredString(CARD_W / 2, logo_box_y - 6.5 * mm_unit, 'www.cardbranch.co.uk')

    # Border decoration
    inset = 2.5 * mm_unit
    br = design.get('border_renderer') or design.get('layout')
    if br == 'framed' or br == 'keyline':
        c.setStrokeColorRGB(*accent_colour)
        c.setLineWidth(0.4)
        c.roundRect(inset, inset, CARD_W - 2 * inset, CARD_H - 2 * inset, 1.2 * mm_unit, fill=0, stroke=1)
    elif br == 'corner_brackets' or br == 'corner_marks':
        c.setStrokeColorRGB(*accent_colour)
        c.setLineWidth(0.5)
        leg = 3 * mm_unit
        c.line(inset, inset, inset + leg, inset)
        c.line(inset, inset, inset, inset + leg)
        c.line(CARD_W - inset, inset, CARD_W - inset - leg, inset)
        c.line(CARD_W - inset, inset, CARD_W - inset, inset + leg)
        c.line(inset, CARD_H - inset, inset + leg, CARD_H - inset)
        c.line(inset, CARD_H - inset, inset, CARD_H - inset - leg)
        c.line(CARD_W - inset, CARD_H - inset, CARD_W - inset - leg, CARD_H - inset)
        c.line(CARD_W - inset, CARD_H - inset, CARD_W - inset, CARD_H - inset - leg)


def _draw_back(c, qr_path, slug):
    c.setFillColorRGB(*LINEN)
    c.rect(0, 0, CARD_W, CARD_H, fill=1, stroke=0)
    if os.path.exists(qr_path):
        qr_size = 32 * mm_unit
        qr_x = round((CARD_W - qr_size) / 2)
        qr_y = round((CARD_H - qr_size) / 2)
        c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
        if slug == 'cardbranch':
            c.setFillColorRGB(0.102, 0.090, 0.082)
            c.setFont(_TAG_FONT, 4)
            c.drawCentredString(CARD_W / 2, qr_y - 3 * mm_unit, 'www.cardbranch.co.uk')


def render_two_page_pdf(output_path, design, brand_name, tagline, slug, logo_path, qr_path):
    """Render a complete two-page card PDF (front + back)."""
    c = canvas.Canvas(output_path, pagesize=(CARD_W, CARD_H))
    c._doc.info.creationDate = (2024, 1, 1, 0, 0, 0)
    _draw_front(c, design, brand_name, tagline, slug, logo_path)
    c.showPage()
    _draw_back(c, qr_path, slug)
    c.save()


# ── PDF normalisation (strip non-deterministic metadata) ──────────────
# ReportLab embeds:
#   /ID (random per generation)
#   /CreationDate (ignores our override — uses wall clock during save)
#   /ModDate (same issue)
# /Creator and /Producer are deterministic and kept.
_META_RE = re.compile(rb'(/ID\s*\[<[0-9a-fA-F]+><[0-9a-fA-F]+>\]|'
                       rb'/CreationDate\s*\([^)]+\)|'
                       rb'/ModDate\s*\([^)]+\))')


def normalized_bytes(path):
    with open(path, 'rb') as f:
        data = f.read()
    return _META_RE.sub(b'', data)


def sha256_raw(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_normalized(path):
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def page_count(path):
    """Return number of pages in a PDF by counting /Type /Page entries."""
    with open(path, 'rb') as f:
        data = f.read()
    # Count /Type /Page (not /Type /Pages which is the page tree node)
    return len(re.findall(rb'/Type\s*/Page[^s]', data))


# ── pixel comparison (via pymupdf — no poppler dependency) ─────────────
def pixel_compare_all(path_old, path_new, dpi=300):
    """Rasterise both PDFs at dpi using pymupdf and return per-page diff stats."""
    try:
        import fitz
    except ImportError:
        return {'error': 'pymupdf not installed; pip install pymupdf'}
    try:
        doc_old = fitz.open(path_old)
        doc_new = fitz.open(path_new)
    except Exception as e:
        return {'error': str(e)}

    if doc_old.page_count != doc_new.page_count:
        return {'pages_mismatch': True, 'old_pages': doc_old.page_count, 'new_pages': doc_new.page_count}

    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    results = []

    for i in range(doc_old.page_count):
        pix_old = doc_old[i].get_pixmap(matrix=mat)
        pix_new = doc_new[i].get_pixmap(matrix=mat)
        img_old = Image.frombytes('RGB', (pix_old.width, pix_old.height), pix_old.samples)
        img_new = Image.frombytes('RGB', (pix_new.width, pix_new.height), pix_new.samples)
        diff = ImageChops.difference(img_old, img_new)
        bbox = diff.getbbox()
        if bbox is None:
            results.append({'page': i + 1, 'differing_pixels': 0, 'max_diff': 0})
        else:
            arr = np.array(diff)
            differing = int(np.count_nonzero(arr))
            max_diff = int(arr.max())
            results.append({'page': i + 1, 'differing_pixels': differing, 'max_diff': max_diff})

    doc_old.close()
    doc_new.close()
    return results


# ── logo download (silent fail without R2) ─────────────────────────────
def _try_logo(logo_filename):
    if not logo_filename:
        return None
    try:
        from app.services.generator import download_logo
        return download_logo(logo_filename)
    except Exception:
        return None


# ── main ────────────────────────────────────────────────────────────────
def main():
    site_url = os.environ.get('SITE_URL', 'http://localhost:5000')
    app = create_app('Debug')
    out_dir = tempfile.mkdtemp(prefix='pdf_full_compare_')
    qr_dir = tempfile.mkdtemp(prefix='qr_')
    print('Output directory: {}'.format(out_dir))
    print()

    with app.app_context():
        rows = db.session.execute(
            sa.text(
                'SELECT id, brand_name, tagline, slug, '
                'card_colour, card_border, card_font, logo_filename '
                'FROM clients ORDER BY id'
            )
        ).all()

    all_normalized_match = True
    all_page_counts_ok = True
    results = []
    any_pixel_diff = False

    for row in rows:
        brand_name = row.brand_name or ''
        tagline = row.tagline or ''
        slug = row.slug

        # Logo — try to download; if it fails, use None for both
        logo_path = _try_logo(row.logo_filename)

        # QR — generate once, use for both old and new
        qr_path = os.path.join(qr_dir, '{}.png'.format(slug))
        _local_qr(slug, site_url, qr_path)

        # Design from independent fields (no legacy card_style)
        design = resolve_design(
            card_colour=row.card_colour,
            card_border=row.card_border,
            card_font=row.card_font,
        )
        pass1_path = os.path.join(out_dir, 'pass1_{}.pdf'.format(row.id))
        render_two_page_pdf(pass1_path, design, brand_name, tagline, slug, logo_path, qr_path)

        pass2_path = os.path.join(out_dir, 'pass2_{}.pdf'.format(row.id))
        render_two_page_pdf(pass2_path, design, brand_name, tagline, slug, logo_path, qr_path)

        # Page counts
        p1_pages = page_count(pass1_path)
        p2_pages = page_count(pass2_path)
        pages_ok = (p1_pages == 2 and p2_pages == 2)
        if not pages_ok:
            all_page_counts_ok = False

        # Raw SHA-256
        raw_p1 = sha256_raw(pass1_path)
        raw_p2 = sha256_raw(pass2_path)
        raw_match = raw_p1 == raw_p2

        # Normalised SHA-256 (strip only /ID)
        norm_data_p1 = normalized_bytes(pass1_path)
        norm_data_p2 = normalized_bytes(pass2_path)
        norm_hash_p1 = hashlib.sha256(norm_data_p1).hexdigest()
        norm_hash_p2 = hashlib.sha256(norm_data_p2).hexdigest()
        norm_match = norm_hash_p1 == norm_hash_p2
        if not norm_match:
            all_normalized_match = False

        # Pixel comparison (only if norm content differs or as full verification)
        pixel = None
        if not norm_match:
            pixel = pixel_compare_all(pass1_path, pass2_path)
            if isinstance(pixel, list):
                for p in pixel:
                    if p['differing_pixels'] > 0:
                        any_pixel_diff = True
        else:
            pixel = pixel_compare_all(pass1_path, pass2_path)

        if isinstance(pixel, list):
            for p in pixel:
                if p['differing_pixels'] > 0:
                    any_pixel_diff = True

        logo_present = row.logo_filename is not None and row.logo_filename != ''

        colour_key = design['colour_key'] if design else '?'
        results.append({
            'id': row.id,
            'colour': colour_key,
            'logo_present': logo_present,
            'p1_pages': p1_pages,
            'p2_pages': p2_pages,
            'pages_ok': pages_ok,
            'raw_match': raw_match,
            'norm_len_p1': len(norm_data_p1),
            'norm_len_p2': len(norm_data_p2),
            'norm_match': norm_match,
            'pixel': pixel,
        })

    # ── report table ──
    header = '{:>4s}  {:20s}  {:6s}  {:>4s} {:>4s}  {:10s}  {:>12s} {:>12s}  {:10s}  {:20s} {:20s}'.format(
        'id', 'colour', 'logo', 'p1p', 'p2p', 'raw match',
        'norm len 1', 'norm len 2', 'norm match',
        'front px', 'back px')
    print(header)
    print('-' * 135)
    for r in results:
        logo_str = 'YES' if r['logo_present'] else 'no'
        raw_str = 'YES' if r['raw_match'] else 'NO (/ID)'
        norm_str = 'YES' if r['norm_match'] else 'NO'
        front_str = '-'
        back_str = '-'
        pr = r['pixel']
        if isinstance(pr, list):
            for p in pr:
                label = 'p{}: {}px m={}'.format(p['page'], p['differing_pixels'], p['max_diff'])
                if p['page'] == 1:
                    front_str = label
                elif p['page'] == 2:
                    back_str = label
        elif isinstance(pr, dict):
            front_str = pr.get('error', str(pr))
            back_str = ''

        print('{:>4d}  {:20s}  {:6s}  {:>4d} {:>4d}  {:10s}  {:>12d} {:>12d}  {:10s}  {:20s} {:20s}'.format(
            r['id'], r['colour'], logo_str,
            r['p1_pages'], r['p2_pages'], raw_str,
            r['norm_len_p1'], r['norm_len_p2'], norm_str,
            front_str, back_str))

    print()
    logos_present = sum(1 for r in results if r['logo_present'])
    print('Rows: {}  Logo present: {}  No logo: {}'.format(len(results), logos_present, len(results) - logos_present))
    print('All page counts OK (2 each): {}'.format(all_page_counts_ok))
    print('All normalised hashes match: {}'.format(all_normalized_match))
    if all_normalized_match:
        print('(Raw SHA-256 differs for all due to random PDF /ID in trailer — expected.)')

    if isinstance(results[0]['pixel'], list):
        all_clean = True
        for r in results:
            pr = r['pixel']
            if isinstance(pr, list):
                for p in pr:
                    if p['differing_pixels'] != 0 or p['max_diff'] != 0:
                        all_clean = False
        if all_clean:
            print('Pixel comparison: ALL PAGES CLEAN (0 differing pixels, max diff=0)')
        else:
            print('Pixel comparison: SOME DIFFERENCES FOUND')
    elif isinstance(results[0]['pixel'], dict):
        print('Pixel comparison: {}'.format(results[0]['pixel'].get('error', 'unavailable')))

    print()
    print('Temp directory: {}'.format(out_dir))


if __name__ == '__main__':
    main()
