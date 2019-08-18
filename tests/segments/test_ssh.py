import pytest
import hyper_prompt.helpers as helpers
from hyper_prompt.prompt import Prompt
from hyper_prompt.segments.ssh import Segment

args = {"prev_error": 0, "shell": "bash"}

@pytest.fixture
def segment():
    _importer = helpers.Importer()
    theme = _importer.import_theme("hyper_prompt.themes.default")
    hyper_prompt = Prompt(args, {}, theme)
    return Segment(hyper_prompt, {"show_symbols":True})


def test_symbol(segment):
    assert segment.symbol("network") == '%s ' % segment.SYMBOL


def test_ssh(segment):
    segment.activate()
    assert segment.content.endswith(" SSH ")