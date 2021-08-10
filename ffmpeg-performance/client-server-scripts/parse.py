#!/usr/bin/env python3
import re
import sys
import pickle
from collections import namedtuple

p = re.compile(
    r"^(frame=\s*\d+\s+)(fps=\s*\d+(?:\.\d+)?\s+).+(time=\d{2}:\d{2}:\d{2}\.\d{2}\s+).+(speed=\d+\.*\d*x)"
)

Row = namedtuple("Row", ["frame", "fps", "q", "size", "time", "bitrate", "speed"])

data = list()
with open(sys.argv[1], "r") as f:
    for line in f:
        match = p.match(line)
        if match:
            r = Row(
                    frame=match.group(1).split("=")[1].strip(),
                    fps=match.group(2).split("=")[1].strip(),
                    time=match.group(3).split("=")[1].strip(),
                    speed=match.group(4).split("=")[1].strip(),

                    # ignore the rest for now
                    q=None,
                    size=None,
                    bitrate=None
                )

            print(r)
            data.append(r)

with open(sys.argv[2], "wb") as f:
    pickle.dump(data, f)
