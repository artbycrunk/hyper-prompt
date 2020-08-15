from hashlib import md5
from math import sqrt

from . import defaults


def __hex2rgb(hexa):
    return [int(hexa[i : i + 2], 16) for i in (0, 2, 4)]


def __rgb2hex(r, g=None, b=None):
    color = r if isinstance(r, tuple) else (r, g, b)
    return "%02x%02x%02x" % color


def __distance(a, b):
    x = (a[0] - b[0]) ** 2
    y = (a[1] - b[1]) ** 2
    z = (a[2] - b[2]) ** 2
    return sqrt(x + y + z)


def rgb2lut(r, g=None, b=None):
    """
    Return the nearest color from LUT given an rgb input.
    """
    color = r if isinstance(r, list) else [r, g, b]
    best = dict()
    for item in defaults.COLOR_LUT:
        distance = __distance(item[2], color)
        if not best or distance <= best.get("distance"):
            best = {"distance": distance, "value": item}
    return best.get("value", defaults.COLOR_LUT[1])


def string_to_colors(input_string, short=False):
    input_string = md5(input_string.encode("utf-8")).hexdigest()[:6]
    rgb = tuple(__hex2rgb(input_string))
    lut = rgb2lut(*rgb)
    if short:
        return (lut[0], lut[4])
    return lut[2], lut[3]
