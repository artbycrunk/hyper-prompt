import pytest

from hyper_prompt.themes.default import DefaultColor


@pytest.mark.parametrize(
    "test, result",
    [("RESET", DefaultColor.RESET), 
     ("USERNAME_FG", DefaultColor.USERNAME_FG),
     ("TEST_FG", DefaultColor.FG),
     ("TEST_BG", DefaultColor.BG)
    ],
)
def test_get_key(test, result):
    assert DefaultColor.get(test) == result