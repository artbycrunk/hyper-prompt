from __future__ import absolute_import
from ..segment import BasicSegment
import time


class Segment(BasicSegment):

    def get_time(self, time_format):
        return time.strftime(time_format)

    def activate(self):
        default_format = '%H:%M:%S'
        time_format = self.seg_conf.get('format')

        if time_format:
            time_str = ' %s ' % self.get_time(time_format)
        else:
            time_str = self.hyper_prompt.shell_vars.get(
                "time", ' %s ' % self.get_time(default_format))
        self.append(time_str,
                    self.theme.get("TIME_FG", 250),
                    self.theme.get("TIME_BG", 238))
