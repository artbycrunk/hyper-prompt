import os
import re
import subprocess

from ..segment import BasicSegment


class Repo(object):
    symbols = {
        'detached': u'\u2693',
        'ahead': u'\u2B06',
        'behind': u'\u2B07',
        'staged': u'\u2714',
        'changed': u'\u270E',
        'new': u'?',
        'conflicted': u'\u273C',
        'stash': u'\u2398',
        'git': u'\uE0A0'
    }

    def __init__(self):

        self.attrs = ["new", "changed", "staged", "conflicted", "active",
                      "ahead", "behind", "conflicted", "branch", "remote"]
        for attr in self.attrs:
            setattr(self, attr, 0)
        self.status()

    @property
    def dirty(self):
        return sum([getattr(self, attr) for attr in self.attrs[:4]]) > 0

    def __str__(self):

        return str({attr: getattr(self, attr) for attr in self.attrs})

    def status(self):
        try:
            proc = subprocess.Popen(['git', 'status', '--porcelain', '-b'],
                                    stdout=subprocess.PIPE)
        except OSError:
            return (None, None)

        data = proc.communicate()
        if proc.returncode != 0:
            return (None, None)

        status = data[0].decode("utf-8").splitlines()

        for statusline in status[1:]:
            code = statusline[:2]
            if code == '??':
                self.new += 1
            elif code in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):
                self.conflicted += 1
            else:
                if code[1] != ' ':
                    self.changed += 1
                if code[0] != ' ':
                    self.staged += 1

        info = re.search('^## (?P<local>\S+?)''(\.{3}(?P<remote>\S+?)( \[(ahead (?P<ahead>\d+)(, )?)?(behind (?P<behind>\d+))?\])?)?$', status[0])
        branch = info.groupdict() if info else {}

        self.ahead = branch.get("ahead", 0)
        self.behind = branch.get("behind", 0)
        self.branch = branch.get("local", '')
        self.remote = branch.get("remote", '')

        self.active = True


class Segment(BasicSegment):

    def is_gitdir(self, cwd):
        found = False
        _cwd = cwd
        while cwd != '/':
            if os.access(".git", os.R_OK):
                found = True
                self.git_dir = cwd
                break
            _cwd = os.getcwd()
            os.chdir('..')
            cwd = os.getcwd()
            if cwd == _cwd:
                break
        os.chdir(self.hyper_prompt.cwd)
        return found

    def add_sub_segment(self, key, fg, bg):
        segment = BasicSegment(self.hyper_prompt, self.seg_conf)
        value = getattr(self.repo, key)
        if value:
            name = str(value) if int(value) > 1 else u''
            content = name + self.repo.symbols.get(key)
            segment.append(self.hyper_prompt._content % (content), fg, bg)
            self.sub_segments.append(segment)

    def activate(self):
        if self.is_gitdir(self.hyper_prompt.cwd):
            self.repo = Repo()
            if self.repo.active:
                fg, bg = (self.theme.get("REPO_CLEAN_FG", 0),
                          self.theme.get("REPO_CLEAN_BG", 148))
                if self.repo.dirty:
                    fg, bg = (self.theme.get("REPO_DIRTY_FG", 15),
                              self.theme.get("REPO_DIRTY_BG", 161))
                symbol = ""
                if self.seg_conf.get("show_symbol", False):
                    symbol = "%s " % self.repo.symbols.get("git")

                content = symbol + self.repo.branch
                self.append(self.hyper_prompt._content % (content), fg, bg)

                self.add_sub_segment('ahead',
                                     self.theme.get("GIT_AHEAD_FG", 250),
                                     self.theme.get("GIT_AHEAD_BG", 240))
                self.add_sub_segment('behind',
                                     self.theme.get("GIT_BEHIND_FG", 250),
                                     self.theme.get("GIT_BEHIND_BG", 240))
                self.add_sub_segment('staged',
                                     self.theme.get("GIT_STAGED_FG", 15),
                                     self.theme.get("GIT_STAGED_BG", 22))
                self.add_sub_segment('changed',
                                     self.theme.get("GIT_NOTSTAGED_FG", 15),
                                     self.theme.get("GIT_NOTSTAGED_BG", 130))
                self.add_sub_segment('new',
                                     self.theme.get("GIT_UNTRACKED_FG", 15),
                                     self.theme.get("GIT_UNTRACKED_BG", 52))
                self.add_sub_segment('conflicted',
                                     self.theme.get("GIT_CONFLICTED_FG", 15),
                                     self.theme.get("GIT_CONFLICTED_BG", 9))
