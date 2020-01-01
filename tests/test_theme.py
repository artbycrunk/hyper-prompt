import pytest

from hyper_prompt.theme import BasicTheme

@pytest.mark.parametrize(
    "test, result",
    [("RESET", BasicTheme.RESET),
     ("TEST_FG", BasicTheme.FG),
     ("TEST_BG", BasicTheme.BG)
    ],
)
def test_get_key(test, result):
    assert BasicTheme({}).get(test) == result