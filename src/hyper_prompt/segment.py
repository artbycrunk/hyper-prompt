import os
import re
import threading

from . import defaults


class BasicSegment(threading.Thread):
    def __init__(self, hyper_prompt, seg_conf):
        super(BasicSegment, self).__init__()
        self.hyper_prompt = hyper_prompt
        self.seg_conf = seg_conf  # type: dict
        self.type = self.seg_conf.get("type")
        self.depends_on = self.seg_conf.get("depends_on", None)
        self.activated = False
        self.content = None
        self.sub_segments = list()
        self.setattrs()

    @property
    def theme(self):
        return self.hyper_prompt.theme

    def setattrs(self):
        if hasattr(self, "ATTRIBUTES"):
            for key, value in self.ATTRIBUTES.items():
                value = self.seg_conf.get(key, value)
                setattr(self, "attr_%s" % key, value)

    def run(self):
        self.activate()

    def activate(self):
        raise NotImplementedError

    def getenv(self, key):
        return os.getenv(key)

    def color_mode(self, code):
        mode = "5"
        if isinstance(code, (tuple, list)):
            code = ";".join([str(x) for x in code])
            mode = "2"  # rgb color
        return mode, code

    def color(self, prefix, code):
        if code is None:
            return ""
        if code == self.theme.RESET:
            return self.hyper_prompt.reset

        mode, code = self.color_mode(code)
        return self.hyper_prompt.color_ % (
            "[%s;%s;%sm" % (prefix, mode, code)
        )

    def fgcolor(self, code):
        return self.color("38", code)

    def bgcolor(self, code):
        return self.color("48", code)

    @property
    def separator(self):
        separator = self.seg_conf.get("separator", None)
        if separator:
            return defaults.SEPARATORS.get(separator, [""])[0]
        return self.hyper_prompt.separator

    def symbol(self, name, symbol_map=None):
        has_symbol = ""
        show_symbols = self.seg_conf.get("show_symbols", None)
        if show_symbols is False:
            return "%s " % has_symbol

        if show_symbols or self.hyper_prompt.show_symbols:
            has_symbol = self.hyper_prompt.symbols.get(name)
            if not has_symbol and symbol_map:
                has_symbol = symbol_map.get(name)
            if not has_symbol and hasattr(self, "SYMBOL"):
                has_symbol = self.SYMBOL
        return ("%s " % has_symbol) if has_symbol else ""

    def append(
        self, content, fg, bg, separator=None, separator_fg=None, sanitize=True
    ):

        self.fg, self.bg = fg, bg

        self.content = content
        if self.hyper_prompt.shell == "bash" and sanitize:
            content = re.sub(r"([`$])", r"\\\1", content)
        self._separator_fg = bg
        if separator is not None:
            self.separator = separator
        if separator_fg is not None:
            self._separator_fg = separator_fg

        self.activated = True

    def draw(self, next_segment=None):
        if not self.activated:
            return ""

        post_bg = self.hyper_prompt.reset
        if next_segment:
            post_bg = self.bgcolor(next_segment.bg)

        return "".join(
            (
                self.fgcolor(self.fg),
                self.bgcolor(self.bg),
                self.content,
                post_bg,
                self.fgcolor(self._separator_fg),
                self.separator,
            )
        )
