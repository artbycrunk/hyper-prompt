from ..segment import BasicSegment


class Segment(BasicSegment):
    SYMBOL = "\uf817"

    def activate(self):
        if self.getenv("SSH_CLIENT"):
            content = self.symbol("network") + "SSH"
            self.append(
                self.hyper_prompt._content % (content),
                self.seg_conf.get("fg_color", self.theme.get("SSH_FG", 254)),
                self.seg_conf.get("bg_color", self.theme.get("SSH_BG", 166)),
            )
