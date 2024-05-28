#!/usr/bin/python3

from fastapi import FastAPI

from logger import Logger
from process import Process


logger = Logger()
process = Process(logger)
app = FastAPI()


@app.get("/")
def get_all_container_stats():
    return process.get_all_container_stats()
