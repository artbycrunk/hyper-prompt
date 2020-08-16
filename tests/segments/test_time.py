import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segments.time import Segment


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {"show_symbols": True})


def test_symbol(segment):
    assert segment.symbol("time") == "%s " % segment.SYMBOL


@pytest.mark.parametrize(
    "seg_conf",
    [
        ({}),
        ({"format": "%H:%M:%S"}),
    ],
)
def test_time(segment, seg_conf):
    segment.seg_conf = seg_conf
    segment.activate()
    time_str = segment.get_time("%H:%M:%S")
    if not seg_conf:
        time_str = segment.hyper_prompt.shell_vars.get(
            "time"
        )

    content = segment.symbol("time") + time_str
    assert segment.content == defaults.CONTENT % content
