from ..segment import BasicSegment
import os
import getpass


class Segment(BasicSegment):
    def activate(self):
        user_prompt = " %s " % os.getenv("USER")
        if self.hyper_prompt.shell == "bash":
            user_prompt = r" \u "
        elif self.hyper_prompt.shell == "zsh":
            user_prompt = " %n "

        bgcolor = self.theme.get("USERNAME_BG")
        fgcolor = self.theme.get("USERNAME_FG")
        if getpass.getuser() == "root":
            bgcolor = self.theme.get("USERNAME_ROOT_BG")

        self.append(user_prompt, fgcolor, bgcolor)
