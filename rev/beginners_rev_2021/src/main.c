
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>


int is_correct(int v, int off);

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

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("give me exactly one argument\n");
    return 1;
  } else if (strlen(argv[1]) != 32) {
    printf("give me an argument with 32 chars\n");
    return 1;
  }

  return check(argv[1]);
}

const int m = 367;
const unsigned char key[] = {
    0x9e,
    0xa5,
    0x43,
    0x3c,
    0x3d,
    0xe5,
    0x50,
    0x95,
    0x29,
    0xfb,
    0x03,
    0x34,
    0xf6,
    0x6d,
    0xf7,
    0x9a,
    0x5e,
    0x8a,
    0x6f,
    0x0f,
    0xae,
    0x6a,
    0x78,
    0x41,
    0x02,
    0x46,
    0x8b,
    0xae,
    0xb6,
    0x83,
    0x09,
    0x4f,
    0x54,
    0x74,
    0x8d,
    0xf4,
    0x79,
    0xd2,
    0xfe,
    0x2d,
    0x78,
    0x1b,
    0x11,
    0x57,
    0xb7,
    0x9f,
    0x4e,
    0xc4,
    0x52,
    0x9e,
    0xf5,
    0xff,
    0x56,
    0x71,
    0x3c,
    0x1b,
    0x60,
    0x22,
    0x9c,
    0x56,
    0xa7,
    0xcf,
    0x8e,
    0x45,
    0x16,
    0x5c,
    0xa5,
    0xf4,
    0x28,
    0xa0,
    0x30,
    0x57,
    0xa5,
    0xb1,
    0xc9,
    0xc4,
    0x86,
    0x3e,
    0xb8,
    0x13,
    0x44,
    0x4d,
    0xbf,
    0x97,
    0xe4,
    0x06,
    0x96,
    0x07,
    0x8b,
    0x9f,
    0x52,
    0x12,
    0x92,
    0xc6,
    0xc0,
    0x8a,
    0x69,
    0xf5,
    0xa5,
    0x9d,
    0xf3,
    0x3b,
    0xb6,
    0x99,
    0x86,
    0xd9,
    0x67,
    0x32,
    0xb1,
    0xbf,
    0xb8,
    0x2e,
    0x58,
    0x55,
    0xb0,
    0x9c,
    0x65,
    0x9e,
    0x9f,
    0xe3,
    0xf0,
    0xbf,
    0xcf,
    0xcd,
    0xde,
    0xfd,
    0x34,
    0x31,
    0x78,
    0x55,
    0x6e,
    0x01,
    0x74,
    0xd7,
    0xa8,
    0x26,
    0xff,
    0xd6,
    0xcc,
    0x99,
    0x51,
    0xfb,
    0xf6,
    0xf4,
    0x03,
    0xfa,
    0x61,
    0xdf,
    0x41,
    0x98,
    0x0d,
    0xbd,
    0xbf,
    0x88,
    0x44,
    0x5e,
    0x56,
    0xd2,
    0xa9,
};
const unsigned int enc[] = {
    0x00b9,
    0x00b4,
    0x00c1,
    0x006b,
    0x0145,
    0x0094,
    0x00fe,
    0x0156,
    0x0038,
    0x00a0,
    0x0152,
    0x008f,
    0x003a,
    0x0121,
    0x016a,
    0x00f8,
    0x013f,
    0x0153,
    0x005c,
    0x0042,
    0x00f8,
    0x0048,
    0x0015,
    0x00e5,
    0x007a,
    0x00ce,
    0x0065,
    0x00eb,
    0x0071,
    0x0064,
    0x002d,
    0x0106,
};

inline int inv(int v)
{
  for (int x = 1; x < m; x++)
  {
    if ((v * x) % m == 1)
    {
      return x;
    }
  }
  return -1;
}

int is_correct(int v, int off)
{
  // I hope you don't analyze this
  if (__builtin_return_address(0) - (void *)check != 0x5f) {
    fputs("This function may not work properly with a debugger.", stderr);
  }

  const unsigned char *p = key + off;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + __builtin_return_address(0) - (void *)check) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v + *p++) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * *p++) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v * *p++) % m;
  v = (v + *p++) % m;
  v = (v + *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v + __builtin_return_address(0) - (void *)check) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v + *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + __builtin_return_address(0) - (void *)check) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * inv(*p++)) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * *p++) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v + *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + __builtin_return_address(0) - (void *)check) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + __builtin_return_address(0) - (void *)check) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v * inv(*p++)) % m;
  v = (v + m - *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + *p++) % m;
  v = (v * *p++) % m;
  v = (v + m - *p++) % m;
  v = (v * *p++) % m;
  v = (v * inv(*p++)) % m;
  v = (v + __builtin_return_address(0) - (void *)check) % m;
  // fprintf(stderr, "%02d: %04x\n", off, v);
  return v == enc[off];
}