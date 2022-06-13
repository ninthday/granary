# Granary

Installation

```shell
sudo apt install python3-pip libglib2.0-dev
```

## Add fastapi env on Pi

```shell
pip install fastapi
pip install uvicorn
```

## Run fastapi

```shell
$ uvicorn main:app --reload --host 127.0.0.1 --port 8087
```

> Note:
> `--reload`: Enable auto-reload
> `--host TEXT`: Bind socket to this host. [default: 127.0.0.1] > `--port INTEGER`: Bind socket to this port. [default: 8000]

## Install bluepy

The PYPL's bluepy package was uploaded in 2018.

However, the bluepy-helper has high-CPU-usage issue
ref: https://github.com/IanHarvey/bluepy/issues/239

and the issue has been resloved by this [8818eb2](https://github.com/IanHarvey/bluepy/commit/8818eb2a6565f253a8001f633a958362fea1a396) merge.

Since the package does not include the merge, we should install from the source before using it.

```shell
$ sudo apt install build-essential libglib2.0-dev
$ git clone https://github.com/IanHarvey/bluepy.git
$ cd bluepy
$ python3 setup.py build
$ sudo python3 setup.py install
```
