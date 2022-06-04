from sage.modules.free_module_integer import IntegerLattice
from ptrlib import Socket, logger
from hashlib import sha256
import sys

if len(sys.argv) != 3:
    logger.info("Usage: sage solve.sage <host> <port>")
    sys.exit(1)

_, host, port = sys.argv

# Babai's Nearest Plane algorithm
# from: http://mslc.ctf.su/wp/plaidctf-2016-sexec-crypto-300/
def Babai_closest_vector(M, G, target):
  small = target
  for _ in range(1):
    for i in reversed(range(M.nrows())):
      c = ((small * G[i]) / (G[i] * G[i])).round()
      small -= M[i] * c
  return target - small

con = Socket(host, int(port))
con.sendlineafter(b'choice? ', b'1')
x1 = int(con.recvlineafter(b'x = '))
s1 = int(con.recvlineafter(b's = '))
con.sendlineafter(b'choice? ', b'1')
x2 = int(con.recvlineafter(b'x = '))
s2 = int(con.recvlineafter(b's = '))
con.sendlineafter(b'choice? ', b'1')
x3 = int(con.recvlineafter(b'x = '))
s3 = int(con.recvlineafter(b's = '))

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
z = int(sha256(b'Baba').hexdigest(), 16)

xs = [x1, x2, x3]
ss = [s1, s2, s3]

logger.info(f'xs = {xs}')
logger.info(f'ss = {ss}')

F = GF(p)

n = 26
t = 3

matrix = []

tmp = [0] * (n * t)
for i in range(t):
  tmp[n * i] = int(F(xs[i]) // F(ss[i]))

matrix.append(tmp)

for i in range(t):
  for j in range(1, n):
    tmp = [0] * (n * t)
    tmp[i * n] = 256^j
    tmp[i * n + j] = -1
    matrix.append(tmp)

for i in range(t):
  tmp = [0] * (n * t)
  tmp[i * n] = p
  matrix.append(tmp)

C = (F(256)^n - 1) // (256 - 1) * 48

target = [0] * (n * t)
for i in range(t):
  target[n * i] = int(C - F(z) // F(ss[i]))

logger.info('LLL started')
lattice = IntegerLattice(matrix, lll_reduce=True)
logger.info('LLL done')
E = lattice.reduced_basis

gram = E.gram_schmidt()[0]
res = Babai_closest_vector(E, gram, vector(ZZ, target))
logger.info('CVP done')

ks = [r - e for r, e in zip(res, target)]
logger.info(f'ks = {ks}')

k1 = int.from_bytes((''.join(map(str, ks[n-1::-1]))).encode(), 'big')
logger.info(f'k1 = {k1}')

recovered_d = (F(k1) * F(s1) - F(z)) // F(x1)
logger.info(f'recovered_d = {recovered_d}')

logger.info('private key recovered')


# secp256k1
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
K = GF(p)
a = K(0x0000000000000000000000000000000000000000000000000000000000000000)
b = K(0x0000000000000000000000000000000000000000000000000000000000000007)
E = EllipticCurve(K, (a, b))
G = E(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
      0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
E.set_order(
    0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141 * 0x1)

z2 = int(sha256(b'Flag').hexdigest(), 16)
k = 334
x, y = (G * k).xy()
F2 = GF(E.order())
s = F2(z2 + int(x) * int(recovered_d)) // k

logger.info(f'z2 = {z2}')
logger.info(f'x = {x}')
logger.info(f'y = {y}')
logger.info(f's = {s}')

con.sendlineafter(b'choice? ', b'2')
con.sendlineafter(b'Which rule do you want to know? ', b'Flag')
con.sendlineafter(b'x? ', str(x).encode())
con.sendlineafter(b's? ', str(s).encode())

flag = con.recvline()
logger.info(flag)

if b'TSGCTF{' not in flag:
  sys.exit(1)

con.close()
