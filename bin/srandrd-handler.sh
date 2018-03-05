#!/usr/bin/env bash
## Configure automatic xrandr configuration for dual monitors + projector

set -x
# Parameters for primary display
dpi="92"
scale="0.45x0.45"
external_monitors_id="F022318301010101"
projector_id="7436003000000001"

# Get the status of a connection from xrandr
# $1 - Connection type (e.g HDMI-1, EDP-1)
get_connection() {
    connection_type="$1"
    connection="$(xrandr | grep "$connection_type" | grep " connected" | \
    sed -e "s/\([A-Z0-9]\+\) connected.*/\1/")"
    echo "$connection"
}

internal_monitor="$(get_connection "eDP-1")"
external1="$(get_connection "HDMI-1")"
external2="$(get_connection "DP-2")"

display="$( echo "$SRANDRD_ACTION" | awk '{print $1;}' )"

if [[ "$SRANDRD_ACTION" =~ .*disconnected.* ]]; then
    xrandr --output "$display" --off \
        --output "$internal_monitor" --dpi "$dpi" --scale "$scale"
elif [[ "$SRANDRD_EDID" == "$projector_id" ]]; then
    xrandr --output "$display" --mode 800x600
elif [[ "$SRANDRD_EDID" == "$external_monitors_id" ]]; then
    if [ "$external1" ] && [ "$external2" ]; then
        xrandr --output "$internal_monitor" --off \
            --output "$external1" --auto \
            --output "$external2" --auto --right-of "$external1"
    fi
fi
