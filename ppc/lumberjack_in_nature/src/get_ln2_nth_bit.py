from mpmath import *
import sys

def printbin(n):
  k = 0
  if n >= mpf(1):
    n -= mpf(1)
    k += 1
  sys.stdout.write(bin(k))
  sys.stdout.write('.')
  for i in range(10000):
    n *= 2
    if n >= 1:
      sys.stdout.write('1')
      n -= 1
    else:
      sys.stdout.write('0')
  print('')

n = 123456789 - 64
# n = 1000000
mp.dps = 1000
mp.pretty = True
ans = mpf(0)

for k in range(1, n + 1):
  if k % 100000 == 0:
    print(k, flush=True)
  ans += mpf(pow(2, n - k, k)) / mpf(k)
  if ans >= mpf(1):
    ans -= mpf(1)

prev_ans = mpf(0)
k = n
while prev_ans != ans:
  k += 1
  prev_ans = ans
  ans += mpf(2) ** (n - k) / mpf(k)

printbin(ans)
