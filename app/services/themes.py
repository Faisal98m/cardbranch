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
    """CSS-ready theme for web templates.
    NOTE: Only 'bg' is rendered on the web (the page background wall).
    'text', 'accent', 'layout' are PDF-only in Phase 1 — included for future
    use but the links page does not render them."""
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
