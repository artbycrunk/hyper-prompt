
# -*- coding: utf-8 -*-

import os

import pytest
import sys

import hyper_prompt.defaults as defaults
import hyper_prompt.helpers as helpers
from hyper_prompt.prompt import Prompt
from hyper_prompt.segment import BasicSegment

args = {"prev_error": 0, "shell": "bash"}


@pytest.fixture(name="segment")
def fixture_segment():
    _importer = helpers.Importer()
    theme = _importer.import_theme("hyper_prompt.themes.default")
    hyper_prompt = Prompt(args, {}, theme)
    return BasicSegment(hyper_prompt, {})


def test_getenv(segment):
    assert segment.getenv("USER") == os.getenv("USER")


@pytest.mark.parametrize(
    "content, fg, bg",
    [
        ("Test", 15, 161),
        ("Host", 220, 80)
    ],
)
def test_draw(segment, content, fg, bg):
    segment.append(content=content, fg=fg, bg=bg)
    prompt = r'\[\e[38;5;%sm\]\[\e[48;5;%sm\]%s\[\e[0m\]\[\e[38;5;%sm\]' % (
        fg, bg, content, bg)
    assert segment.draw().startswith(prompt)


def test_activate(segment):
    with pytest.raises(NotImplementedError):
        segment.run()

@pytest.mark.parametrize(
    "prefix, code",
    [
        ("38", "00"),
        ("48", "35"),
        ("38", None),
        ("48", 'RESET'),
    ],
)
def test_color(segment, prefix, code):
    if not code:
        assert segment.color(prefix, code) == ''

    elif code == "RESET":
        assert (segment.color(prefix, segment.theme.RESET) == 
        (defaults.SHELLS[segment.hyper_prompt.shell].get("color") % ("[0m")))

    else:
        assert (segment.color(prefix, code) == 
         (defaults.SHELLS[segment.hyper_prompt.shell].get("color") 
                % ("[%s;5;%sm" % (prefix, code))))
