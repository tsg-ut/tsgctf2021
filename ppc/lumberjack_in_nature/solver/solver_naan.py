from mpmath import *
import json

mp.dps = 2000

def decode(s, e):
    p = mpf(0)
    for i in range(1, e + 1):
        p += (pow(2, e - i, 8 * i) * s % (8 * i)) / mpf(i)
    for i in range(1, mp.prec + s.bit_length()):
        p += s / mpf((e + i) << i)
    return int(power(2, p - int(p - 2000) // 8 * 8))

with open('encoded.json') as f:
    s, e = json.load(f)

flag = decode(s, e)

print(flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big')[:200])