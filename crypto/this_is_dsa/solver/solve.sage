import subprocess
import sys
from os import path
from ptrlib import Socket, logger

if len(sys.argv) != 3:
    print("Usage: sage solve.sage <host> <port>")
    sys.exit(1)

while True:
    con = Socket(sys.argv[1], int(sys.argv[2]))
    q = int(con.recvlineafter('q = '))
    logger.info(f'q = {q}')
    n = 2048 // 256

    if int(q ** n).bit_length() != 2048:
        logger.warn('Precondition faild. Retrying...')
        con.close()
        continue

    p = q^n
    phi = q^(n - 1) * (q - 1)
    h = pow(2, phi // q, p)

    logger.info(f'p = {p}')
    logger.info(f'h = {h}')

    con.sendlineafter('p? ', str(p).encode())
    con.sendlineafter('h? ', str(h).encode())

    g = int(con.recvlineafter('g = '))
    logger.info(f'g = {g}')

    y = int(con.recvlineafter('y = '))
    logger.info(f'y = {y}')

    Q = Qp(q, n + 2)
    Qg = Q(int(g))
    Qy = Q(int(y))

    Qx = Qy.log() / Qg.log()
    logger.info(Qx)

    x = Qx.polynomial()[0][0]
    assert(pow(g, x, p) == y)

    logger.info(f'x = {x}')

    ret = subprocess.run(
        ['sage', '-python', 'decode.py', str(p), str(q), str(h), str(g), str(y), str(x)],
        capture_output=True,
        cwd=path.dirname(__file__))
    sign = ret.stdout.decode().strip()
    logger.info(f'sign = {sign}')
    con.sendlineafter('sign? ', sign.encode())

    line = b''
    while b'TSGCTF' not in line:
        line = con.recvline()
        logger.info(line)

    break
