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
