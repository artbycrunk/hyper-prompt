from ..segment import BasicSegment


class Segment(BasicSegment):
    def activate(self):
        var_value = self.getenv(self.seg_conf.get("var"))
        if (not var_value and
                self.seg_conf.get("skip_undefined", False)):
            return
        content = self.symbol('env') + var_value
        self.append(
            self.hyper_prompt._content % (content),
            self.seg_conf.get("fg_color", self.theme.get("PATH_FG", 250)),
            self.seg_conf.get("bg_color", self.theme.get("PATH_BG", 237)))
