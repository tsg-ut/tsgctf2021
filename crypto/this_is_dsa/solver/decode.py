import sys
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from base64 import b64encode

p, q, h, g, y, x = map(int, sys.argv[1:])

dsa = DSA.construct((y, g, p, q, x))
dss = DSS.new(dsa, 'fips-186-3')
sign = dss.sign(SHA256.new(b'flag'))

print(b64encode(sign).decode())
