#!/usr/bin/env bash
## Purely for use with `emacsclient` on server for which emacs cannot detect the
## home folder
## See https://emacs.stackexchange.com/a/8089/5444
emacs -nw -q -l ~/.emacs.d/init.el
