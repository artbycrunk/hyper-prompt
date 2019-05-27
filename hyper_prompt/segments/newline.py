from ..segment import BasicSegment


class Segment(BasicSegment):
    @property
    def separator(self):
        return ""

    def activate(self):
        FG = self.theme.get("RESET", -1)
        BG = self.theme.get("RESET", -1)
        self.append("\n", FG, BG)
