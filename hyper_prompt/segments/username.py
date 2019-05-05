from ..segment import BasicSegment
import getpass


class Segment(BasicSegment):
    def is_root(self):
        return getpass.getuser() == "root"

    def activate(self):
        user_prompt = self.hyper_prompt.shell_vars.get(
            "username", " %s " % self.getenv("USER"))

        fgcolor = self.theme.get("USERNAME_FG", 250)
        bgcolor = (self.theme.get("USERNAME_ROOT_BG", 124) if
                   self.is_root() else
                   self.theme.get("USERNAME_BG", 240))

        self.append(user_prompt, fgcolor, bgcolor)
