CARD_THEMES = {
    'oxblood':  {'bg': (0.420, 0.122, 0.165), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'layout': 'minimal'},
    'navy':     {'bg': (0.102, 0.153, 0.267), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'layout': 'minimal'},
    'forest':   {'bg': (0.102, 0.239, 0.169), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'layout': 'minimal'},
    'slate':    {'bg': (0.176, 0.216, 0.282), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'layout': 'minimal'},
    'charcoal': {'bg': (0.102, 0.090, 0.082), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'layout': 'minimal'},
    'linen':    {'bg': (0.941, 0.922, 0.894), 'text': (0.102, 0.090, 0.082), 'accent': (0.102, 0.090, 0.082), 'light': True,  'layout': 'minimal'},
    'sage':     {'bg': (0.910, 0.929, 0.910), 'text': (0.102, 0.090, 0.082), 'accent': (0.102, 0.090, 0.082), 'light': True,  'layout': 'minimal'},
    'blush':    {'bg': (0.961, 0.925, 0.910), 'text': (0.102, 0.090, 0.082), 'accent': (0.102, 0.090, 0.082), 'light': True,  'layout': 'minimal'},

    'midnight_framed':   {'bg': (0.071, 0.125, 0.227), 'text': (0.941, 0.929, 0.910), 'accent': (0.788, 0.635, 0.294), 'light': False, 'layout': 'framed'},
    'oxblood_minimal':   {'bg': (0.420, 0.122, 0.165), 'text': (0.961, 0.929, 0.886), 'accent': (0.878, 0.788, 0.651), 'light': False, 'layout': 'minimal'},
    'linen_brackets':    {'bg': (0.957, 0.945, 0.918), 'text': (0.165, 0.149, 0.125), 'accent': (0.122, 0.361, 0.275), 'light': True,  'layout': 'corner_brackets'},
    'evergreen_classic': {'bg': (0.078, 0.196, 0.122), 'text': (0.933, 0.941, 0.918), 'accent': (0.780, 0.659, 0.400), 'light': False, 'layout': 'framed'},
    'noir_framed':       {'bg': (0.086, 0.086, 0.086), 'text': (0.941, 0.929, 0.910), 'accent': (0.788, 0.635, 0.294), 'light': False, 'layout': 'framed'},
}


def resolve_theme(card_style):
    """Resolve a card_style key to a theme dict. Unknown or legacy keys
    (None, 'default', empty, or any unrecognised value) fall back to 'oxblood',
    which is the exact fallback the previous CARD_COLOURS.get(card_style,
    CARD_COLOURS['oxblood']) used — preserving existing output for those cards."""
    return CARD_THEMES.get(card_style, CARD_THEMES['oxblood'])


def theme_css(card_style):
    """Return CSS-ready theme values for web templates.
    The public links page currently uses only bg for its background wall.
    Dashboard card previews (card_view, editor) also use text, accent, light,
    and layout to approximate the printed card."""
    t = resolve_theme(card_style)
    def rgb(tup):
        return 'rgb(%d, %d, %d)' % (round(tup[0]*255), round(tup[1]*255), round(tup[2]*255))
    return {
        'bg': rgb(t['bg']), 'text': rgb(t['text']), 'accent': rgb(t['accent']),
        'light': t['light'], 'layout': t['layout'],
    }


# Presentation metadata for the style picker. 'group' is INDEPENDENT of luminance:
# premium themes are grouped commercially, not by light/dark. layout_name is the
# customer-facing label — internal identifiers like 'corner_brackets' must never
# appear in the UI.
THEME_PICKER_META = {
    'oxblood':  {'name': 'Oxblood',  'group': 'dark',  'premium': False, 'layout_name': ''},
    'navy':     {'name': 'Navy',     'group': 'dark',  'premium': False, 'layout_name': ''},
    'forest':   {'name': 'Forest',   'group': 'dark',  'premium': False, 'layout_name': ''},
    'slate':    {'name': 'Slate',    'group': 'dark',  'premium': False, 'layout_name': ''},
    'charcoal': {'name': 'Charcoal', 'group': 'dark',  'premium': False, 'layout_name': ''},
    'linen':    {'name': 'Linen',    'group': 'light', 'premium': False, 'layout_name': ''},
    'sage':     {'name': 'Sage',     'group': 'light', 'premium': False, 'layout_name': ''},
    'blush':    {'name': 'Blush',    'group': 'light', 'premium': False, 'layout_name': ''},
    'midnight_framed':   {'name': 'Midnight Framed',   'group': 'premium', 'premium': True, 'layout_name': 'Framed'},
    'oxblood_minimal':   {'name': 'Oxblood Minimal',   'group': 'premium', 'premium': True, 'layout_name': 'Minimal'},
    'linen_brackets':    {'name': 'Linen Brackets',    'group': 'premium', 'premium': True, 'layout_name': 'Brackets'},
    'evergreen_classic': {'name': 'Evergreen Classic', 'group': 'premium', 'premium': True, 'layout_name': 'Framed'},
    'noir_framed':       {'name': 'Noir Framed',       'group': 'premium', 'premium': True, 'layout_name': 'Framed'},
}

# Explicit stable order for the picker (dark, then light, then premium).
_PICKER_ORDER = [
    'oxblood', 'navy', 'forest', 'slate', 'charcoal',
    'linen', 'sage', 'blush',
    'midnight_framed', 'oxblood_minimal', 'linen_brackets', 'evergreen_classic', 'noir_framed',
]

def theme_picker_options():
    """Presentation-ready picker options, in stable order, CSS-ready colours.
    Each option: key, name, group, premium, layout_name, bg, text, accent, light, layout."""
    def rgb(tup):
        return 'rgb(%d, %d, %d)' % (round(tup[0]*255), round(tup[1]*255), round(tup[2]*255))
    opts = []
    for key in _PICKER_ORDER:
        t = CARD_THEMES[key]
        meta = THEME_PICKER_META[key]
        opts.append({
            'key': key, 'name': meta['name'], 'group': meta['group'],
            'premium': meta['premium'], 'layout_name': meta['layout_name'],
            'bg': rgb(t['bg']), 'text': rgb(t['text']), 'accent': rgb(t['accent']),
            'light': t['light'], 'layout': t['layout'],
        })
    return opts

def normalise_theme_key(card_style, fallback='oxblood'):
    """Return card_style if it is a known theme, else fallback."""
    return card_style if card_style in CARD_THEMES else fallback

def theme_picker_option(card_style):
    """One presentation-ready picker option for card_style, falling back to oxblood."""
    key = normalise_theme_key(card_style)
    for option in theme_picker_options():
        if option['key'] == key:
            return option
    return theme_picker_options()[0]  # unreachable; normalise guarantees a valid key


# ---------------------------------------------------------------------------
# New-style design registries (card_colour / card_border / card_font)
# ---------------------------------------------------------------------------
# These are data-only. No renderer, route, template, or form changes yet.
# The existing card_style column and CARD_THEMES remain the active system.
# ---------------------------------------------------------------------------

CARD_COLOURS = {
    'oxblood':           {'bg': (0.420, 0.122, 0.165), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'display_name': 'Oxblood'},
    'navy':              {'bg': (0.102, 0.153, 0.267), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'display_name': 'Navy'},
    'forest':            {'bg': (0.102, 0.239, 0.169), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'display_name': 'Forest'},
    'slate':             {'bg': (0.176, 0.216, 0.282), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'display_name': 'Slate'},
    'charcoal':          {'bg': (0.102, 0.090, 0.082), 'text': (0.980, 0.973, 0.957), 'accent': (0.980, 0.973, 0.957), 'light': False, 'display_name': 'Charcoal'},
    'linen':             {'bg': (0.941, 0.922, 0.894), 'text': (0.102, 0.090, 0.082), 'accent': (0.102, 0.090, 0.082), 'light': True,  'display_name': 'Linen'},
    'sage':              {'bg': (0.910, 0.929, 0.910), 'text': (0.102, 0.090, 0.082), 'accent': (0.102, 0.090, 0.082), 'light': True,  'display_name': 'Sage'},
    'blush':             {'bg': (0.961, 0.925, 0.910), 'text': (0.102, 0.090, 0.082), 'accent': (0.102, 0.090, 0.082), 'light': True,  'display_name': 'Blush'},
    'midnight_framed':   {'bg': (0.071, 0.125, 0.227), 'text': (0.941, 0.929, 0.910), 'accent': (0.788, 0.635, 0.294), 'light': False, 'display_name': 'Midnight Framed'},
    'oxblood_minimal':   {'bg': (0.420, 0.122, 0.165), 'text': (0.961, 0.929, 0.886), 'accent': (0.878, 0.788, 0.651), 'light': False, 'display_name': 'Oxblood Minimal'},
    'linen_brackets':    {'bg': (0.957, 0.945, 0.918), 'text': (0.165, 0.149, 0.125), 'accent': (0.122, 0.361, 0.275), 'light': True,  'display_name': 'Linen Brackets'},
    'evergreen_classic': {'bg': (0.078, 0.196, 0.122), 'text': (0.933, 0.941, 0.918), 'accent': (0.780, 0.659, 0.400), 'light': False, 'display_name': 'Evergreen Classic'},
    'noir_framed':       {'bg': (0.086, 0.086, 0.086), 'text': (0.941, 0.929, 0.910), 'accent': (0.788, 0.635, 0.294), 'light': False, 'display_name': 'Noir Framed'},
}

CARD_BORDERS = {
    'none':             {'display_name': 'None',              'border_renderer': 'none'},
    'keyline':          {'display_name': 'Keyline',           'border_renderer': 'keyline'},
    'corner_marks':     {'display_name': 'Corner Marks',      'border_renderer': 'corner_marks'},
    'split_edge':       {'display_name': 'Split Edge',        'border_renderer': 'split_edge'},
    'top_bottom_rule':  {'display_name': 'Top & Bottom Rule', 'border_renderer': 'top_bottom_rule'},
}

CARD_FONTS = {
    'playfair': {
        'display_name': 'Playfair',
        'browser_family': "'Playfair Display', Georgia, serif",
        'pdf_regular': 'PlayfairDisplay-Regular',
        'pdf_bold': 'PlayfairDisplay-Bold',
    },
    'cormorant': {
        'display_name': 'Cormorant',
        'browser_family': "'Cormorant', Georgia, serif",
        'pdf_regular': 'Cormorant-Regular',
        'pdf_bold': 'Cormorant-Bold',
    },
    'poppins': {
        'display_name': 'Poppins',
        'browser_family': "'Poppins', Arial, sans-serif",
        'pdf_regular': 'Poppins-Regular',
        'pdf_bold': 'Poppins-Bold',
    },
}

# ---------------------------------------------------------------------------
# Legacy-style map — each legacy card_style key → (colour, border, font)
# ---------------------------------------------------------------------------
# Border reinterpretation of the old CARD_THEMES layout field:
#   'minimal'        → none
#   'framed'         → keyline
#   'corner_brackets' → corner_marks
# ---------------------------------------------------------------------------

LEGACY_STYLE_MAP = {
    'oxblood':           ('oxblood',          'none',          'playfair'),
    'navy':              ('navy',             'none',          'playfair'),
    'forest':            ('forest',           'none',          'playfair'),
    'slate':             ('slate',            'none',          'playfair'),
    'charcoal':          ('charcoal',         'none',          'playfair'),
    'linen':             ('linen',            'none',          'playfair'),
    'sage':              ('sage',             'none',          'playfair'),
    'blush':             ('blush',            'none',          'playfair'),
    'midnight_framed':   ('midnight_framed',  'keyline',       'playfair'),
    'oxblood_minimal':   ('oxblood_minimal',  'none',          'playfair'),
    'linen_brackets':    ('linen_brackets',   'corner_marks',  'playfair'),
    'evergreen_classic': ('evergreen_classic','keyline',       'playfair'),
    'noir_framed':       ('noir_framed',      'keyline',       'playfair'),
}

_LEGACY_FALLBACK = ('oxblood', 'none', 'playfair')


def resolve_design(card_colour=None, card_border=None, card_font=None, legacy_card_style=None):
    """Resolve card design from either the three new fields (all-or-nothing)
    or the legacy card_style key via LEGACY_STYLE_MAP.

    New-style path: all three must be non-None and valid in their registries.
    Legacy fallback path: uses LEGACY_STYLE_MAP with _LEGACY_FALLBACK for
    None, '', 'default', or any unrecognised key.
    Never blends new and legacy fields.
    """
    colour_valid = card_colour is not None and card_colour in CARD_COLOURS
    border_valid = card_border is not None and card_border in CARD_BORDERS
    font_valid = card_font is not None and card_font in CARD_FONTS

    if colour_valid and border_valid and font_valid:
        colour = CARD_COLOURS[card_colour]
        border = CARD_BORDERS[card_border]
        font = CARD_FONTS[card_font]
        return {
            'colour_key': card_colour,
            'border_key': card_border,
            'font_key': card_font,
            'bg': colour['bg'],
            'text': colour['text'],
            'accent': colour['accent'],
            'light': colour['light'],
            'border_renderer': border['border_renderer'],
            'browser_family': font['browser_family'],
            'pdf_regular': font['pdf_regular'],
            'pdf_bold': font['pdf_bold'],
        }

    # Legacy fallback
    if legacy_card_style is None or legacy_card_style == '' or legacy_card_style not in LEGACY_STYLE_MAP:
        resolved = _LEGACY_FALLBACK
    else:
        resolved = LEGACY_STYLE_MAP[legacy_card_style]

    colour_key, border_key, font_key = resolved
    colour = CARD_COLOURS[colour_key]
    border = CARD_BORDERS[border_key]
    font = CARD_FONTS[font_key]
    return {
        'colour_key': colour_key,
        'border_key': border_key,
        'font_key': font_key,
        'bg': colour['bg'],
        'text': colour['text'],
        'accent': colour['accent'],
        'light': colour['light'],
        'border_renderer': border['border_renderer'],
        'browser_family': font['browser_family'],
        'pdf_regular': font['pdf_regular'],
        'pdf_bold': font['pdf_bold'],
    }


def design_css(resolved):
    """Convert a resolved design dict into CSS-ready string values."""
    def rgb(tup):
        return 'rgb(%d, %d, %d)' % (round(tup[0]*255), round(tup[1]*255), round(tup[2]*255))
    return {
        'bg': rgb(resolved['bg']),
        'text': rgb(resolved['text']),
        'accent': rgb(resolved['accent']),
        'light': resolved['light'],
        'border_renderer': resolved['border_renderer'],
        'browser_family': resolved['browser_family'],
    }


SELECTABLE_COLOUR_KEYS = ['oxblood', 'navy', 'forest', 'linen', 'midnight_framed', 'evergreen_classic']
SELECTABLE_BORDER_KEYS = ['none', 'keyline', 'corner_marks', 'split_edge', 'top_bottom_rule']
SELECTABLE_FONT_KEYS = ['playfair', 'cormorant', 'poppins']

_COLOUR_DISPLAY_OVERRIDES = {
    'midnight_framed': 'Midnight',
    'evergreen_classic': 'Evergreen',
}

def card_colour_options():
    """Presentation-ready options for the 6 selectable new-style colours."""
    def rgb(tup):
        return 'rgb(%d, %d, %d)' % (round(tup[0]*255), round(tup[1]*255), round(tup[2]*255))
    opts = []
    for key in SELECTABLE_COLOUR_KEYS:
        c = CARD_COLOURS[key]
        opts.append({
            'key': key,
            'display_name': _COLOUR_DISPLAY_OVERRIDES.get(key, c['display_name']),
            'bg': rgb(c['bg']), 'text': rgb(c['text']), 'accent': rgb(c['accent']),
            'light': c['light'],
        })
    return opts

def card_border_options():
    """Presentation-ready options for all 5 borders, stable dict order."""
    return [
        {'key': k, 'display_name': v['display_name'], 'border_renderer': v['border_renderer']}
        for k, v in CARD_BORDERS.items()
    ]

def card_font_options():
    """Presentation-ready options for all 3 fonts, stable dict order."""
    return [
        {'key': k, 'display_name': v['display_name'], 'browser_family': v['browser_family']}
        for k, v in CARD_FONTS.items()
    ]
