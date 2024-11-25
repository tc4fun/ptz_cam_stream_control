# Logitech PTZ Pro 2 Streaming and Control

## Introduction

Connect Logitech PTZ Pro 2 (`lsusb` shows ID 046d:085f) to a Linux PC, stream video (via `ffmpeg`) to a WebRTC server (via `mediamtx`), host a web page (via `flask`) so that using a browser one can view the stream and pan / tilt / zoom the view (via `v4l`).


## Requirement
`lsusb` shows following ID
```
Bus 007 Device 002: ID 046d:085f Logitech, Inc. PTZ Pro 2

```

## Container

```
docker-compose build
docker-compose up

```
will bring up everything.

Then open a web browser with `http://<server_ip>:5000` to view the results.

If interested in details, continue to following sections...

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
    sudo chmod 666 /dev/video0
    ```

## Run

Run all three parts in this order in seperate sessions (I use `screen` but a `docker-compose` would be a better solution)
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
