import pytest

import hyper_prompt.helpers as helpers

@pytest.mark.parametrize(
    "test, key, result",
    [
        ("test", "type", "test"),
        ("test", "module", "hyper_prompt.segments.test"),
        ({"type": 'test', "name": 'test'}, "module", "hyper_prompt.segments.test"),
        ({"module":"test"}, "module", "test")
    ],
)
def test_ensure_dict(test, key, result):
    conf = helpers.ensure_dict(test)
    assert conf.get(key) == result


def test_import_exception(importer):
    with pytest.raises(helpers.ModuleNotFoundException):
        importer.import_segment("hyper_prompt.segments.not_cwd")


def test_import_segment(importer):
    _segment = importer.import_segment("hyper_prompt.segments.cwd")
    from hyper_prompt.segments.cwd import Segment

    assert Segment == _segment

@pytest.mark.parametrize(
    "mode, msg",
    [("warn", "warn testing"), ("info", "info testing")],
)
def test_warn_info(capsys, mode, msg):
    if mode == "warn":
        helpers.warn(msg)
    else:
        helpers.info(msg)
    captured = capsys.readouterr()
    assert msg in captured.out
