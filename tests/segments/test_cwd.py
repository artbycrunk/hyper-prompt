import os

import pytest

import hyper_prompt.defaults as defaults
import hyper_prompt.helpers as helpers
import hyper_prompt.segments.cwd as cwd
from hyper_prompt.prompt import Prompt

args = {"prev_error": 0, "shell": "bash"}
ELLIPSIS = cwd.Segment.symbols.get("ellipsis", "\u2026")


@pytest.fixture
def cwd_segment():
    _importer = helpers.Importer()
    theme = _importer.import_theme("hyper_prompt.themes.default")
    hyper_prompt = Prompt(args, {}, theme)
    return cwd.Segment(hyper_prompt, {})


def test_cwd_home(cwd_segment):
    cwd_segment.hyper_prompt.cwd = os.getenv("HOME")
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % "~"

def test_cwd_root(cwd_segment):
    cwd_segment.hyper_prompt.cwd = "/"
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % "/"

@pytest.mark.parametrize(
    "cwd, result, mode",
    [
        ("/var/tmp/hyper_prompt", "hyper_prompt", "dironly"),
        ("/var/tmp/hyper_prompt", "/var/tmp/hyper_prompt", "plain"),
    ],
    ids=["dironly", "plain"],
)
def test_cwd_mode(cwd_segment, cwd, result, mode):
    cwd_segment.hyper_prompt.cwd = cwd
    cwd_segment.seg_conf["mode"] = mode
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % result


def test_cwd_maxsize(cwd_segment):
    cwd_segment.hyper_prompt.cwd = "/var/tmp/hyper_prompt"
    cwd_segment.seg_conf["max_dir_size"] = 5
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % "/var/tmp/hyper"


def test_cwd_readonly(cwd_segment):
    cwd_segment.hyper_prompt.cwd = "/var/tmp/hyper_prompt"
    cwd_segment.seg_conf["show_readonly"] = True
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % "/var/tmp/hyper_prompt"


@pytest.mark.parametrize(
    "cwd, result, depth",
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
def test_cwd_maxdepth(cwd_segment, cwd, result, depth):
    cwd_segment.hyper_prompt.cwd = cwd
    cwd_segment.seg_conf["max_depth"] = depth
    cwd_segment.setattrs()
    cwd_segment.activate()
    assert cwd_segment.content == defaults.CONTENT % result
