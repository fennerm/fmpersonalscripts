#!/usr/bin/env bash
## Sync my google calendar events with calcurse

LOCK="/home/fen-arch/.calcurse/caldav/lock"
[ -e "$LOCK" ] && rm "$LOCK"
/usr/bin/calcurse-caldav --init keep-remote
