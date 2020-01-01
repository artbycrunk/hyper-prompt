import os

import pytest

import hyper_prompt.defaults as defaults
import hyper_prompt.helpers as helpers
import hyper_prompt.segments.cwd as cwd
from hyper_prompt.prompt import Prompt

args = {"prev_error": 0, "shell": "bash"}
ELLIPSIS = cwd.Segment.symbols.get("ellipsis", "\u2026")


@pytest.fixture(name="cwd_segment")
def fixture_cwd_segment():
    _importer = helpers.Importer()
    _theme = _importer.import_theme("hyper_prompt.themes.default")
    theme = _theme({})
    hyper_prompt = Prompt(args, {}, theme)
    return cwd.Segment(hyper_prompt, {})


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
def test_cwd(cwd_segment, current_cwd, result, symbols):
    cwd_segment.hyper_prompt.cwd = current_cwd
    symbol = ""
    if symbols:
        cwd_segment.hyper_prompt.show_symbols = True
        symbol_name = "cwd_home" if result == "~" else "cwd"
        symbol = cwd_segment.symbol(symbol_name, cwd_segment.symbols)
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % (symbol + result)


@pytest.mark.parametrize(
    "current_cwd, result, mode",
    [
        ("/var/tmp/hyper_prompt", "hyper_prompt", "dironly"),
        ("/var/tmp/hyper_prompt", "/var/tmp/hyper_prompt", "plain"),
    ],
    ids=["dironly", "plain"],
)
def test_cwd_mode(cwd_segment, current_cwd, result, mode):
    cwd_segment.hyper_prompt.cwd = current_cwd
    cwd_segment.seg_conf["mode"] = mode
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % result


@pytest.mark.parametrize(
    "current_cwd, result, max_dir_size",
    [("/var/tmp/hyper_prompt", "/var/tmp/hyper", 5)],
    ids=["size=5"],
)
def test_cwd_maxsize(cwd_segment, current_cwd, result, max_dir_size):
    cwd_segment.hyper_prompt.cwd = current_cwd
    cwd_segment.seg_conf["max_dir_size"] = max_dir_size
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % result


def test_cwd_readonly(cwd_segment):
    cwd_segment.hyper_prompt.cwd = "/var/tmp/hyper_prompt"
    cwd_segment.seg_conf["show_readonly"] = True
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % "/var/tmp/hyper_prompt"


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
def test_cwd_maxdepth(cwd_segment, current_cwd, result, depth):
    cwd_segment.hyper_prompt.cwd = current_cwd
    cwd_segment.seg_conf["max_depth"] = depth
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % result
