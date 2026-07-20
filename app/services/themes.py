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

_DEFAULT_COLOUR = 'oxblood'
_DEFAULT_BORDER = 'none'
_DEFAULT_FONT = 'playfair'


def resolve_design(card_colour=None, card_border=None, card_font=None):
    """Resolve card design from independent card_colour, card_border, card_font.

    Each axis falls back independently:
      - invalid/missing colour → oxblood
      - invalid/missing border → none
      - invalid/missing font  → playfair
    """
    colour_key = card_colour if card_colour is not None and card_colour in CARD_COLOURS else _DEFAULT_COLOUR
    border_key = card_border if card_border is not None and card_border in CARD_BORDERS else _DEFAULT_BORDER
    font_key = card_font if card_font is not None and card_font in CARD_FONTS else _DEFAULT_FONT

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


SELECTABLE_COLOUR_KEYS = ['oxblood', 'navy', 'forest', 'linen', 'sage', 'blush', 'midnight_framed', 'evergreen_classic']
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
