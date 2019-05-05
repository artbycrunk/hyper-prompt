from . import defaults
from hashlib import md5
from colorsys import hls_to_rgb, rgb_to_hls
from math import sqrt


def get_opposite_color(r, g, b):
    # convert to float before getting hls value
    r, g, b = [x/255.0 for x in [r, g, b]]
    hls = rgb_to_hls(r, g, b)
    opp = list(hls[:])
    # shift hue (a.k.a. color)
    opp[0] = (opp[0]+0.2) % 1
    if opp[1] > 255/2:   # for level you want to make sure they
        opp[1] -= 255/2  # are quite different so easily readable
    else:
        opp[1] += 255/2
    if opp[2] > -0.5:  # if saturation is low on first color increase second's
        opp[2] -= 0.5
    opp = hls_to_rgb(*opp)
    m = max(opp)
    if m > 255:  # colorsys module doesn't give caps to their conversions
        opp = [x*254/m for x in opp]
    return tuple([int(x) for x in opp])


def rgbstring2tuple(s):
    return tuple([int(h, 16) for h in (s[:2], s[2:4], s[4:])])


def __hex2rgb(hexa):
    r = int(hexa[0:2], 16)
    g = int(hexa[2:4], 16)
    b = int(hexa[4:6], 16)
    return [r, g, b]


def __distance(a, b):
    x = (a[0] - b[0]) ** 2
    y = (a[1] - b[1]) ** 2
    z = (a[2] - b[2]) ** 2
    return sqrt(x + y + z)


_colors = list(map(__hex2rgb, defaults.HEX_COLORS))


def rgb2short(r, g=None, b=None):
    """
    Return the nearest xterm 256 color code from rgb input.
    """
    c = r if isinstance(r, list) else [r, g, b]
    best = dict()

    for index, item in enumerate(_colors):
        d = __distance(item, c)
        if(not best or d <= best.get('distance')):
            best = {'distance': d, 'index': index}

    return best.get('index', 1)


def string_to_colors(string, short=False):
    string = string.encode('utf-8')
    string = md5(string).hexdigest()[:6]  # get a random color
    color1 = rgbstring2tuple(string)
    color2 = get_opposite_color(*color1)
    if short:
        return tuple((rgb2short(*color) for color in [color1, color2]))
    return color1, color2
