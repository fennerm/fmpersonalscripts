#!/usr/bin/env bash
## Load a default .gitignore for a python repo.
url="https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore"
if [ ! -f ".gitignore" ]; then
    wget -O ".gitignore" "$url" || curl "$url" >".gitignore"
fi
