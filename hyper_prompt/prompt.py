import os
import sys

from . import defaults, helpers


def get_valid_cwd() -> str:
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
            "Your current directory is invalid. Lowest valid directory: " + up)
    return cwd


class Prompt(object):
    def __init__(self, args, config, theme):
        self.args = args
        self.config = config
        self.theme = theme
        self.cwd = get_valid_cwd()
        self.shell_vars = defaults.SHELLS.get(self.shell, {})
        self.color_ = self.shell_vars.get("color")

        self.reset = self.color_ % '[0m'

        mode = config.get("mode", "patched")
        self.symbols = defaults.SYMBOLS.get(mode, {})
        self.segments = list()

    @property
    def shell(self):
        if hasattr(self.args, "shell"):
            return self.args.shell
        return "bash"

    def segment_conf(self, seg_name, key, default=None):
        return self.config.get(seg_name, {}).get(key, default)

    def draw(self):
        items = list()
        for idx in range(len(self.segments)):
            next_segment = None
            if idx < len(self.segments) - 1:
                next_segment = self.segments[idx + 1]
            items.append(self.segments[idx].draw(next_segment=next_segment))
        return (''.join(items) + self.reset) + ' '
