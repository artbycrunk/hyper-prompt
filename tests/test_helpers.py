import pytest

import hyper_prompt.helpers as helpers

conf = helpers.ensure_dict("test")


@pytest.mark.parametrize(
    "test, result",
    [("type", "test"), ("module", "hyper_prompt.segments.test")],
)
def test_ensure_dict(test, result):
    assert conf.get(test) == result
