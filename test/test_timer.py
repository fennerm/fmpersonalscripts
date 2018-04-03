"""Test suite for timer.py."""
from pytest import mark

from bin.timer import *

@mark.parametrize('input,output', [
    ('1h30m2s', 5402),
    ('20s', 20),
    ('2h', 7200),
    ('1m', 60),
    ('1H30M2S', 5402)
])
def test_to_seconds(input, output):
    assert to_seconds(input) == output
