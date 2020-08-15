import json
import os
import re

from . import defaults, helpers


def find(args):
    for location in defaults.CONFIG_LOCATIONS:
        fullpath = os.path.expanduser(
            location.format(**vars(args)))
        if os.path.exists(fullpath):
            return fullpath
    return None


def get(args):
    config_path = find(args)
    if not config_path:
        return defaults.CONFIG

    if args.debug:
        print("Using config path: %s" % config_path)

    config = dict()
    with open(config_path) as f:
        try:
            config = json.loads(
                re.sub("//.*", "", f.read(), flags=re.MULTILINE)
            )
        except Exception as e:
            helpers.warn(
                "Config file ({0}) could not be decoded! Error: {1}".format(
                    config_path, e
                )
            )
            return defaults.CONFIG
    return config
