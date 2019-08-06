from __future__ import absolute_import

import time

from ..segment import BasicSegment


class Segment(BasicSegment):
    SYMBOL = "\ufa1e"

    def get_time(self, time_format):
        return time.strftime(time_format)

    def activate(self):
        default_format = "%H:%M:%S"
        time_format = self.seg_conf.get("format")

        if time_format:
            time_str = self.get_time(time_format)
        else:
            time_str = self.hyper_prompt.shell_vars.get(
                "time", self.get_time(default_format)
            )
        content = self.symbol("time") + time_str
        self.append(
            self.hyper_prompt._content % (content),
            self.theme.get("TIME_FG", 250),
            self.theme.get("TIME_BG", 238),
        )

