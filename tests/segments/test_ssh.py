import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segments.ssh import Segment


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {"show_symbols": True})


def test_symbol(segment):
    assert segment.symbol("network") == "%s " % segment.SYMBOL

@pytest.mark.parametrize(
    "test, result",
    [
        ("1", "SSH"),
        (None, None),
    ],
)
def test_ssh(segment, test, result):
    ssh_client = os.getenv("SSH_CLIENT")
    if ssh_client:
        del os.environ["SSH_CLIENT"]
    if test:
        os.environ["SSH_CLIENT"] = test
    segment.activate()
    if ssh_client:
        os.environ["SSH_CLIENT"] = ssh_client

    if not result:
        assert segment.content is result
    else:
        content = segment.symbol("network") + result
        assert segment.content == defaults.CONTENT % content
