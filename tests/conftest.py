import argparse
import pytest
import hyper_prompt.helpers as helpers
from hyper_prompt.prompt import Prompt


@pytest.fixture(name="args")
def fixture_args():
    args = argparse.Namespace()
    args.prev_error = 0
    args.shell = "bash"
    args.showall = None
    args.separator = None
    return args


@pytest.fixture(name="importer")
def fixture_importer(args):
    return helpers.Importer()


@pytest.fixture(name="prompt")
def fixture_prompt(importer, args):
    _theme = importer.import_theme("hyper_prompt.themes.default")
    theme = _theme({})
    return Prompt(args, {}, theme)
