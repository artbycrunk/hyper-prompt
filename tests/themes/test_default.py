import pytest

from hyper_prompt.themes.default import Theme


@pytest.mark.parametrize(
    "test, result",
    [("RESET", Theme.RESET), 
     ("USERNAME_FG", Theme.USERNAME_FG),
     ("TEST_FG", Theme.FG),
     ("TEST_BG", Theme.BG)
    ],
)
def test_get_key(test, result):
    assert Theme({}).get(test) == result