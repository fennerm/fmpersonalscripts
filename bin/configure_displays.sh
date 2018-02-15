#!/usr/bin/env bash
## Configure automatic xrandr configuration for dual monitors / projector

# Paramaters for primary display
dpi="92"
scale="0.45x0.45"

monitor1="$(xrandr | grep "eDP" | grep " connected" | \
    sed -e "s/\([A-Z0-9]\+\) connected.*/\1/")"
monitor2="$(xrandr | grep "HDMI" | grep " connected" | \
    sed -e "s/\([A-Z0-9]\+\) connected.*/\1/")"
monitor3="$(xrandr | grep "HDMI" | grep " connected" | \
    sed -e "s/\([A-Z0-9]\+\) connected.*/\1/")"

projector_connected="$(xrandr | grep "800x840")"
dual_monitors_connected="$(xrandr | grep "$monitor3 connected")"

if [ "$dual_monitors_connected" ]; then
    xrandr --output "$monitor1" --off \
        --output "$monitor2" --auto --output "$monitor3" --auto
elif [ "$projector_connected" ]; then
    xrandr --output "$monitor2" --mode 800x840
else
    xrandr --output "$monitor1" --output "$monitor1" --auto \
        --output "$monitor2" --off --output "$monitor3" --off
    xrandr --output "$monitor1" --dpi "$dpi" --scale "$scale"
fi
