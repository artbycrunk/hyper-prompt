import pytest

import hyper_prompt.colors as colors
import hyper_prompt.defaults as defaults

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
    print(colors.string_to_colors(test, short=short))
    assert colors.string_to_colors(test, short=short) == result
