###### tags: `TSG CTF 2021`

# TSG CTF 2021 B??e64 Author's Writeup

author: [@m1kit](https://twitter.com/m1kit)

## Problem Overview

- The server generates a 32 chars-length secret string encoded 8 times with base64.
- You can know arbitrarily 124 chars among the 344 chars-length encoded message.
- You need to guess the original secret 8 times consecutively.

## Hint

- <details>
    <summary>Hint 1</summary>
    In a single Base64 encoding, 6 bits of data become 8 bits. Thus there is some redundancy. Can you find redundant parts of some encoded secrets?
  </details>
- <details>
    <summary>Hint 2</summary>
    Assume you have enough information to restore the original message, can you write a brute-force algorithm to restore the original message from a masked base64 string?  
  </details>
- <details>
    <summary>Hint 3</summary>
    To get a good mask, you need to think of heuristic algorithms and/or entropy.
  </details>

🙈 Solution below

👇

👇

👇

👇

👇

👇

## Solution

### Find one possible original message from the masked message

Let's think about brute-forcing the original message from the masked message.

If you fix the first $n$ characters of the original message, the first $\left\lfloor \frac{4}{3}\left\lfloor \frac{4}{3}\left\lfloor \frac{4}{3}\left\lfloor \frac{4}{3}\left\lfloor \frac{4}{3}\left\lfloor \frac{4}{3}\left\lfloor \frac{4}{3}\left\lfloor \frac{4n}{3} \right\rfloor\right\rfloor\right\rfloor\right\rfloor\right\rfloor\right\rfloor\right\rfloor\right\rfloor$ characters of the encoded message are fixed as well.

So, you can try:

- change the first character until the first encoded character matches,
- change the second character until the first two encoded characters match,
- change the third character until the first 22 encoded characters match,
- and so on...

If it does not match, you will need to go back to the previous character.

```python=
def almost_eq(seq, pat):
  return all(s == p or p == '*' for s, p in zip(seq, pat))

def solve(s, n=32, charset=CHARSET):
  assert len(s) == len(enc(' ' * n))

  dr = []
  for i in range(n):
    b = i + 1
    for _ in range(8):
      b = b * 8 // 6
    dr.append(b)
  dr[-1] = len(s)

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
```

By this solver, you can quickly find the lexicographically smallest possible original message. Similarly, you can find the lexicographically largest one.

Let's call the masked message is _unique_ if the lexicographically smallest one and the lexicographically largest one are identical.

### Construct a good mask

I understand there are various approaches to do this. Let me introduce one of them.

I randomly sampled 1000 original messages and encoded them all, and calculated entropy for each character position in encoded messages. Clearly, we want to know a character position with high entropy.

I removed characters from low-entropy ones as long as it keeps _uniqueness_ which we defined above. To determine _uniqueness_, I randomly sampled 32 messages.

By doing this I got this mask:

```
*******??**?***?***???***?*??****??**??**?**?*?**???***?***?*??***?**?**?****?*?**???**?**?**?*?***???*?*****?*???***??***?**?*?*?**?**?**?**?*?***?**??***?*?*?***?***?*?***?*??**??***?****?*?****?*?????****??**?*****??****?**?****???*??**??****??*?***??*?****?*?*??***??*****?*?**?****?**???***?**?**??******???**??***?*?**********************
```

With this mask we can guess 95% of messages correctly, which is sufficient for this problem.

BTW, do you notice there are only 122 `?`s in this mask?
Yes, I increased number of allowed `?`s by two before the competition.

## Appendix

The flag was, `TSGCTF{Ba5e6A_has_a_f1xp0int}`.

I should have written it as "fixpoints", since there are some.

One fixpoint I know is, "".
Clearly, an empty string is a fixpoint for `base64` operation.

Also, we have a fixpoint with infinity length string, starting with "Vm0wd2Qy".

```
❯ echo Vm0wd2Qy | base64
Vm0wd2QyUXkK

❯ echo Vm0wd2QyUXkK | base64
Vm0wd2QyUXlVWGtLCg==
```

In this problem, after 8 times encoding, the first part of the encoded string converges to this fixpoint, so the entropy of the first part is low.
This is why the first few chars are useless when you create a mask.
