# Container exporter

This API export stats from all containers into prometheus format


# How to use it ?


```
docker run \
    --rm \
    -it \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -p 8000:8000 \
    netmisa/prometheus-container-exporter:latest
```
Then, go to `http://localhost:8000/metrics`

or

```
make build

docker run \
    --rm \
    -it \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -p 8000:8000 \
    localhost/prometheus/container-exporter:latest
```
Then, go to `http://localhost:8000/metrics`

or

```
make build

make start
```
Then, go to `http://localhost:8000/metrics`

After

```
make stop
```


### For development

```
make build
make dev
```

After:

```
make clean
```
