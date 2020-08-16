from hashlib import md5

import pytest

import hyper_prompt.colors as colors
import hyper_prompt.defaults as defaults


@pytest.mark.parametrize(
    "test, result",
    [
        ("hyper-prompt", (158, 27, 204)),
        ("hyper-prompt-test", (187, 212, 171)),
    ],
)
def test_hex2rgb2hex(test, result):
    input_string = md5(test.encode("utf-8")).hexdigest()[:6]
    rgb = tuple(colors.__hex2rgb(input_string))
    assert result == rgb

    _hex = colors.__rgb2hex(rgb)
    assert _hex == input_string


@pytest.mark.parametrize(
    "test, result",
    [
        ((18, 52, 86), 23),
        ((255, 255, 255), 231),
        ((13, 173, 214), 38),
        ((255, 215, 215), 224),
    ],
)
def test_rgb2lut(test, result):
    lut = colors.rgb2lut(*test)
    assert lut == defaults.COLOR_LUT[result]

@pytest.mark.parametrize(
    "test, result, short",
    [
        ("hyper-prompt", ((175, 0, 215), (64, 189, 191)), False),
        ("hyper-prompt", ((128, 73)), True),
    ],
)
def test_string_to_colors(test, result, short):
    # print(colors.string_to_colors(test, short=short))
    assert colors.string_to_colors(test, short=short) == result
