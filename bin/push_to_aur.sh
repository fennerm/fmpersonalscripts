#!/usr/bin/bash
set -euo pipefail
IFS=$'\n\t'
makepkg --printsrcinfo > .SRCINFO
git add PKGBUILD .SRCINFO
git commit -m "$1"
git push origin master
