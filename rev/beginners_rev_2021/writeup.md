###### tags: `TSG CTF 2021`

# TSG CTF 2021 Beginner's Rev Author's Writeup

author: [@m1kit](https://twitter.com/m1kit)

## Problem Overview

You are given a binary that tells you if a flag is correct or not.

## Hints

- Hint 1: Try to run the given program. You should get somehow helpful information about the flag.
- Hint 2: Do you know [ghidra](https://ghidra-sre.org/)? To understand the behavior of the program, you need to do some static analysis.
- Hint 3: Don't spend too much on reading the code. Once you get an idea of the behavior, I recommend you to try some dynamic analysis with various tools.
- <details>
      <summary>Hint 4:</summary>
      There are some interesting system calls.
  </details>
- <details>
      <summary>Hint 5:</summary>
      32 characters, 32 processes
  </details>
- <details>
      <summary>Hint 6:</summary>
      You can use strace to observe system calls.
  </details>

🙈 Solution below

👇

👇

👇

👇

👇

👇

## Solution

### Run

As mentioned in the hint, we can run the program first.

```
❯ ./beginners_rev
give me exactly one argument

❯ ./beginners_rev aaa
give me an argument with 32 chars

❯ ./beginners_rev aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
wrong
```

Now we know this programs determine correctness of something with 32 chars length.

### Read

Next, let's read the program with ghidra.

We can see the entrypoint like this.
It calls `check` only if it has 32 chars.

```c=
undefined8 main(int param_1,long param_2) {
  char *__s;
  size_t sVar1;
  undefined8 uVar2;

  if (param_1 == 2) {
    __s = *(char **)(param_2 + 8);
    sVar1 = strlen(__s);
    if (sVar1 == 0x20) {
      uVar2 = check(__s);
      return uVar2;
    }
    puts("give me an argument with 32 chars");
  }
  else {
    puts("give me exactly one argument");
  }
  return 1;
}
```

Let's see `check`.
There are some interesting system calls!

```c=
byte check(long param_1) {
  __pid_t _Var1;
  int iVar2;
  int iVar3;
  int iVar4;
  uint uVar5;
  long in_FS_OFFSET;
  byte bVar6;
  undefined local_34;
  byte local_33;
  long local_30;

  uVar5 = 0;
  iVar4 = 0;
  iVar3 = 0;
  local_30 = *(long *)(in_FS_OFFSET + 0x28);
  do {
    _Var1 = fork();
    iVar4 = iVar4 + 1;
    if (_Var1 == 0) {
      iVar4 = 0;
      uVar5 = uVar5 | 1 << ((byte)iVar3 & 0x1f);
      iVar2 = open("/dev/null",1);
      dup2(iVar2,1);
    }
    iVar3 = iVar3 + 1;
  } while (iVar3 != 5);
  iVar3 = iVar4 + -1;
  iVar2 = is_correct((int)*(char *)(param_1 + (int)uVar5),uVar5);
  bVar6 = iVar2 == 0;
  if (iVar4 != 0) {
    do {
      iVar3 = iVar3 + -1;
      wait(&local_34);
      bVar6 = bVar6 | local_33;
    } while (iVar3 != -1);
  }
  if (bVar6 == 0) {
    puts("correct");
  }
  else {
    puts("wrong");
  }
  if (local_30 == *(long *)(in_FS_OFFSET + 0x28)) {
    return bVar6;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

The key point is the program calls `fork()` five times in `for`-loop.
Therefore we have 32 processes, and each of them checks one character in the flag around line number 29.

Hope this rough illust of 4 processes example will help you.
![](https://i.imgur.com/yigfqUA.png =400x400)

After that results from processes are aggregates around line number 35.
![](https://i.imgur.com/4diKGEL.png =400x400)

Each process prints the result to stdout at line number 38-43, however, only the message from the root process is visible since anything else is redirected to `/dev/null` at line number 23.

## Solve

With [strace](https://man7.org/linux/man-pages/man1/strace.1.html) command, you can observe system calls executed.
We can use this to check the number of times ` puts("correct");` has been called.

```shell
strace -f ./dist/beginners_rev "$1" 2>&1 | grep correct | wc -l
```

We can create a simple brute force script to determine the flag.
Note that you need to check from the back to the front, due to the structure of the process tree.

```python
import subprocess
import string

def oracle(v):
  p = subprocess.Popen(["./the_magic_oracle_above.sh", v], stdout=subprocess.PIPE)
  output, _ = p.communicate()
  return int(str(output, 'ascii'))

ans = ['*'] * 32
for i in range(31,-1,-1):
  for c in string.printable:
    ans[i] = c
    flag = ''.join(ans)
    if oracle(flag) == 32 - i:
      break
print(flag)
```

## Alt 1

[@moratorium08](https://twitter.com/moratorium08)'s solution

Alternatively, you can patch the binary to remove `dup2(open("/dev/null", 1),1);`.
Now you can see the number of "correct"s in your stdout.

## Alt 2

[@taiyoslime](https://twitter.com/taiyoslime)'s solution

You can write a gdb script to leak a hint for the flag.
But you need some efforts to avoid anti-debugging codes in `is_correct` function.

FYI: this is my anti-debugging mechanism.

```c
if (__builtin_return_address(0) - (void *)check != 0x5f) {
    fputs("This function may not work properly with a debugger.", stderr);
}
```

## Appendix

Here's our original C code for `check`.

```c
int check(char *flag)
{
  int index = 0, count = 0;
  for (int i = 0; i < 5; i++) {
    if (fork()) {
      count++;
    } else {
      count = 0;
      index |= 1 << i;
      dup2(open("/dev/null", O_WRONLY), 1);
    }
  }

  int result = !is_correct(flag[index], index);
  while (count--) {
    int status;
    wait(&status);
    result |= WEXITSTATUS(status);
  }

  if (result == 0) {
    printf("correct\n");
  } else {
    printf("wrong\n");
  }
  return result;
}
```
