import subprocess
import string

def oracle(v):
  p = subprocess.Popen(["./oracle.sh", v], stdout=subprocess.PIPE)
  output, _ = p.communicate()
  return int(str(output, 'ascii'))

ans = ['*'] * 32
for i in range(31,-1,-1):
  for c in string.printable:
    ans[i] = c
    flag = ''.join(ans)
    if oracle(flag) == 32 - i:
      break
print(flag) # TSGCTF{y0u_kN0w_m@ny_g0od_t0015}
