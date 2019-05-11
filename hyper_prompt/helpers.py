import importlib
import os
import sys

from . import defaults


class ModuleNotFoundException(Exception):
    pass


class Importer(object):
    def __init__(self):
        self.file_import_count = 0

    def import_theme(self, module):
        theme_mod = self._import(module, description="Theme")
        return getattr(theme_mod, "Color")

    def import_segment(self, module):
        segment_mod = self._import(module, description="Segment")
        return getattr(segment_mod, "Segment")

    def _import(self, module, description=None):
        try:
            mod = importlib.import_module(module)
        except ImportError:
            msg = "{0} {1} cannot be found".format(description, module)
            raise ModuleNotFoundException(msg)
        return mod


def ensure_dict(conf, conf_type="segment"):
    if not isinstance(conf, dict):
        conf = {"type": conf, "name": conf}
    if "module" not in conf:
        conf["module"] = "hyper_prompt.%ss.%s" % (conf_type, conf["type"])
    return conf


def warn(msg):
    print("[%s] WARN: " % defaults.NAME, msg)


def info(msg):
    print("[%s] INFO: " % defaults.NAME, msg)
