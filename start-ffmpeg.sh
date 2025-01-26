#!/bin/bash

echo "Starting FFmpeg service..."

# Infinite loop to keep retrying if the camera is not found
while true; do
    if [ -e /dev/video0 ]; then
        echo "Camera found: /dev/video0. Starting FFmpeg..."
        ffmpeg -re -f v4l2 -i /dev/video0 \
               -input_format mjpeg -video_size 800x450 -framerate 30 \
               -vcodec libx264 -preset veryfast -tune zerolatency \
               -pix_fmt yuv420p -f rtsp rtsp://127.0.0.1:8554/live
    else
        echo "Error: /dev/video0 not found. Retrying in 15 seconds..."
    fi
    sleep 15
done
