import re
import os


class BasicSegment(object):
    def __init__(self, hyper_prompt, seg_conf):
        self.hyper_prompt = hyper_prompt
        self.seg_conf = seg_conf  # type: dict
        self.type = self.seg_conf["type"]
        self.activated = False

    def start(self):
        self.activate()

    def activate(self):
        pass

    def getenv(self, key):
        return os.getenv(key)

    def color(self, prefix, code):
        if code is None:
            return ''
        elif code == self.hyper_prompt.theme.RESET:
            return self.hyper_prompt.reset
        else:
            return self.hyper_prompt.color_template % (
                '[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, content, fg, bg,
               separator=None, separator_fg=None, sanitize=True):

        self.fg, self.bg = fg, bg

        self.content = content
        if self.hyper_prompt.args.shell == "bash" and sanitize:
            content = re.sub(r"([`$])", r"\\\1", content)

        self.separator = self.hyper_prompt.separator
        self._separator_fg = bg
        if separator is not None:
            self.separator = separator
        if separator_fg is not None:
            self._separator_fg = separator_fg

        self.activated = True

    def draw(self, next_segment=None):
        if not self.activated:
            return ''

        post_bg = self.hyper_prompt.reset
        if next_segment:
            post_bg = self.bgcolor(next_segment.bg)

        return ''.join((
            self.fgcolor(self.fg),
            self.bgcolor(self.bg),
            self.content,
            post_bg,
            self.fgcolor(self._separator_fg),
            self.separator))
