#!/bin/sh
set -eu

cd /home/katsurahiroyuki/catastrophe/build
python3 proof-of-work.py &&\
python3 start_docker.py
