import os
import sys

from . import defaults, helpers


def get_valid_cwd():
    try:
        if os.name == "nt":
            cwd = os.getcwd()
        else:
            cwd = os.getenv("PWD") or os.getcwd()
    except Exception:
        helpers.warn("Invalid current working directory!")
        sys.stdout.write("> ")
        sys.exit(1)

    parts = cwd.split(os.sep)
    up = cwd
    while parts and not os.path.exists(up):
        parts.pop()
        up = os.sep.join(parts)
    if cwd != up:
        helpers.warn(
            "Your current directory is invalid. Lowest valid directory: " + up
        )
    return cwd


class Prompt(object):
    def __init__(self, args, config, theme):
        self.args = args
        self.config = config
        self.theme = theme
        self.theme.hyper_prompt = self
        self.cwd = get_valid_cwd()
        self.shell_vars = defaults.SHELLS.get(self.shell, {})
        self.color_ = self.shell_vars.get("color")
        self._content = defaults.CONTENT

        self.reset = self.color_ % "[0m"
        self.show_symbols = config.get("show_symbols", False)

        separator = config.get("separator", "patched")
        self.separator = defaults.SEPARATORS.get(separator, [""])[0]
        self.symbols = config.get("symbols", {})
        self.segments = list()

    @property
    def shell(self):
        if hasattr(self.args, "shell"):
            return self.args.shell
        return "bash"

    def segment_conf(self, seg_name, key, default=None):
        return self.config.get(seg_name, {}).get(key, default)

    def add_segments(self, segment_threads):
        for segment in segment_threads:
            if segment.activated:
                self.segments.append(segment)
                if segment.sub_segments:
                    for sub_segment in segment.sub_segments:
                        if sub_segment.activated:
                            self.segments.append(sub_segment)

    def draw(self):
        segment_types = [segment.type for segment in self.segments]
        for segment in self.segments:
            if segment.depends_on and not segment.depends_on in segment_types:
                segment.activated = False

        active_segs = [
            segment for segment in self.segments if segment.activated
        ]
        active_segs_len = len(active_segs)

        items = list()
        for idx in range(active_segs_len):
            segment = active_segs[idx]
            next_segment = None
            if idx < active_segs_len - 1:
                next_segment = active_segs[idx + 1]
            draw = segment.draw(next_segment=next_segment)
            items.append(draw)
        concat_prompt = ("".join(items) + self.reset) + " "

        try:
            if isinstance(concat_prompt, unicode):
                return concat_prompt.encode("utf8")
        except Exception:
            return concat_prompt
