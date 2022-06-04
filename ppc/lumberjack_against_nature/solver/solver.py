from mpmath import *
from ptrlib import Socket, logger
import sys

if len(sys.argv) != 3:
    print("Usage: sage solve.sage <host> <port>")
    sys.exit(1)

_, host, port = sys.argv

PREC = 800
mp.dps = PREC

def minimize_dec_part_by_error(alpha, beta, epsi):
    pn = 1
    pp = alpha % 8
    nn = 0
    np = -8
    tn = 0
    tp = beta % 8
    while tp > epsi:
        if pp + np < 0:
            cnp = max(int(floor(np / pp + 1)), int(floor((np + tp) / pp)))
            nn -= pn * cnp
            np -= pp * cnp
            ctn = min(0, max(int(floor(tp / np + 1)), int(floor((tp - epsi) / np))))
            tn -= nn * ctn
            tp -= np * ctn
            cnp = int(floor(np / pp + 1))
            nn -= pn * cnp
            np -= pp * cnp
            ctn = min(0, max(int(floor(tp / np + 1)), int(floor((tp - epsi) / np))))
            tn -= nn * ctn
            tp -= np * ctn
        else:
            cpn = int(floor(pp / np + 1))
            pn -= nn * cpn
            pp -= np * cpn
    return tn

n = 13371337
input_size = 74 * 8 - 1

'''
alpha = mpf(0)
for k in range(1, n + 1):
    if k % 100000 == 0:
        print(k, alpha)
    alpha += mpf(pow(2, n - k, 8 * k)) / mpf(k)
    if alpha >= mpf(8):
        alpha -= mpf(8)

for i in range(1, mp.prec + input_size + 20):
    alpha += 1 / mpf((n + i) << i)
'''
# precalculated
alpha = mpf('4.7396117340837793711371297775036183456741618715118745733571476638760829983723876344914685376828064293054935338817988540584046774591521643231150981482047557980855503123359010052926884736466815909325647295188463901910074175981042315574350877903700718989528185250518628945966687769202441377531204712225329763121391382541705273557338449007205782846746499505157358534818651117420356302405977063896739000105681987827910687898735470250468871840247058781837816933498583050066100637509951279529261863673224374401968021253481900071395644126972753122498565589124175006886421727505463660907430624967938300329455318928094275550112851762670695669161116354496301425292099081546261717220201028050470557451091843631970855346867417603303085192852905225722657325423293711552774464756100491089040348388984263696300329243')

logger.info(f'alpha = {alpha}')

con = Socket(host, int(port))
line = con.recvline()
logger.info(line)
decoded = int.from_bytes(line.split(b"'")[-2], byteorder='big')
assert(decoded.bit_length() == input_size)

logger.info(f'decoded = {decoded}')

encoded = minimize_dec_part_by_error(alpha, -log(mpmathify(decoded), 2), log(mpmathify(decoded+1), 2) - log(mpmathify(decoded), 2))
logger.info(f'encoded = {encoded}')

con.sendline(str(encoded).encode())
flag = con.recvline()
if b'TSGCTF{' in flag:
    logger.info(flag)
    con.close()
    sys.exit(0)

sys.exit(1)

