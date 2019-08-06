from socket import gethostname

from .. import colors
from ..segment import BasicSegment


class Segment(BasicSegment):
    SYMBOL = "\uf6c3"

    @property
    def hostname(self):
        if not hasattr(self, "_hostname"):
            self._hostname = gethostname()
        return self._hostname

    def activate(self):
        host_prompt = self.hyper_prompt.shell_vars.get(
            "hostname", self.hostname.split(".")[0]
        )

        content = self.symbol("hostname") + host_prompt

        if self.seg_conf.get("colorize"):
            FG, BG = colors.string_to_colors(self.hostname, short=True)
        else:
            FG = self.theme.get("HOSTNAME_FG", 250)
            BG = self.theme.get("HOSTNAME_BG", 238)
        self.append(self.hyper_prompt._content % (content), FG, BG)
