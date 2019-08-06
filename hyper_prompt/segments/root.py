from ..segment import BasicSegment


class Segment(BasicSegment):
    def activate(self):
        root = self.hyper_prompt.shell_vars.get("root", "")
        content = self.symbol("root") + root

        bg = self.theme.get("CMD_PASSED_BG", 236)
        fg = self.theme.get("CMD_PASSED_FG", 15)
        if self.hyper_prompt.args.prev_error != 0:
            fg = self.theme.get("CMD_FAILED_FG", 15)
            bg = self.theme.get("CMD_FAILED_BG", 161)
        self.append(
            self.hyper_prompt._content % (content), fg, bg, sanitize=False
        )
