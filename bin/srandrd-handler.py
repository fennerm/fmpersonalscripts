#!/usr/bin/env python
'''Automatically configure xrandr for dual monitors + projector with srandrd'''
import logging
from logging import info
import os
import sys

from plumbum import (
    BG,
    local,
    ProcessExecutionError,
)
from plumbum.cmd import (
    rg,
    xrandr,
)

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))

SRANDRD_ACTION = os.environ['SRANDRD_ACTION']
SRANDRD_EDID = os.environ['SRANDRD_EDID']

LAUNCH_POLYBAR = local['~/dotfiles/polybar/.config/polybar/launch.sh']

INTERNAL = {
    'output': 'eDP-1',
    'flags': ['--dpi', '192', '--mode', '1920x1080']
}

EXTERNAL_MONITOR1 = {
    'output': 'HDMI-1',
    'edid': 'F022318301010101',
    'flags': ['--auto']
}

EXTERNAL_MONITOR2 = {
    'output': 'DP-2',
    'edid': 'F022318301010101',
    'flags': ['--right-of', EXTERNAL_MONITOR1['output'], '--auto']
}

PROJECTOR = {
    'output': 'HDMI-1',
    'edid': '7436003000000001',
    'flags': ['--mode', '800x600']
}


def is_connected(device):
    '''Test whether a given display output is connected'''
    try:
        (xrandr | rg['-i', device['output'] + ' connected'])()
        return True
    except ProcessExecutionError:
        return False


def external_monitor_connected():
    return SRANDRD_EDID in [EXTERNAL_MONITOR1['edid'], EXTERNAL_MONITOR2['edid']]


def display_was_disconnected():
    return 'disconnected' in SRANDRD_ACTION


def projector_connected():
    return SRANDRD_EDID in PROJECTOR['edid']


def enable(device):
    xrandr_args = ['--output', device['output']] + device['flags']
    xrandr.__getitem__(xrandr_args)()


def disable(device):
    xrandr('--output', device['output'], '--off')


def main():
    if display_was_disconnected():
        if (not is_connected(EXTERNAL_MONITOR1) and
                not is_connected(EXTERNAL_MONITOR2)):
            info('All external display(s) disconnected, disabling...')
            disable(EXTERNAL_MONITOR1)
            disable(EXTERNAL_MONITOR2)
            enable(INTERNAL)
            info('External display(s) successfully disabled...')
            info('Relaunching polybar...')
            LAUNCH_POLYBAR & BG
        else:
            info('External display disconnected, but not disabling yet because '
                 'other external display is still connected')
            info('-> SRANDRD_ACTION = %s', SRANDRD_ACTION)

    else:
        if external_monitor_connected():
            if (is_connected(EXTERNAL_MONITOR1) and
                    is_connected(EXTERNAL_MONITOR2)):
                info('Both external monitors connected, enabling them...')
                enable(EXTERNAL_MONITOR1)
                enable(EXTERNAL_MONITOR2)
                disable(INTERNAL)
                info('Successfully enabled external monitors')
                info('Relaunching polybar...')
                LAUNCH_POLYBAR & BG
            else:
                info('New display detected, waiting for extra displays...')
        elif projector_connected():
            info('Projector connected, enabling...')
            enable(PROJECTOR)
            info('Projector successfully enabled')


if __name__ == '__main__':
    main()
    sys.exit()
