#!/usr/bin/env python
"""Symlink all dotfiles in the data/dotfiles repo to the home directory"""
from __future__ import print_function
from warnings import warn

from plumbum import local

def symlink_dir(d, base):
    """Symlink a config directory

    If the target exists, emit a warning. Otherwise link all the contained
    config files, creating directories as necessary

    Parameters
    ----------
    d: local.path
        Directory to be linked
    base: local.path
        Directory to link into
    """
    if not d.name == '.git':
        base = base / d.name
        if not base.exists():
            base.mkdir()
        for f in d.list():
            symlink_dotfile(f, base)

def symlink_dotfile(f, base):
    """Symlink a config file

    If the target exists, emit a warning. Otherwise symlink `f` into `base`

    Parameters
    ----------
    f: local.path
        Directory to be linked
    base: local.path
        Directory to link into
    """
    if f.is_dir():
        symlink_dir(f, base)
    else:
        dest = base / f.name
        if dest.is_symlink():
            dest.unlink()
        if dest.exists():
            warn("DOTFILE WARNING: Conficting file present at " + dest)
        else:
            f.symlink(dest)

def symlink_all_dotfiles(dots, home):
    """Symlink all dotfiles into the home directory

    Parameters
    ----------
    dots: local.path
        The directory containing the dotfiles.
    home: local.path
        The home directory
    """
    for f in dots.list():
        symlink_dotfile(f, home)


if __name__ == "__main__":
    # Grab arguments from environment variables
    dots = local.path(local.env["DOTS"])
    home = local.path(local.env["HOME"])
    symlink_all_dotfiles(home=home, dots=dots)
