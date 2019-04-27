import json
import os

from . import defaults, helpers


def find():
    for location in defaults.CONFIG_LOCATIONS:
        fullpath = os.path.expanduser(location)
        if os.path.exists(fullpath):
            return fullpath


def get():
    config = dict()
    config_path = find()
    if config_path:
        with open(config_path) as f:
            try:
                config = json.loads(f.read())
            except Exception as e:
                helpers.warn(
                    "Config file ({0}) could not be decoded! Error: {1}".format(config_path, e))
                config = defaults.CONFIG
    else:
        config = defaults.CONFIG
    return config
