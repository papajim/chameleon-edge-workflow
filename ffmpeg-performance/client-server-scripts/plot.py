#!/usr/bin/env python3
import pickle
from pathlib import Path
from collections import namedtuple

import matplotlib.pyplot as plt

Pair = namedtuple("Pair", ["resolution", "client", "server"])

# example row: Row(frame='5', fps='0.0', q=None, size=None, time='00:00:00.20', bitrate=None, speed='0.393x')
Row = namedtuple("Row", ["frame", "fps", "q", "size", "time", "bitrate", "speed"])

'''
with open("480x360_client_rpi.pkl", "rb") as f:
    client_data = pickle.load(f)

with open("480x360_client_rpi_tmpfs.pkl", "rb") as f:
    client_tmpfs_data = pickle.load(f)

figure = plt.figure()
ax = figure.add_subplot(1,1,1)
ax.plot(
    [int(row.frame) for row in client_data],
    [float(row.fps) for row in client_data],
    label="RPI client"
)

ax.plot(
    [int(row.frame) for row in client_tmpfs_data],
    [float(row.fps) for row in client_tmpfs_data],
    label="RPI client using tmpfs"
)
ax.axhline(y=25, color="g", linestyle="dotted", label="native fps")
ax.legend()
ax.set(xlabel="frame #", ylabel="fps", title="480x360 using tmpfs")

text = """
Comparing fps reported from RPI as client using disk vs tmpfs 
(fs in ram mounted to /dev/shm). MBP server streaming fps not reported 
"""

plt.show()
'''


MBP_client_runs = [
        Pair(resolution="240x160", client="240x160_client_mbp.pkl", server="240x160_server_rpi.pkl"),
        Pair(resolution="480x360", client="480x360_client_mbp.pkl", server="480x360_server_rpi.pkl"),
        Pair(resolution="720x480", client="720x480_client_mbp.pkl", server="720x480_server_rpi.pkl"),
        Pair(resolution="1024x768", client="1024x768_client_mbp.pkl", server="1024x768_server_rpi.pkl"),
        Pair(resolution="1920x1080", client="1920x1080_client_mbp.pkl", server="1920x1080_server_rpi.pkl"),

    ]

RPI_client_runs = [
        Pair(resolution="240x160", client="240x160_client_rpi.pkl", server="240x160_server_mbp.pkl"),
        Pair(resolution="480x360", client="480x360_client_rpi.pkl", server="480x360_server_mbp.pkl"),
        Pair(resolution="720x480", client="720x480_client_rpi.pkl", server="720x480_server_mbp.pkl"),
        Pair(resolution="1024x768", client="1024x768_client_rpi.pkl", server="1024x768_server_mbp.pkl"),
        Pair(resolution="1920x1080", client="1920x1080_client_rpi.pkl", server="1920x1080_server_mbp.pkl")
]

figure, axes = plt.subplots(nrows=2, ncols=len(RPI_client_runs))
for i, run in enumerate(RPI_client_runs):
    ax = axes[0, i]
    
    with open(run.client, "rb") as f:
        client_data = pickle.load(f)
    
    with open(run.server, "rb") as f:
        server_data = pickle.load(f)
    
    ax.plot(
        [int(row.frame) for row in server_data],
        [float(row.fps) for row in server_data],
        label="MBP server"
    )

    ax.plot(
        [int(row.frame) for row in client_data],
        [float(row.fps) for row in client_data],
        label="RPI client"  
    )

    if run.resolution == "480x360":
        with open("480x360_client_rpi_tmpfs.pkl", "rb") as f:
            client_tmpfs_data = pickle.load(f)
        
        ax.plot(
            [int(row.frame) for row in client_tmpfs_data],
            [float(row.fps) for row in client_tmpfs_data],
            label="RPI client using tmpfs",
            color="tab:purple"
        )

    ax.axhline(y=25, color="g", linestyle="dotted", label="native fps")

    ax.set_xlim([0, 5000])
    ax.set_ylim([0, 80])
    ax.legend()
    ax.set(xlabel="frame #", ylabel="fps", title=run.resolution)

for i, run in enumerate(MBP_client_runs):
    ax = axes[1, i]
    
    with open(run.client, "rb") as f:
        client_data = pickle.load(f)
    
    with open(run.server, "rb") as f:
        server_data = pickle.load(f)
    
    ax.plot(
        [int(row.frame) for row in server_data],
        [float(row.fps) for row in server_data],
        label="RPI server"
    )

    ax.plot(
        [int(row.frame) for row in client_data],
        [float(row.fps) for row in client_data],
        label="MBP client"  
    )

    ax.axhline(y=25, color="g", linestyle="dotted", label="native fps")
    ax.fill()

    ax.set_xlim([0, 5000])
    ax.set_ylim([0, 80])
    ax.legend()
    ax.set(xlabel="frame #", ylabel="fps", title=run.resolution)

txt = """
Data obtained by parsing ffmpeg logs on both client and server side.
Each log: "frame=    9 fps=0.0 q=-0.0 size=N/A time=00:00:00.36 bitrate=N/A speed=0.706x"
produced at arbitrary times are recorded to obtain frame (frame # on x axis) and
fps (fps on y axis). This can be interpreted as, "as frame i is being processed,
this is the estimated fps at that time".
"""

figure.text(0.5,0, txt, ha="center")
plt.show()

'''
# bar graph 
import numpy as np

labels = [
    "240x160",
    "480x360",
    "720x480",
    "1024x768",
    "1920x1080"
]

fig, axes = plt.subplots(nrows=1, ncols=2)

dur = datetime.timedelta(minutes=3, seconds=14.08).total_seconds()

server = [
    datetime.timedelta(minutes=3, seconds=2.068).total_seconds(),
    datetime.timedelta(minutes=3, seconds=2.518).total_seconds(),
    datetime.timedelta(minutes=3, seconds=9.066).total_seconds(),
    datetime.timedelta(minutes=3, seconds=13.399).total_seconds(),
    datetime.timedelta(minutes=3, seconds=20.018).total_seconds(),
]

client = [
    datetime.timedelta(minutes=3, seconds=14.694).total_seconds(),
    datetime.timedelta(minutes=3, seconds=15.22).total_seconds(),
    datetime.timedelta(minutes=3, seconds=15.776).total_seconds(),
    datetime.timedelta(minutes=3, seconds=17.137).total_seconds(),
    datetime.timedelta(minutes=3, seconds=20.130).total_seconds(), 
]

x = np.arange(len(labels))

ax = axes[0]
width = 0.35
rects1 = ax.bar(x - width / 2, server, width, label="RPI server")
rects2 = ax.bar(x + width / 2, client, width, label="MBP client")

ax.set_xticks(x)
ax.set_xticklabels(labels)

ax.axhline(y=dur, color="g", linestyle="dotted", label="native video duration")
ax.set_ylabel("duration (seconds)")

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

ax.set_ylim([0, 1900])

plt.xticks(list(plt.xticks()[0]) + [dur])

ax.legend()
#######
ax = axes[1]
server = [
    datetime.timedelta(minutes=2, seconds=56.991).total_seconds(),
    datetime.timedelta(minutes=3, seconds=58.321).total_seconds(),
    datetime.timedelta(minutes=5, seconds=17.549).total_seconds(),
    datetime.timedelta(minutes=10, seconds=36.756).total_seconds(),
    datetime.timedelta(minutes=29, seconds=50).total_seconds(),
]

client = [
    datetime.timedelta(minutes=3, seconds=14.551).total_seconds(),
    datetime.timedelta(minutes=4, seconds=14.989).total_seconds(),
    datetime.timedelta(minutes=5, seconds=32.179).total_seconds(),
    datetime.timedelta(minutes=11, seconds=19.533).total_seconds(),
    datetime.timedelta(minutes=30, seconds=0).total_seconds(), 
]

x = np.arange(len(labels))


width = 0.35
rects1 = ax.bar(x - width / 2, server, width, label="MBP server")
rects2 = ax.bar(x + width / 2, client, width, label="RPI client")

ax.set_xticks(x)
ax.set_xticklabels(labels)

ax.axhline(y=dur, color="g", linestyle="dotted", label="native video duration")
ax.set_ylabel("duration (seconds)")

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

ax.legend()

ax.set_ylim([0, 1900])

fig.suptitle("ffmpeg command duration reported by time")
fig.tight_layout()
plt.show()


'''