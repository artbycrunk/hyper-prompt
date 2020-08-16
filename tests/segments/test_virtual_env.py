import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segments.virtual_env import Segment


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {"show_symbols": True})


def test_symbol(segment):
    assert segment.symbol("venv") == "%s " % segment.SYMBOL


@pytest.mark.parametrize(
    "test, result",
    [
        ("/var/tmp/hyper_prompt", "hyper_prompt"),
        ("/var/tmp/hyper_prompt/.venv", "hyper_prompt"),
        (None, None),
    ],
)
def test_venv(segment, test, result):
    venv = os.getenv("VIRTUAL_ENV")
    if venv:
        del os.environ["VIRTUAL_ENV"]
    if test:
        os.environ["VIRTUAL_ENV"] = test
    segment.activate()
    if venv:
        os.environ["VIRTUAL_ENV"] = venv

    if not result:
        assert segment.content is result
    else:
        content = segment.symbol("venv") + result
        assert segment.content == defaults.CONTENT % content
