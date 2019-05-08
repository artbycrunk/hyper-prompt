from socket import gethostname

from .. import colors
from ..segment import BasicSegment


class Segment(BasicSegment):
    @property
    def hostname(self):
        if not hasattr(self, "_hostname"):
            self._hostname = gethostname()
        return self._hostname

    def activate(self):
        host_prompt = self.hyper_prompt.shell_vars.get(
            "hostname", " %s " % self.hostname.split(".")[0])
        if self.seg_conf.get("colorize"):
            FG, BG = colors.string_to_colors(self.hostname, short=True)
        else:
            FG = self.theme.get("HOSTNAME_FG", 250)
            BG = self.theme.get("HOSTNAME_BG", 238)
        self.append(host_prompt, FG, BG)
