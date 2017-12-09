#!/usr/bin/env python
"""Symlink all dotfiles in the data/dotfiles repo to the home directory"""
from __future__ import print_function
from warnings import warn

from plumbum import local

def is_excluded(f, mint_only, arch_only):
    """Test if a file should be excluded from linking

    Parameters
    ----------
    f: local.path
        File/directory to be linked
    mint_only: List[str]
        List of files or directories which should not be linked for Linux Mint
    arch_only: List[str]
        List of files or directories which should not be linked for Arch

    Returns
    -------
    bool
        True if should be excluded
    """
    os = local.env['OS']
    if os == 'arch' and (str(f) in mint_only):
        excluded = True
    elif os == 'mint' and (str(f) in arch_only):
        excluded = True
    else:
        excluded = False
    return excluded

def symlink_dir(d, base, mint_only, arch_only):
    """Symlink a config directory

    If the target exists, emit a warning. Otherwise link all the contained
    config files, creating directories as necessary

    Parameters
    ----------
    d: local.path
        Directory to be linked
    base: local.path
        Directory to link into
    mint_only: List[str]
        List of files or directories which should not be linked for Linux Mint
    arch_only: List[str]
        List of files or directories which should not be linked for Arch
    """
    if not d.name == '.git':
        base = base / d.name
        if not base.exists():
            base.mkdir()
        for f in d.list():
            symlink_dotfile(f, base, mint_only, arch_only)

def symlink_dotfile(f, base, mint_only, arch_only):
    """Symlink a config file

    If the target exists, emit a warning. Otherwise symlink `f` into `base`

    Parameters
    ----------
    f: local.path
        Directory to be linked
    base: local.path
        Directory to link into
    mint_only: List[str]
        List of files or directories which should not be linked for Linux Mint
    arch_only: List[str]
        List of files or directories which should not be linked for Arch
    """
    if f.is_dir():
        symlink_dir(f, base, mint_only, arch_only)
    else:
        if not is_excluded(f, mint_only, arch_only):
            dest = base / f.name
            if dest.is_symlink():
                dest.unlink()
            if dest.exists():
                warn("DOTFILE WARNING: Conficting file present at " + dest)
            else:
                f.symlink(dest)

def symlink_all_dotfiles(dots, home, mint_only, arch_only):
    """Symlink all dotfiles into the home directory

    Parameters
    ----------
    dots: local.path
        The directory containing the dotfiles.
    home: local.path
        The home directory
    mint_only: List[str]
        List of files or directories which should not be linked for Linux Mint
    arch_only: List[str]
        List of files or directories which should not be linked for Arch
    """
    for f in dots.list():
        symlink_dotfile(f, home, mint_only, arch_only)


if __name__ == "__main__":
    # Grab arguments from environment variables
    dots = local.path(local.env["DOTS"])
    home = local.path(local.env["HOME"])
    arch_only = local.env["ARCH_ONLY"].split(':')
    mint_only = local.env["MINT_ONLY"].split(':')
    symlink_all_dotfiles(home=home, dots=dots, arch_only=arch_only,
                 mint_only=mint_only)
