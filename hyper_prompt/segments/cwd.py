import os

from ..segment import BasicSegment


class Segment(BasicSegment):
    ATTRIBUTES = {
        "full_cwd": False,
        "max_depth": 5,
        "max_dir_size": False,
        "mode": False,
        "show_readonly": False,
    }

    symbols = {"cwd": "\uf07c", "cwd_home": "\uf7db", "ellipsis": "\u2026"}

    def replace_home_dir(self, cwd):
        home = os.path.realpath(self.getenv("HOME"))
        real_cwd = os.path.realpath(cwd)
        if real_cwd.startswith(home):
            return "~" + real_cwd[len(home) :]
        return cwd

    def split_path_into_names(self, cwd, sep=os.sep):
        names = cwd.split(sep)

        if names[0] == "":
            # cwd starts with /
            names = names[1:]

        if not names[0]:
            # cwd is just a /
            return [os.sep]

        return names

    def add_lock_sub_segment(self):
        segment = BasicSegment(self.hyper_prompt, self.seg_conf)
        if not os.access(self.hyper_prompt.cwd, os.W_OK):
            symbol = self.symbol("lock", {"lock": "\uf023"}).strip()
            fg, bg = (
                self.theme.get("READONLY_FG", 254),
                self.theme.get("READONLY_BG", 124),
            )
            segment.append(self.hyper_prompt._content % (symbol), fg, bg)
            self.sub_segments.append(segment)

    def activate(self):
        cwd = self.replace_home_dir(self.hyper_prompt.cwd)

        sep = os.path.sep
        if "/" in cwd:
            sep = "/"

        names = self.split_path_into_names(cwd, sep=sep)

        max_depth = self.attr_max_depth
        if max_depth > 0 and len(names) > max_depth:
            n_before = 2 if max_depth > 2 else max_depth - 1
            names = (
                names[:n_before]
                + [self.symbols.get("ellipsis")]
                + names[n_before - max_depth :]
            )

        if self.attr_mode == "dironly":
            # Only display current working dir
            names = names[-1:]

        elif self.attr_mode == "plain":
            joined = sep.join(names)

        max_size = self.attr_max_dir_size
        if not (self.attr_full_cwd or self.attr_mode == "plain"):
            mod_names = list()
            for i, name in enumerate(names):
                if max_size:
                    name = name[:max_size]
                    print(name)
                mod_names.append(name)
            joined = sep.join(mod_names)

        fg, bg = self.theme.get("CWD_FG", 254), self.theme.get("PATH_BG", 237)
        if joined.startswith("~"):
            symbol = self.symbol("cwd_home", self.symbols)
            fg, bg = (
                self.theme.get("HOME_FG", 254),
                self.theme.get("HOME_BG", 31),
            )
        else:
            symbol = self.symbol("cwd", self.symbols)
            if self.attr_mode != "dironly":
                if not joined.startswith(sep):
                    joined = sep + joined

        content = symbol + joined

        self.append(self.hyper_prompt._content % (content), fg, bg)

        if self.attr_show_readonly:
            self.add_lock_sub_segment()
