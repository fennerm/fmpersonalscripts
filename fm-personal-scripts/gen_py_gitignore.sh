#!/usr/bin/env bash
## Load a default .gitignore for a python repo.

GIG=".gitignore"
if [ ! -f "$GIG" ]; then
	URL="https://raw.githubusercontent.com/github/gitignore/master/Python.gitig"
	URL+="nore"
	wget -O "$GIG" "$URL" || curl $URL > "$GIG"
fi
