import os
import pytest

from hyper_prompt.segments.ssh import Segment

@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {"show_symbols": True})


def test_symbol(segment):
    assert segment.symbol("network") == "%s " % segment.SYMBOL


def test_ssh(segment):
    ssh_client = os.getenv("SSH_CLIENT")
    if not ssh_client:
        os.environ["SSH_CLIENT"] = "1"
    segment.activate()
    if not ssh_client:
        del os.environ["SSH_CLIENT"]
    assert segment.content.endswith(" SSH ")
