#!/bin/sh

echo "$1" 1>&2
strace -f ./dist/beginners_rev "$1" 2>&1 | grep correct | wc -l
