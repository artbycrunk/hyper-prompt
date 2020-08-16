import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segments.shell import Segment


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {"show_symbols": True})


def test_symbol(segment):
    assert segment.symbol("shell") == "%s " % segment.SYMBOL

@pytest.mark.parametrize(
    "fullname",
    [
        (True),
        (False),
    ],
)
def test_shell(segment, fullname):

    segment.attr_fullname = fullname
    shellname = segment.hyper_prompt.shell
    if not segment.attr_fullname:
        shellname = shellname[0].capitalize()

    segment.activate()
    content = segment.symbol("shell") + shellname
    assert segment.content == defaults.CONTENT % content
