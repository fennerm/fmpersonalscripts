#!/usr/bin/env bash
## Set this as default application for 'file' in firefox to open directories
## ranger. TERM_EMULATOR environment variable must be set to preferred emulator.
 
PATH=${1#file://}
 
if [ -d "$PATH" ]
then
    "$TERM_EMULATOR" -e "/usr/bin/ranger $PATH" 
else
    "$TERM_EMULATOR" -e "/usr/bin/ranger --selectfile=$PATH"
fi
