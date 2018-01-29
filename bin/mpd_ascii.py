#!/usr/bin/env python
"""Display ASCII version of cover art in terminal"""
from mpd import MPDClient
from plumbum import local
import taglib as tl

ADDRESS="localhost"
LIBRARY="~/data/music"
PORT=6600

def get_cover(song_path):
    try:
        extract_embedded(song_path)
    tags =
    song_dir = song_path.parent

def main():
    mpd = MPDClient()
    mpd.connect(ADDRESS, PORT)
    song = mpd.currentsong()
    song_path = local.path(song['file'])
    cover = get_cover(song_path)


if __name__ == "__main__":
    main()
