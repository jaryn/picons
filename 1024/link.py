import re
import os

with open('channels') as channels:
    M=r'#EXTINF:-1 logo=".*" tvg-id="[a-f0-9]*",(.*)'
    matches = [re.search(M, line) for line in channels]

matches = [m.group(1) for m in matches if m]
mapping = {k: k.replace(" ", "").replace("|","").lower() for k in matches if k }

for tgt, src in mapping.items():
    if os.path.isfile(f"{src}.png"):
        print(f"linking: {src}")
        os.link(f"{src}.png", f"dvb-{tgt}.png")
    else:
        print(f"{src}.png doesn't exist")
