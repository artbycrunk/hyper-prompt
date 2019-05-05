class DefaultColor(object):
    RESET = -1

    BG = 35
    FG = 00

    USERNAME_FG = 250
    USERNAME_BG = 240
    USERNAME_ROOT_BG = 124

    VIRTUAL_ENV_BG = 35
    VIRTUAL_ENV_FG = 00

    @classmethod
    def get(cls, key, default=None):
        if hasattr(cls, key):
            return getattr(cls, key)
        if default:
            return default
        if key.endswith("FG"):
            return cls.FG
        if key.endswith("BG"):
            return cls.BG


class Color(DefaultColor):
    pass
