#!/bin/env bash
# Use tdrop to create a drop down terminal. Command is bound to <F12>.
# See: https://github.com/noctuid/tdrop
#      https://github.com/thestinger/termite
#
# "-P ‘wmctrl -i -r $wid -b add,above’" Sets the dropdown as always on top.
tdrop -ma -w 50% -h 100% -y -10 -P 'wmctrl -i -r $wid -b add,above' -s dropdown termite
