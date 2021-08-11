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
MacbookPro                 |                                                |  Raspberry Pi 4
4core/8thread              |--------- latency: ~0.397ms, ~112 MB/s bw --------|  4 core
16 GB ram                  |                                                |  4 GB ram
ssd w/ ~ 2400 MB/s write   |                                                |  64 GB sd card w/ ~ 50 MB/s write
```

## ffmpeg Commands
- client: `time ffmpeg -re -i tcp://192.168.0.253:9999 -v debug -report videoFrames/frame%05d.bmp`
  - for `tmpfs` scenario, used `time ffmpeg -re -i tcp://192.168.0.253:9999 -v debug -report /dev/shm/videoFrames/frame%05d.bmp`
- server: `time ffmpeg -i $VIDEO -v debug -report -vcodec mpeg4 -listen 1 -f mpegts tcp://192.168.0.16:9999`

log lines parsed:
- parsed out logs which show fps of ffmpeg at arbitrary times
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
