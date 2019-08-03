from ..segment import BasicSegment


class Segment(BasicSegment):
    @property
    def separator(self):
        return ""

    def activate(self):
        newline = self.hyper_prompt.shell_vars.get("newline", '')
        FG = self.theme.get("RESET", -1)
        BG = self.theme.get("RESET", -1)
        self.append(newline, FG, BG)