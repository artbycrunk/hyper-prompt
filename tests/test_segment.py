
from hyper_prompt.segment import BasicSegment
from hyper_prompt.prompt import Prompt
import hyper_prompt.helpers as helpers
import hyper_prompt.defaults as defaults
import pytest
import os


@pytest.fixture
def segment():
    _importer = helpers.Importer()
    theme = _importer.import_theme("hyper_prompt.themes.default")
    hyper_prompt = Prompt({}, {}, theme)
    return BasicSegment(hyper_prompt, {})


def test_getenv(segment):
    assert segment.getenv("USER") == os.getenv("USER")


def test_fgcolor(segment):
    assert (segment.fgcolor("00") ==
            (defaults.TEMPLATES[segment.hyper_prompt.shell] %
            ('[%s;5;%sm' % ("38", "00"))))


def test_bgcolor(segment):
    assert (segment.bgcolor("35") ==
            (defaults.TEMPLATES[segment.hyper_prompt.shell] %
            ('[%s;5;%sm' % ("48", "35"))))
