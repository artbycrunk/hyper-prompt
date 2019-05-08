import os

from ..segment import BasicSegment

ELLIPSIS = u'\u2026'


class Segment(BasicSegment):

    def replace_home_dir(self, cwd):
        home = os.path.realpath(self.getenv('HOME'))
        real_cwd = os.path.realpath(cwd)
        if real_cwd.startswith(home):
            return '~' + real_cwd[len(home):]
        return cwd

    def split_path_into_names(self, cwd, sep=os.sep):
        names = cwd.split(sep)

        if names[0] == '':
            names = names[1:]

        if not names[0]:
            return [os.sep]

        return names

    def activate(self):
        cwd = self.replace_home_dir(self.hyper_prompt.cwd)

        sep = os.path.sep
        if '/' in cwd:
            sep = '/'

        names = self.split_path_into_names(cwd, sep=sep)

        full_cwd = self.seg_conf.get("full_cwd", False)
        max_depth = self.seg_conf.get("max_depth", 5)
        max_size = self.seg_conf.get("max_dir_size", False)
        mode = self.seg_conf.get("mode")

        if max_depth > 0 and len(names) > max_depth:
            n_before = 2 if max_depth > 2 else max_depth - 1
            names = names[:n_before] + [ELLIPSIS] + names[n_before - max_depth:]

        if mode == "dironly":
            # Only display current working dir
            names = names[-1:]

        elif mode == "plain":
            joined = sep.join(names)

        if not (full_cwd or mode == "plain"):
            mod_names = list()
            for i, name in enumerate(names):
                if max_size:
                    name = name[:max_size]
                    print(name)
                mod_names.append(name)
            joined = sep.join(mod_names)

        fg, bg = self.theme.get("CWD_FG", 254), self.theme.get("PATH_BG", 237)
        if joined.startswith("~"):
            fg, bg = (self.theme.get("HOME_FG", 254),
                      self.theme.get("HOME_BG", 31))
        else:
            if mode != "dironly":
                if not joined.startswith(sep):
                    joined = sep + joined

        self.append(self.hyper_prompt._content % (joined), fg, bg)
