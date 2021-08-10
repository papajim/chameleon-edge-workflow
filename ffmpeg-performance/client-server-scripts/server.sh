#!/bin/bash
set -e
set -x

VIDEO=$1

ffprobe $VIDEO

echo "starting up ffmpeg server to send $VIDEO"
time ffmpeg -i $VIDEO -v debug -report -vcodec mpeg4 -listen 1 -f mpegts tcp://192.168.0.16:9999
