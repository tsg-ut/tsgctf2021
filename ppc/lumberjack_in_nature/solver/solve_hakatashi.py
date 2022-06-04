from mpmath import *
import json
from subprocess import run, PIPE
import sys

mp.dps = 10000

with open('../dist/encoded.json') as f:
  s, e = json.load(f)

p = run(['cargo', 'run', '--manifest-path=../src/fast_ln2/Cargo.toml', '--release', str(e)], stdout=PIPE)
fs = p.stdout.decode().strip()
f = int(fs, 2)
size = len(fs)

sf = (s * f) % (1 << size)
p = mpf(sf) / mpf(1 << size) * ln(2)
flag = int(exp(p) * mpf(1 << (74 * 8 - 2)))
print(flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big'))
