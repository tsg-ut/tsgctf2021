#!/bin/sh

set -eu

mkdir -p dist/chat_service

files="Dockerfile connector.py chat_service/base64.c chat_service/base64.h chat_service/host.cpp chat_service/client.cpp chat_service/service.hpp chat_service/Makefile host client"

for file in $files
do
	cp "src/$file" "dist/$file"
done

cp "build/libc.so.6" "dist/libc.so.6"
mkdir -p "dist/env/connector"
echo "hello" > dist/env/connector/.hello

