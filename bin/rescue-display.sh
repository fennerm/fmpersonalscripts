#!/usr/bin/env bash
## Restore the primary display in case the xrandr autoconfiguration script fails

xrandr --output "$monitor1" --auto 
