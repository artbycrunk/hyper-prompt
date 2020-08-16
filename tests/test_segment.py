
# -*- coding: utf-8 -*-

import os

import pytest

import hyper_prompt.defaults as defaults
from hyper_prompt.segment import BasicSegment


@pytest.fixture(name="segment")
def fixture_segment(prompt):
    return BasicSegment(prompt, {})


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
        ("48", (165, 190, 64))
    ],
)
def test_color(segment, prefix, code):
    if not code:
        assert segment.color(prefix, code) == ''

    shell_config = defaults.SHELLS[segment.hyper_prompt.shell]
    if code == "RESET":
        assert (segment.color(prefix, segment.theme.RESET) == shell_config.get("color") % ("[0m"))

    if code and code != "RESET":
        mode, code_result = segment.color_mode(code)
        assert (segment.color(prefix, code) ==
                (shell_config.get("color") % ("[%s;%s;%sm" % (prefix, mode, code_result))))


def test_separator(segment):
    assert segment.separator == segment.hyper_prompt.separator

    for key, _ in defaults.SEPARATORS.items():
        segment.seg_conf = {"separator": key}
        assert segment.separator == defaults.SEPARATORS.get(key, [""])[0]


def test_symbol(segment):
    assert segment.symbol("test") == ""

    segment.seg_conf = {"show_symbols": False}
    assert segment.symbol("test") == " "

    segment.seg_conf = {"show_symbols": True}
    segment.hyper_prompt.symbols = {"cwd": "\uf07c"}
    assert segment.symbol("cwd") == "%s " % segment.hyper_prompt.symbols.get("cwd")


def test_append(segment):
    pass