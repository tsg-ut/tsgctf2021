N, e = (1108103848370322618250236235096737547381026108763302516499816051432801216813681568375319595638932562835292256776016949573972732881586209527824393027428125964599378845347154409633878436868422905300799413838645686430352484534761305185938956589612889463246508935994301443576781452904666072122465831585156151, 65537)
c = 254705401581808316199469430068831357413481187288921393400711004895837418302514065107811330660948313420965140464021505716810909691650540609799307500282957438243553742714371028405100267860418626513481187170770328765524251710154676478766892336610743824131087888798846367363259860051983889314134196889300426

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

def print_as_bytes(x):
    print(x.to_bytes((x.bit_length() + 7) // 8, byteorder='big'))

for i in range(1, 101):
    print(i)
    for j in range(i, 10000 // i + 1):
        tmp = (i + j) * (i + j) + 4 * (N - 1) * i * j
        st = sqrt(tmp)
        if st ** 2 == tmp and (st - i - j) % (2 * i * j) == 0:
            g = (st - i - j) // (2 * i * j)
            p, q = (i * g + 1), (j * g + 1)
            if p != 1 and q != 1 and N == p * q:
                phi = (p - 1) * (q - 1)
                d = modinv(e, phi)
                print_as_bytes(pow(c, d, N))