import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segments.username import Segment


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {"show_symbols": True})


def test_symbol(segment):
    assert segment.symbol("username") == "%s " % segment.SYMBOL


def test_username(segment):
    for _, value in defaults.SHELLS.items():
        user_prompt = value.get(
            "username", os.environ["USER"]
        )
        segment.hyper_prompt.shell_vars = value
        segment.activate()
        content = segment.symbol("username") + user_prompt
        assert segment.content == defaults.CONTENT % content
