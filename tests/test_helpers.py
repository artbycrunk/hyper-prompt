import pytest

import hyper_prompt.helpers as helpers

conf = helpers.ensure_dict("test")


@pytest.mark.parametrize(
    "test, result",
    [("type", "test"), ("module", "hyper_prompt.segments.test")],
)
def test_ensure_dict(test, result):
    assert conf.get(test) == result


def test_import_exception():
    with pytest.raises(helpers.ModuleNotFoundException):
        _importer = helpers.Importer()
        _segment = _importer.import_segment("hyper_prompt.segments.not_cwd")


def test_import_segment():
    _importer = helpers.Importer()
    _segment = _importer.import_segment("hyper_prompt.segments.cwd")
    from hyper_prompt.segments.cwd import Segment

    assert Segment == _segment

@pytest.mark.parametrize(
    "mode, msg",
    [("warn", "warn testing"), ("info", "info testing")],
)
def test_warn_info(capsys, mode, msg):
    helpers.warn(msg) if mode == "warn" else helpers.info(msg)
    captured = capsys.readouterr()
    assert msg in captured.out
