from . import defaults


class BasicTheme(object):
    RESET = -1

    BG = (0, 175, 95)
    FG = (0, 0, 0)

    def __init__(self, theme_conf):
        self.theme_conf = theme_conf  # type: dict
        self.hyper_prompt = None

    # @classmethod
    def get(self, key, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        if default:
            return default
        if key.endswith("FG"):
            return self.FG
        if key.endswith("BG"):
            return self.BG
        return None
