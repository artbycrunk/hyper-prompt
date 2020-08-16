import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segments.cwd import Segment
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR

ELLIPSIS = Segment.symbols.get("ellipsis", "\u2026")


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return Segment(prompt, {})


@pytest.mark.parametrize(
    "current_cwd, result, symbols",
    [
        (os.getenv("HOME"), "~", False),
        (os.getenv("HOME"), "~", True),
        ("/", "/", False),
        ("/", "/", True),
    ],
    ids=["home-plain", "home-symbols", "root-plain", "root-symbols"],
)
def test_cwd(segment, current_cwd, result, symbols):
    segment.hyper_prompt.cwd = current_cwd
    symbol = ""
    if symbols:
        segment.hyper_prompt.show_symbols = True
        symbol_name = "cwd_home" if result == "~" else "cwd"
        symbol = segment.symbol(symbol_name, segment.symbols)
    segment.activate()
    assert segment.content == defaults.CONTENT % (symbol + result)


@pytest.mark.parametrize(
    "current_cwd, result, mode",
    [
        ("/var/tmp/hyper_prompt", "hyper_prompt", "dironly"),
        ("/var/tmp/hyper_prompt", "/var/tmp/hyper_prompt", "plain"),
    ],
    ids=["dironly", "plain"],
)
def test_cwd_mode(segment, current_cwd, result, mode):
    segment.hyper_prompt.cwd = current_cwd
    segment.seg_conf["mode"] = mode
    segment.setattrs()
    segment.activate()
    assert segment.content == defaults.CONTENT % result


@pytest.mark.parametrize(
    "current_cwd, result, max_dir_size",
    [("/var/tmp/hyper_prompt", "/var/tmp/hyper", 5)],
    ids=["size=5"],
)
def test_cwd_maxsize(segment, current_cwd, result, max_dir_size):
    segment.hyper_prompt.cwd = current_cwd
    segment.seg_conf["max_dir_size"] = max_dir_size
    segment.setattrs()
    segment.activate()
    assert segment.content == defaults.CONTENT % result


def test_cwd_readonly(segment):
    segment.hyper_prompt.cwd = "/var/tmp/hyper_prompt"
    if not os.path.exists(segment.hyper_prompt.cwd):
        os.makedirs(segment.hyper_prompt.cwd)
    segment.seg_conf["show_readonly"] = True
    segment.setattrs()

    # Make readonly and test
    os.chmod(segment.hyper_prompt.cwd, S_IREAD | S_IRGRP | S_IROTH)
    segment.activate()
    lock_segment = segment.add_lock_sub_segment()
    assert lock_segment is not None

    # Make writeable and test again
    os.chmod(segment.hyper_prompt.cwd, S_IWUSR | S_IREAD)
    segment.activate()
    lock_segment = segment.add_lock_sub_segment()
    assert lock_segment is None
    assert segment.content == defaults.CONTENT % "/var/tmp/hyper_prompt"


@pytest.mark.parametrize(
    "current_cwd, result, depth",
    [
        ("/var/tmp/hyper_prompt", "/var/%s/hyper_prompt" % ELLIPSIS, 2),
        (
            "/var/tmp/tmp/hyper_prompt",
            "/var/tmp/%s/hyper_prompt" % ELLIPSIS,
            3,
        ),
    ],
    ids=["depth=2", "depth=3"],
)
def test_cwd_maxdepth(segment, current_cwd, result, depth):
    segment.hyper_prompt.cwd = current_cwd
    segment.seg_conf["max_depth"] = depth
    segment.setattrs()
    segment.activate()
    assert segment.content == defaults.CONTENT % result
