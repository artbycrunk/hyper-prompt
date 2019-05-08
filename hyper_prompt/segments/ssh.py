from ..segment import BasicSegment


class Segment(BasicSegment):
    def activate(self):
        if self.getenv('SSH_CLIENT'):
            self.append(' %s ' % self.symbols.get('network'),
                        self.theme.get("SSH_FG", 254),
                        self.theme.get("SSH_BG", 166))
