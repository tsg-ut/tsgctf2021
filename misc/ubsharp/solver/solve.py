import sys
import subprocess as sp
from pwn import *

host = sys.argv[1]
port = int(sys.argv[2])

conn = remote(host, port)

conn.recvuntil(b'`')
hashcash_command = conn.recvuntil(b'`')[:-1].decode('ascii')

hashcash_result = sp.run(hashcash_command.split(' '), capture_output=True)
hashcash_result = hashcash_result.stdout.decode('ascii')[:-1]

conn.send((hashcash_result+'\n').encode('ascii'))

conn.recv()

with open("./ans_input.txt", 'r') as f:
    ans_input = f.read()

conn.send((ans_input+'\n').encode('ascii'))

conn.recvuntil(b'Congratulations! ')
flag_str = conn.recv()

if b'TSGCTF' in flag_str:
    sys.exit(0)
else:
    sys.exit(1)
