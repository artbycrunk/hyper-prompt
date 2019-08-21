import getpass

from ..segment import BasicSegment


class Segment(BasicSegment):
    SYMBOL = "\uf2c0"

    def is_root(self):
        return getpass.getuser() == "root"

    def activate(self):
        user_prompt = self.hyper_prompt.shell_vars.get(
            "username", self.getenv("USER")
        )

        content = self.symbol("username") + user_prompt

        fgcolor = self.seg_conf.get("fg_color", self.theme.get("USERNAME_FG", 250))
        bgcolor = self.seg_conf.get("bg_color",
            self.theme.get("USERNAME_ROOT_BG", 124)
            if self.is_root() else self.theme.get("USERNAME_BG", 240)
        )
        self.append(self.hyper_prompt._content % (content), fgcolor, bgcolor)
