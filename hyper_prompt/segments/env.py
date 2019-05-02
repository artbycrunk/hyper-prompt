from ..segment import BasicSegment


class Segment(BasicSegment):
    def activate(self):
        var_value = self.getenv(self.seg_conf["var"])
        if (not var_value and self.seg_conf.get("skip_undefined", False)):
            return
        self.append(
            " %s " % var_value,
            self.seg_conf.get("fg_color", self.theme.get("PATH_FG")),
            self.seg_conf.get("bg_color", self.theme.get("PATH_BG")))
