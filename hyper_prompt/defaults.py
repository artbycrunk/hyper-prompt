NAME = 'hyper-prompt'

CONFIG = {
    "segments": [
        'virtual_env',
        'username'
    ]
}

CONFIG_LOCATIONS = [
    "hyper_prompt.json",
    "~/.hyper_prompt.json",
    "~/.config/hyper_prompt/config.json"]

TEMPLATES = {
    'bash': r'\[\e%s\]',
    'tcsh': r'%%{\e%s%%}',
    'zsh': '%%{%s%%}',
    'bare': '%s',
}

SYMBOLS = {
    'compatible': {
        'lock': 'RO',
        'network': 'SSH',
        'separator': u'\u25B6',
        'separator_thin': u'\u276F'
    },
    'patched': {
        'lock': u'\uE0A2',
        'network': 'SSH',
        'separator': u'\uE0B0',
        'separator_thin': u'\uE0B1'
    },
    'flat': {
        'lock': u'\uE0A2',
        'network': 'SSH',
        'separator': '',
        'separator_thin': ''
    },
}
