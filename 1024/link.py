import re
import os

with open('channels') as channels:
    M=r'#EXTINF:-1 logo=".*" tvg-id="[a-f0-9]*",(.*)'
    matches = [re.search(M, line) for line in channels]

matches = [m.group(1) for m in matches if m]

def commonreplace(s):
    return s.replace(".", "").replace("+", "plus").replace("+", "plus")

def makesrc(s):
    """ This is the file with the content """
    s = commonreplace(s)
    s = s.replace('CRo D-DUR', 'croddur')
    s = s.replace("| T2","")
    s = s.replace("| P", "")
    s = s.replace("| T", "")
    s = s.replace(":D/", "D")
    s = s.replace(" ", "")
    s = s.lower()
    return s

def maketgt(s):
    """ This is what will be in the url (from tvheadend)"""
    s = commonreplace(s).strip()
    s = s.replace("|", "_")
    s = s.replace(":D/", "_D-")
    return s

add = {
    'CT 1 SM HD T2': 'ct1hdt2',
}

linked = failed = 0
for channel in sorted(set(matches)):
    src = makesrc(channel)
    tgt = maketgt(channel)
    print(f"For channel {channel:<20}\tcrating {src} -> {tgt}", end="")
    if os.path.isfile(f"{src}.png"):
        os.link(f"{src}.png", f"dvb-{tgt}.png")
        linked += 1
    else:
        print(f"\tthe source file doesn't exist", end="")
        failed += 1
    print()

print(f"Linked: {linked}, failed: {failed}")
