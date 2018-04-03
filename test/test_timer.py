"""Test suite for timer.py."""
from pytest import mark

from bin.timer import *


@mark.parametrize('input,output', [
    ('1h30m2s', (1, 30, 2)),
    ('20s', (0, 0, 20)),
    ('30m', (0, 30, 0)),
    ('30M', (0, 30, 0))
])
def test_split_time_string(input, output):
    assert split_time_string(input) == output


@mark.parametrize('input,output', [
    ('1h30m2s', 5402),
    ('20s', 20),
    ('2h', 7200),
    ('1m', 60),
    ('1H30M2S', 5402)
])
def test_to_seconds(input, output):
    assert to_seconds(input) == output
