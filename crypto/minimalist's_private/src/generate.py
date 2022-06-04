import Crypto.Util.number
import itertools
import random


def gcd(a,b):
    if a == 0:
        return b
    while b != 0:
        a,b = b,a % b
    return a

def sqrt(n):
    l = 0
    r = n + 1
    while l + 1 < r:
        mid = (l + r) // 2
        if mid * mid >= n:
            r = mid
        else:
            l = mid
    return r


upper_limit = 10000
lis = list(itertools.chain.from_iterable([[(i, j) for j in range(i + 1, upper_limit // i + 1) if gcd(i, j) is 1] for i in range(1, sqrt(upper_limit) + 10)]))
random.shuffle(lis)

bit = 512

def gen_key():
    while True:
        print('trial')
        tmp_p = Crypto.Util.number.getPrime(bit - upper_limit.bit_length() // 2 - 1)
        print('    prime gen done')
        pr_lis = [+Crypto.Util.number.isPrime(tmp_p * 2 * i + 1) for i in range(0, upper_limit + 1)]
        print('    list done')
        print('    there are', sum(pr_lis), 'primes.')
        for x, y in lis:
            if (pr_lis[x] is 1) and (pr_lis[y] is 1):
                return (2 * tmp_p * x + 1, 2 * tmp_p * y + 1)

p, q = gen_key()

print(f'p, q = {p}, {q}')

phi = (p - 1) * (q - 1) // gcd(p - 1, q - 1)

def xgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modinv(a, m):
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

N = p * q

e = 65537
d = modinv(e, phi)

with open('secret.py', mode='w') as f:
    f.write(f'N = {N}\np, q = {p}, {q}\nL = {phi}\ne = {e}')
