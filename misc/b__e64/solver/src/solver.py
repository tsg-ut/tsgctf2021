import base64
import string

CHARSET = string.ascii_lowercase + string.digits


def enc(s, encoding='ascii'):
  for _ in range(8):
    s = base64.b64encode(bytes(s, encoding)).decode(encoding)
  return s

def almost_eq(seq, pat):
  return all(s == p or p == '*' for s, p in zip(seq, pat))

def solve(s, n=32, charset=CHARSET):
  assert len(s) == len(enc(' ' * n))

  # フラグのi文字目まで決め打ちするとエンコード結果のdr[i]文字目まで確定する
  dr = []
  for i in range(n):
    b = i + 1
    for _ in range(8):
      b = b * 8 // 6
    dr.append(b)
  dr[-1] = len(s)

  # 先頭から決め打ちできる
  cur = 0
  res = [0] * n
  while cur < n:
    m = ''.join(charset[x] for x in res)
    c = enc(m)
    if almost_eq(c[:dr[cur]], s[:dr[cur]]):
      cur += 1
    else:
      res[cur] += 1
      rc = cur
      while res[rc] == len(charset):
        res[rc] = 0
        rc -= 1
        res[rc] += 1
  return ''.join(charset[x] for x in res)

if __name__ == '__main__':
  import sys
  ans1 = solve(sys.argv[1])
  print(ans1)
  ans2 = solve(sys.argv[1], charset=''.join(reversed(CHARSET)))
  if ans1 == ans2:
    print('Unique')
  else:
    print('Ambiguous')
