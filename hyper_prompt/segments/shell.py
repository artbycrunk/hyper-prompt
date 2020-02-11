from ..segment import BasicSegment


class Segment(BasicSegment):
    SYMBOL = "\ue7a2"

    ATTRIBUTES = {
        "fullname": False,
    }

    def activate(self):
        shellname = self.hyper_prompt.shell
        if not self.attr_fullname:
            shellname = shellname[0].capitalize()

        content = self.symbol("shell") + shellname
        self.append(
            self.hyper_prompt._content % (content),
            self.seg_conf.get("fg_color", self.theme.get("SHELL_FG", 254)),
            self.seg_conf.get("bg_color", self.theme.get("SHELL_BG", 236)),
        )
