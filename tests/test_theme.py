import pytest

from hyper_prompt.theme import BasicTheme

@pytest.mark.parametrize(
    "test, result, default",
    [
        ("RESET", BasicTheme.RESET, None),
        ("FG", BasicTheme.FG, None),
        ("BG", BasicTheme.BG, None),
        ("TEST_FG", BasicTheme.FG, None),
        ("TEST_BG", BasicTheme.BG, None),
        ("NEW_BG", 'hello', 'hello'),
        ("NEW_VALUE", None, None),
    ]
)
def test_get_key(test, result, default):
    assert BasicTheme({}).get(test, default) == result
