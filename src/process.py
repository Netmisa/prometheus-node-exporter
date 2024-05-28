#!/usr/bin/python3

from logger import Logger

import docker
from prometheus_client import (
    Info,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
)
from fastapi.responses import Response


class Process:
    METRIC_PREFIX = "container_exporter"

    def __init__(
        self,
        logger: Logger,
    ) -> None:
        self.log = logger
        self.docker = docker.from_env()
        self.my_registry = CollectorRegistry()
        self.gauges = {}
        self.infos = {}

        self.__init_gauges()
        self.__init_infos()

    def __init_gauges(self) -> None:
        label_names = ["container_id", "container_name", "stack_name"]
        metrics = [
            {
                "name": "stats_cpu_total_usage",
                "description": "Total CPU usage (in nanoseconds)",
            },
            {
                "name": "stats_memory_stats_usage",
                "description": "Memory usage (in bytes)",
            },
            {
                "name": "stats_memory_stats_limit",
                "description": "Memory limit (in bytes)",
            },
            {"name": "stats_block_io_read", "description": "Block IO read (in bytes)"},
            {
                "name": "stats_block_io_write",
                "description": "Block IO write (in bytes)",
            },
            {
                "name": "stats_net_io_received",
                "description": "Network IO received (in bytes)",
            },
            {
                "name": "stats_block_io_transmitted",
                "description": "Network IO transmitted (in bytes)",
            },
        ]

        for metric in metrics:
            self.gauges[metric["name"]] = Gauge(
                f"{self.METRIC_PREFIX}_{metric['name']}",
                metric["description"],
                labelnames=label_names,
                registry=self.my_registry,
            )

    def __init_infos(self) -> None:
        infos = [
            {"name": "docker_version", "description": "Docker version"},
        ]

        for info in infos:
            self.infos[info["name"]] = Info(
                f"{self.METRIC_PREFIX}_{info['name']}",
                info["description"],
                registry=self.my_registry,
            )

    def __extract_stack_name(self, name) -> str:
        return name.split(".")[0]

    def __get_total_block_io(self, stats):
        total_read = 0
        total_write = 0

        for io in stats["blkio_stats"]["io_service_bytes_recursive"]:
            total_read += io["value"] if io["op"] == "read" else 0
            total_write += io["value"] if io["op"] == "write" else 0

        return total_read, total_write

    def __get_total_net_io(self, stats):
        rx_bytes = 0
        tx_bytes = 0

        for _, interface in stats["networks"].items():
            rx_bytes += interface["rx_bytes"]
            tx_bytes += interface["tx_bytes"]

        return rx_bytes, tx_bytes

    def __set_metrics(self, container) -> None:
        label_values = [
            container.id,
            container.name,
            self.__extract_stack_name(container.name),
        ]
        stats = container.stats(stream=False)

        self.gauges["stats_memory_stats_limit"].labels(*label_values).set(
            stats["memory_stats"]["limit"]
        )
        self.gauges["stats_memory_stats_usage"].labels(*label_values).set(
            stats["memory_stats"]["usage"]
        )
        self.gauges["stats_cpu_total_usage"].labels(*label_values).set(
            stats["cpu_stats"]["cpu_usage"]["total_usage"]
        )

        block_read, block_write = self.__get_total_block_io(stats)
        self.gauges["stats_block_io_read"].labels(*label_values).set(block_read)
        self.gauges["stats_block_io_write"].labels(*label_values).set(block_write)

        received_bytes, transmitted_bytes = self.__get_total_net_io(stats)
        self.gauges["stats_net_io_received"].labels(*label_values).set(received_bytes)
        self.gauges["stats_block_io_transmitted"].labels(*label_values).set(
            transmitted_bytes
        )

    def get_all_container_stats(self) -> None:
        try:
            containers = self.docker.containers.list()

            for container in containers:
                self.__set_metrics(container)
        except Exception as e:
            self.log.error(f"Error : {e}")

        self.infos["docker_version"].info({"version": self.docker.version()["Version"]})

        return Response(
            generate_latest(self.my_registry), media_type=CONTENT_TYPE_LATEST
        )
