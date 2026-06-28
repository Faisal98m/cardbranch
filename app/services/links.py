import re

LINK_TYPES = {
    'website': {'icon': 'ti-world', 'input_mode': 'url'},
    'custom': {'icon': 'ti-link', 'input_mode': 'url'},
    'phone': {'icon': 'ti-phone', 'input_mode': 'tel'},
    'whatsapp': {'icon': 'ti-brand-whatsapp', 'input_mode': 'tel'},
    'email': {'icon': 'ti-mail', 'input_mode': 'email'},
    'instagram': {'icon': 'ti-brand-instagram', 'input_mode': 'handle'},
    'tiktok': {'icon': 'ti-brand-tiktok', 'input_mode': 'handle'},
    'linkedin': {'icon': 'ti-brand-linkedin', 'input_mode': 'url'},
}

UK_PHONE_RE = re.compile(r'^(?:\+44\d{10}|0\d{10})$')


def normalize_uk_phone(raw):
    """Strip spaces/dashes/brackets, validate UK format, return E.164 (+44...) or None if invalid."""
    cleaned = re.sub(r'[\s\-()]', '', raw or '')
    if not UK_PHONE_RE.match(cleaned):
        return None
    if cleaned.startswith('0'):
        return '+44' + cleaned[1:]
    return cleaned


def normalize_instagram_handle(raw):
    """Accept handle, @handle, or pasted URL; return the bare profile handle."""
    raw = (raw or '').strip()
    if raw.lower().startswith(('http://', 'https://')):
        raw = re.sub(r'^https?://[^/]+/?', '', raw, flags=re.IGNORECASE)
    raw = raw.split('?')[0]
    raw = raw.strip('/')
    raw = raw.lstrip('@')
    raw = raw.split('/')[0]
    return raw


def build_href(link_type, value):
    """Given a link's type and raw stored value, return the href to use in templates."""
    value = (value or '').strip()

    if link_type == 'phone':
        phone = normalize_uk_phone(value)
        return f'tel:{phone}' if phone else '#'

    if link_type == 'whatsapp':
        phone = normalize_uk_phone(value)
        return f'https://wa.me/{phone.lstrip("+")}' if phone else '#'

    if link_type == 'email':
        return f'mailto:{value}' if value else '#'

    if link_type == 'instagram':
        handle = normalize_instagram_handle(value)
        return f'https://instagram.com/{handle}' if handle else '#'

    if link_type == 'tiktok':
        handle = normalize_tiktok_handle(value)
        return f'https://tiktok.com/@{handle}' if handle else '#'

    # website, linkedin, custom: raw URL passthrough, adding https:// when missing
    if value and not value.lower().startswith(('http://', 'https://')):
        return f'https://{value}'

    return value or '#'


def normalize_tiktok_handle(raw):
    """Accept handle, @handle, or pasted URL; return the bare profile handle."""
    raw = (raw or '').strip()
    if raw.lower().startswith(('http://', 'https://')):
        raw = re.sub(r'^https?://[^/]+/?', '', raw, flags=re.IGNORECASE)
    raw = raw.split('?')[0]
    raw = raw.strip('/')
    raw = raw.lstrip('@')
    raw = raw.split('/')[0]
    return raw


def should_open_new_tab(link_type):
    """True if this link type should render with target=_blank + rel=noopener noreferrer."""
    return link_type not in ('phone', 'whatsapp', 'email')
