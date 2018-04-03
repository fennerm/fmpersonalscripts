#!/usr/bin/env bash
## Upload a PKGBUILD to the aur
## Run from the PKGBUILD directory

printf "Initializing git repo...\\n"
pkgname="${PWD##*/}"
git remote add "$pkgname" "ssh://aur@aur.archlinux.org/${pkgname}.git"
git fetch "$pkgname"

printf "Uploading PKGBUILD...\\n"
makepkg --printsrcinfo > .SRCINFO
git add PKGBUILD .SRCINFO
git commit -m "Initial commit to AUR"
git push
cd ..
git add "${pkgname}/PKGBUILD"
git commit -m "Autoupdated PKGBUILD"
cd "$pkgname"
