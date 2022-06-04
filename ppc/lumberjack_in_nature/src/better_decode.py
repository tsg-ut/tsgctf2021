import mpmath
import json

PREC = 10000
mpmath.mp.dps = PREC

def decrypt(enc):
    return int(mpmath.power(2, enc * mpmath.ln(2) - int(enc * mpmath.ln(2) - 2000) // 8 * 8))


with open('../dist/encoded.json') as f:
    s, e = json.load(f)

flag = decrypt(s << e)

print(flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big')[:200])