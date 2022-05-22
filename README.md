
# Granary

Installation

```shell
sudo apt install python3-pip libglib2.0-dev
```

## Run fastapi
```shell
$ uvicorn main:app --reload --host 127.0.0.1 --port 8087
```
> Note:
> `--reload`: Enable auto-reload
> `--host TEXT`: Bind socket to this host. [default: 127.0.0.1]
> `--port INTEGER`: Bind socket to this port. [default: 8000]
