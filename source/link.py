#!/bin/python3

import sys
import re
import os
import argparse
import requests
from textwrap import dedent

parser = argparse.ArgumentParser(description='Create icons based on playlist.')
parser.add_argument('--playlist-url', default="http://raspberrypi.lan:9981/playlist",
                    help='The url of the playlist')

args = parser.parse_args()

channels = requests.get(args.playlist_url).text.split('\n')

M=r'#EXTINF:-1 logo=".*" tvg-id="[a-f0-9]*",(.*)'
matches = [re.search(M, line) for line in channels]

matches = sorted(set(m.group(1) for m in matches if m))
if not matches:
    print("Didn't find any channel in the playlist")
    sys.exit(-1)

def applyregexps(patterns, text):
    for pattern, subst in patterns:
        orig = text
        text = re.sub(pattern, subst, text).strip()
        print("Changed", orig, "->", text, "pattern: ", pattern)
    return text

def replace(patterns, text):
    for pattern, subst in patterns:
        orig = text
        text = text.replace(pattern, subst).strip()
        print("Changed", orig, "->", text, "pattern: ", pattern)
    return text

def commonreplace(s):
    return s.replace("+", "plus")

def guess_image_name(s):
    """ This is the file with the content """
    orig = s
    replacements = (
        ('CRo D-DUR', 'croddur'),
        ("| T2",""),
        ("| P", ""),
        (" HD",""),
        (" T2",""),
        (":D/", "D"),
        (" ", "")
    )
    s = commonreplace(s)
    r = replace(replacements, s)


    s = r.lower()
    # Exceptions
    s = s.replace("barrandovnews", "barrandovnewst2")
    s = s.replace("tvrebel", "rebel")
    s = s.replace("tvrelax", "relax")
    s = s.replace("seznam.cztv", "seznamcz")
    s = s.replace("tvzak", "zak")
    return f"{s}.png"

def tvheadend_file_name(s):
    """ This is what will be in the url (from tvheadend)"""
    s = commonreplace(s).strip()
    s = s.replace("|", "_")
    s = s.replace(":D/", "_D-")

    # Exception
    s = s.replace("Prima plus1", "Prima +1")
    return f"dvb-{s}.png"

linked = failed = 0
for channel in matches:
    image = guess_image_name(channel)
    tvh_f_n = tvheadend_file_name(channel)
    print(f"For channel {channel:<20}\tcrating {image} -> {tvh_f_n}", end="")
    if os.path.isfile(image):
        os.link(image, tvh_f_n)
        linked += 1
    else:
        print(f"\tthe source file doesn't exist", end="")
        os.symlink(image, tvh_f_n)
        failed += 1
    print()

print(f"Linked: {linked}, failed: {failed}")
