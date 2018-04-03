#!/usr/bin/env python
"""Simple timer which sends libnotify event upon completion."""
from __future__ import print_function

from datetime import timedelta
import re
from time import sleep

import click
import notify2
from notify2 import Notification


def re_to_int(regex):
    """Extract the integer portion of a regex match."""
    try:
        return int(regex.group(1))
    except AttributeError:
        return 0


def split_time_string(time_string):
    """Split time string into a tuple of form (hours, minutes, seconds)."""
    time_string = time_string.lower()
    hms = [re.search('(\d+)' + x, time_string) for x in ['h', 'm', 's']]
    hms = [re_to_int(regex) for regex in hms]
    return hms[0], hms[1], hms[2]


def to_seconds(time_string):
    """Convert a time string with hours, minutes and seconds to seconds.

    E.g to_seconds('1h30m2s') => 5402

    Parameters
    ----------
    time_string: str
        Formatted as ints with h/m/s in between. Any of h/m/s may be omitted,
        e.g '34m' is valid.

    Returns
    -------
    int
        Number of seconds.

    """
    h, m, s = split_time_string(time_string)
    seconds = timedelta(hours=h, minutes=m, seconds=s).total_seconds()
    return seconds


@click.command()
@click.option('--name', '-n', help='Name of task')
@click.argument('time_string')
def timer(time_string, name):
    """Send notification after time is complete.

    Time should be formatted with hms e.g 1h30m or 3h20m30s.
    """
    notify2.init('timer')
    print('Starting timer!')
    sleep(to_seconds(time_string))
    print('Done!')
    n = Notification('Timer finished!', name)
    n.show()


if __name__ == '__main__':
    timer()
