# TSGCTF 3 optimized (rev) explainer

author: @ishitatsuyuki

---

This reversing challenge involved a "crack the password" style Linux program, with packing as a layer of obfuscation.

## Solution

### Unpacking

Running `file` on the binary gives some strange results:

```
$ file optimized                
optimized: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, no section header
```

And `binwalk` does not give us any additional info either.

A (seemingly) statically linked executable without section headers is a good sign that the binary was packed. In such cases, it is a good idea to try taking the coredump of a live instance using a debugger.

Run the binary using `gdb`, interrupt it, and type in `gcore` to get a coredump that can be used to analyze the actual assembly.

#### Alternative: restoring UPX header

The binary in question was actually packed by UPX, but the strings were replaced by unrelated ones. It's a common obfuscation strategy used for Linux binaries<sup>[1]</sup>.

Even in presence of anti-unpacking techniques like [2], it is still sometimes possible to identify the packer used if you're familiar with their prologue (entrypoint assembly). For this challenge, all you need to fix is to replace the 3 occurrences of `tsg_` by `UPX!`. After that, the original binary can be obtained through `upx -d optimized`.

[1]: https://github.com/radareorg/r2con2018/blob/master/talks/unpacking/Unpacking-a-Non-Unpackables.pdf

[2]: https://cujo.com/upx-anti-unpacking-techniques-in-iot-malware/

### Cracking the password

A lot of SIMD instructions are used in the password check routine, and many tools are confused by their presence. However IDA seems to do a decent job with the code recovery:

```c=
if ( _mm_movemask_epi8(
         _mm_cmpeq_epi8(
           _mm_slli_si128((__m128i)0x9569uLL, 8),
           _mm_slli_si128(
             (__m128i)(((0x2AF91 * (unsigned __int128)(0x5F50DDCA7B17LL * (unsigned __int64)v5)) >> 64) & 0x3FFFF),
             8))) != 0xFFFF
    || _mm_movemask_epi8(
         _mm_cmpeq_epi8(
           _mm_slli_si128((__m128i)0x26CF2uLL, 8),
           _mm_slli_si128(
             (__m128i)(((0x34AB9 * (unsigned __int128)(0x4DC4591DAC8FLL * (unsigned __int64)v5)) >> 64) & 0x3FFFF),
             8))) != 0xFFFF
    || _mm_movemask_epi8(
         _mm_cmpeq_epi8(
           _mm_slli_si128((__m128i)0x20468uLL, 8),
           _mm_slli_si128(
             (__m128i)(((0x36B39 * (unsigned __int128)(0x4AE11552DF1ALL * (unsigned __int64)v6)) >> 64) & 0x3FFFF),
             8))) != 0xFFFF
    || _mm_movemask_epi8(
         _mm_cmpeq_epi8(
           _mm_slli_si128((__m128i)0x3787AuLL, 8),
           _mm_slli_si128(
             (__m128i)(((0x3A2D3 * (unsigned __int128)(0x46680B140EFFLL * (unsigned __int64)v6)) >> 64) & 0x3FFFF),
             8))) != 0xFFFF
    || 0x4D935BBD3E0LL * (unsigned __int64)v7 >= 0x4D935BBD3E0LL
    || _mm_movemask_epi8(
         _mm_cmpeq_epi8(
           _mm_slli_si128((__m128i)0x5563uLL, 8),
           _mm_slli_si128(
             (__m128i)(((0x27DF9 * (unsigned __int128)(0x66B9B431B9EDLL * (unsigned __int64)v7)) >> 64) & 0x3FFFF),
             8))) != 0xFFFF
    || 0x1E5D2BE81C5LL * (unsigned __int64)(unsigned int)v8[0] >= 0x1E5D2BE81C5LL
    || _mm_movemask_epi8(
         _mm_cmpeq_epi8(
           _mm_slli_si128((__m128i)0x133E7uLL, 8),
           _mm_slli_si128(
             (__m128i)(((0x3BC65 * (unsigned __int128)(0x448626500938LL * (unsigned __int64)(unsigned int)v8[0])) >> 64) & 0x3FFFF),
             8))) != 0xFFFF )
  {
    v2 = "Wrong!";
    goto LABEL_17;
  }
```

While not being the intended solution, an easy way to solve the puzzle is to exhaustively search the space of 32-bit integers for each of the 4 input values. The search took around 15 seconds in an internal test.

~~I hope you did not ran angr for hours without dealing with the packing~~

With a little more effort, it is possible to get rid of the SIMD intrinsics and get the code in a more readable state. The check consists from 2 variants, and the first variant looks like this (negated for clarity):

```c
0x9569uLL == (0x2AF91 * (__uint128_t)(0x5F50DDCA7B17LL * (uint64_t)v5)) >> 64
```

After trying a few random values for `v5`, one notices that the right hand side is equivalent to `v5 % 0x2AF91`. The first 2 pair of the conditions consists of two such constraints; the key is easily computable through the extended GCD algorithm.

The second variant, looks like this:

```c
0x4D935BBD3E0LL * (uint64_t)v7 < 0x4D935BBD3E0LL
```

At first glace, it's quite hard to figure out what is going on here. But the constant `0x4D935BBD3E0LL` is suspiciously similar to the constant `0x5F50DDCA7B17LL` in the `v5` case above. These numbers actually corresponds to the fixed-point complement of the divisor: for example, `0x5F50DDCA7B17*0x2AF91=0x10000000000027107`. So what does the second formula really do?

Well, if you have been able to follow up to this point, you already have an example that satisfies this. By diving `(1<<64)` by `0x4D935BBD3E0`, we obtain `3460306.999999531`. Now, rounding this and putting this into the complement formula, we get that `0x4D935BBD3E0*0x34CCD3=0x100000000002621A0`. Keep in mind that this is 64-bit integer so the `0x10000000000000000` part is dropped!

So what this is really about is a divisibility check. It translates to `v7 % 0x34CCD3 == 0`, which means that the key is also computable in the same method that worked for the first kind of constraints.

The four keys, solved with the extended GCD algorithms, are `772928896 2204180909 4273479145 1334930147`. Feeding this to the program gives the flag:

```
TSGCTF{F457_m0dul0!}
```

If you got interested in the mathematical background behind this, you should definitely check out the original research<sup>[3]</sup> that inspired this challenge.

[3]: https://lemire.me/blog/2019/02/08/faster-remainders-when-the-divisor-is-a-constant-beating-compilers-and-libdivide/