import hyper_prompt.colors as colors
import pytest

@pytest.mark.parametrize(
    'test, result', [
        ((18, 52, 86), 23),
        ((255, 255, 255), 231),
        ((13, 173, 214), 38),
        ((255, 215, 215), 224)
    ]
)
def test_rgb2short(test, result):
    assert colors.rgb2short(*test) == result

@pytest.mark.parametrize(
    'test, result, short', [
        ('hyper-prompt', ((158, 27, 204), (94, 161, 157)), False),
        ('hyper-prompt', ((128, 73)), True)
    ]
)
def test_string_to_colors(test, result, short):
    assert colors.string_to_colors(test, short=short) == result
