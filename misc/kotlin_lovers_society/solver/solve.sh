#!/bin/sh

curl -X POST -F file=@/home/user/image.rgb "http://server:9060/submit" | grep TSGCTF
