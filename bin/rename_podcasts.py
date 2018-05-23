#!/usr/bin/env python3
"""Recursively rename all mp3 files in a directory with the episode title.

This script is for assigning useful and readable names to automatically
downloaded podcasts e.g from podget.
"""
from datetime import datetime
import os
import re

import eyed3
from plumbum import local
import sys


def sanitize_path(path):
    """Replace illegal path characters and spaces in path."""
    return re.sub(r"[^a-zA-Z0-9_\-/\.]", "", path.replace(" ", "_"))


def get_title(mp3):
    """Get the podcast title from the ID3 tags."""
    try:
        title = eyed3.load(mp3).tag.title
        return sanitize_path(title)
    except AttributeError:
        return None


def get_modification_date(mp3):
    timestamp = os.path.getmtime(mp3)
    return datetime.fromtimestamp(timestamp).strftime("%Y-%M-%d")


def get_new_filename(mp3):
    """Get the new output filename for an mp3.

    Output name is of form <Date>_<Title>.mp3.
    """
    title = get_title(mp3)
    modification_date = get_modification_date(mp3)
    if title:
        new_basename = sanitize_path("_".join([modification_date, title]))
    else:
        new_basename = modification_date
    return mp3.dirname / (new_basename + ".mp3")


def carefully_move_file(src, dest):
    """If destination exists, add a suffix to the output filename."""
    if dest.exists() and src != dest:
        dest = dest.dirname / "x".join([dest.name, dest.suffix])
        carefully_move_file(src, dest)
    else:
        src.move(dest)


def rename_mp3s_in_dir(dir):
    """Rename all mp3s in a directory using their ID3 tags."""
    for mp3 in dir.glob("*.mp3"):
        new_filename = get_new_filename(mp3)
        carefully_move_file(mp3, new_filename)


def rename_podcasts(dir):
    """Recursively rename all mp3s in a directory and all subdirectories using
    ID3 tags.
    """
    rename_mp3s_in_dir(dir)
    for file in dir.list():
        if file.is_dir():
            rename_podcasts(file)


if __name__ == "__main__":
    rename_podcasts(local.path(sys.argv[1]))
