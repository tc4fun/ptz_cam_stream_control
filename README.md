# Logitech PTZ Pro 2 Streaming and Control

## Introduction

Connect Logitech PTZ Pro 2 of following model to Linux PC, creates a web page so any one on the same network can open a browser to view the stream and pan tilt and zoom the view.


## Requirement
`lsusb` shows following ID
```
Bus 007 Device 002: ID 046d:085f Logitech, Inc. PTZ Pro 2
```

## Install

1. `mediamtx` from [here](https://github.com/bluenviron/mediamtx/releases/tag/v1.9.3)

    ```
    wget https://github.com/bluenviron/mediamtx/releases/download/v1.9.3/mediamtx_v1.9.3_linux_amd64.tar.gz
    tar -xvf mediamtx_v1.9.3_linux_amd64.tar.gz
    ```
2. Install packages
    ```
    sudo apt install ffmpeg v4l-utils python3-pip python3-venv
    ```
3. python dependency
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    ```
4. Connect the camera and set permission
    ```
    chmod 666 /dev/video0
    ```

## Run
Run all three part in this above order in seperate sessions
```
./mediamtx
```
```
./ffmpeg_service.sh
```
```
source .venv/bin/activate
python3 ptzcam.py
```
Then open a web browser with `http://<server_ip>:5000` to view the results.