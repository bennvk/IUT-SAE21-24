#!/bin/bash

rm -f stream*.ts stream.m3u8

ffmpeg -fflags nobuffer \
  -flags low_delay \
  -strict experimental \
  -fflags +genpts \
  -rtsp_transport tcp \
  -i rtsp://192.168.146.4:554/live.sdp \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -g 15 -keyint_min 15 \
  -f hls -hls_time 0.5 -hls_list_size 3 -hls_flags delete_segments+omit_endlist \
  stream.m3u8
