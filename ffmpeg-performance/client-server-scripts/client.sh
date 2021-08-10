#/bin/bash
set -e
set -x

# cleanup 
rm -f videoFrames/*

time ffmpeg -re -i tcp://192.168.0.253:9999 -v debug -report videoFrames/frame%05d.bmp
