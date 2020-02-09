import re
import os

with open('/home/jhenner/Downloads/channels') as channels:
    [print(line) for line in channels]

with open('/home/jhenner/Downloads/channels') as channels:
    M=r'#EXTINF:-1 tvg-id="[a-f0-9]*",(.*)'
    matches = [re.search(M, line) for line in channels]

matches = [m.group(1) for m in matches if m]
mapping = {k: k.replace(" ", "").lower() for k in matches if k }

for tgt, src in mapping.items():
    if os.path.isfile(f"{src}.png"):
        os.symlink(f"{src}.png", f"dvb-{tgt}.png")
    else:
        print(f"{src}.png doesn't exist")
