#!/bin/sh
set -eu

cd /home/katsurahiroyuki/chat/build
BASE=./env python3 -u start_docker.py 2> /dev/null
