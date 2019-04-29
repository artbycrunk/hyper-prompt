from ..segment import BasicSegment
import os
import getpass


class Segment(BasicSegment):
    def activate(self):
        if self.hyper_prompt.shell == "bash":
            user_prompt = r" \u "
        elif self.hyper_prompt.shell == "zsh":
            user_prompt = " %n "
        else:
            user_prompt = " %s " % os.getenv("USER")

        if getpass.getuser() == "root":
            bgcolor = self.hyper_prompt.theme.USERNAME_ROOT_BG
        else:
            bgcolor = self.hyper_prompt.theme.USERNAME_BG
        self.append(user_prompt, self.hyper_prompt.theme.USERNAME_FG, bgcolor)
