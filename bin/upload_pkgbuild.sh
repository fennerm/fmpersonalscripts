#!/usr/bin/env bash
## Upload a PKGBUILD to the aur
## Run from the PKGBUILD directory

printf "Uploading PKGBUILD...\\n"
makepkg --printsrcinfo > .SRCINFO
git add -f PKGBUILD .SRCINFO
git commit -m "Initial commit to AUR"
git push
cd ..
git add "${pkgname}/PKGBUILD"
git commit -m "Autoupdated PKGBUILD"
cd "$pkgname"