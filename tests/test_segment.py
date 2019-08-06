import os

import pytest

import hyper_prompt.defaults as defaults
import hyper_prompt.helpers as helpers
from hyper_prompt.prompt import Prompt
from hyper_prompt.segment import BasicSegment

args = {"prev_error": 0, "shell": "bash"}


@pytest.fixture
def segment():
    _importer = helpers.Importer()
    theme = _importer.import_theme("hyper_prompt.themes.default")
    hyper_prompt = Prompt(args, {}, theme)
    return BasicSegment(hyper_prompt, {})


def test_getenv(segment):
    assert segment.getenv("USER") == os.getenv("USER")


def test_fgcolor(segment):
    assert segment.fgcolor("00") == (
        defaults.SHELLS[segment.hyper_prompt.shell].get("color")
        % ("[%s;5;%sm" % ("38", "00"))
    )


def test_bgcolor(segment):
    assert segment.bgcolor("35") == (
        defaults.SHELLS[segment.hyper_prompt.shell].get("color")
        % ("[%s;5;%sm" % ("48", "35"))
    )
