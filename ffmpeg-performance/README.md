# ffmpeg on raspberry pi 4 

## Test Videos
- **duration**: 3 minutes 14.08 seconds
- **fps**: 25

| resolution | mp4 size | individual frame size | total size of all frames |
|------------|----------|-----------------------|--------------------------|
| 240x160    | 4.7 MB   | ~ 113 KB              | ~ 550 MB                 |
| 480x360    | 19 MB    | ~ 507 KB              | ~ 2.4 GB                 |
| 720x480    | 36 MB    | ~ 1 MB                | ~ 4.8 GB                 |
| 1024x768   | 75 MB    | ~ 2.3 MB              | ~ 11 GB                  |
| 1920x1080  | 169 MB   | ~ 6 MB                | ~ 29 GB                  |

## Test Environment

```
MacbookPro                 |                                                  |  Raspberry Pi 4
4core/8thread              |--------- latency: ~0.397ms, ~112 MB/s bw --------|  4 core
16 GB ram                  |                                                  |  4 GB ram
ssd w/ ~ 2400 MB/s write   |                                                  |  64 GB sd card w/ ~ 50 MB/s write
```

## ffmpeg Commands
- client: `time ffmpeg -re -i tcp://192.168.0.253:9999 -v debug -report videoFrames/frame%05d.bmp`
  - for `tmpfs` scenario, used `time ffmpeg -re -i tcp://192.168.0.253:9999 -v debug -report /dev/shm/videoFrames/frame%05d.bmp`
- server: `time ffmpeg -i $VIDEO -v debug -report -vcodec mpeg4 -listen 1 -f mpegts tcp://192.168.0.16:9999`
    - for `tmpfs` scenario, used `time ffmpeg -i $VIDEO -frames $FRAMES -v debug -report -vcodec mpeg4 -listen 1 -f mpegts tcp://192.168.0.16:9999`
        where `$FRAMES` is the number of individual frames that will fit into 2.7GB (used `mount -o remount,size=3G /dev/shm` to set tmpfs size)

log lines parsed:
- parsed out logs which show fps of ffmpeg at arbitrary times (e.g. `5197 frame=  219 fps= 11 q=31.0 size=    2982kB time=00:00:08.72 bitrate=2801.9kbits/s speed=0.455x`)
- fps, speed, q, etc. is reported at some time not marked by a timestamp, so using `frame #` as a point of
    reference in the plots
```
5193 [h264 @ 0x7f9987008000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5194 [h264 @ 0x7f998701b000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5195 [h264 @ 0x7f9987001e00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5196 [h264 @ 0x7f9987002400] nal_unit_type: 5(IDR), nal_ref_idc: 3
5197 frame=  219 fps= 11 q=31.0 size=    2982kB time=00:00:08.72 bitrate=2801.9kbits/s speed=0.455x    ^M[h264 @ 0x7f9987002a00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5198 [h264 @ 0x7f9987003000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5199 [h264 @ 0x7f9987003600] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5200 [h264 @ 0x7f9987003c00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5201 [h264 @ 0x7f9987004200] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5202 [h264 @ 0x7f9987008000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5203 [h264 @ 0x7f998701b000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5204 [h264 @ 0x7f9987001e00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5205 [h264 @ 0x7f9987002400] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5206 [h264 @ 0x7f9987002a00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5207 [h264 @ 0x7f9987003000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5208 frame=  230 fps= 12 q=31.0 size=    3099kB time=00:00:09.16 bitrate=2771.2kbits/s speed=0.465x    ^M[h264 @ 0x7f9987003600] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5209 [h264 @ 0x7f9987003c00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5210 [h264 @ 0x7f9987004200] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5211 [h264 @ 0x7f9987008000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5212 [h264 @ 0x7f998701b000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5213 [h264 @ 0x7f9987001e00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5214 [h264 @ 0x7f9987002400] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
5215 frame=  237 fps=9.8 q=31.0 size=    3143kB time=00:00:09.44 bitrate=2727.9kbits/s speed=0.39x    ^M[h264 @ 0x7f9987002a00] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5216 [h264 @ 0x7f9987003000] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 0
5217 [h264 @ 0x7f9987003600] nal_unit_type: 1(Coded slice of a non-IDR picture), nal_ref_idc: 2
```

## Plots

![reported fps](https://github.com/pegasus-isi/chameleon-edge-workflow/blob/master/ffmpeg-performance/Figure_2.png?raw=true)
![duration](https://github.com/pegasus-isi/chameleon-edge-workflow/blob/master/ffmpeg-performance/Figure_3.png?raw=true)

## strace output when using SD card vs /dev/shm for writes
```
# writing to sd card
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 94.85  138.804315        9283     14951        19 futex
  4.54    6.646224         119     55391           write
  0.19    0.283952          39      7119           brk
  0.17    0.248650          49      5061         8 openat
  0.08    0.116254          21      5399           nanosleep
...
```

```
# writing to /dev/shm
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 96.13  133.670781        8730     15310        13 futex
  2.97    4.134965          75     54920       724 write
  0.28    0.388190          54      7119           brk
  0.24    0.338613          22     14848           nanosleep
...
```
