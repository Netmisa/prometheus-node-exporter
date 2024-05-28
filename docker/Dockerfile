FROM python:3.12-alpine3.19

ENV PYTHONPATH=/usr/local/lib

WORKDIR /app

COPY --from=prometheus-container-exporter:build /install /usr/local/lib
RUN mv /usr/local/lib/bin/* /usr/local/bin/ && \
    rm -rf /usr/local/lib/bin

COPY ./src src

VOLUME [ "/var/run/docker.sock" ]

ENTRYPOINT ["fastapi", "run", "src/main.py"]
