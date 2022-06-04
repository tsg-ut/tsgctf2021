#!/bin/sh

make clean && \
make dist && \
make deploy && \
docker-compose build && \
docker-compose up -d
