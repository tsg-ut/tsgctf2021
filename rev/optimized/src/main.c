#include <openssl/conf.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define NOP __asm__("nop")

#define ten(a)     a;a;a;a;a;a;a;a;a;a
#define ten2(a) ten(ten(a))
#define ten4(a) ten2(ten2(a))

static inline uint64_t computeM_u32(uint32_t d) {
  return UINT64_C(0xFFFFFFFFFFFFFFFF) / d + 1;
}

// fastmod computes (a % d) given precomputed M
static inline uint32_t fastmod_u32(uint32_t a, uint64_t M, uint32_t d) {
  uint64_t lowbits = M * a;
  return ((__uint128_t)lowbits * d) >> 64;
}

// given precomputed M, checks whether n % d == 0
static inline bool is_divisible(const uint32_t v, const uint64_t M) {
  return v * M < M;
}

// Check if input % d == ans % d. Inlining should be enabled to optimize out the actual answer value.
static inline bool check(const uint32_t input, const uint32_t ans,
                         const uint32_t d) {
  return fastmod_u32(input, computeM_u32(d), d) == ans % d;
}

// Check if input % d == 0.
static inline bool check2(const uint32_t input, const uint32_t d) {
  return is_divisible(input, computeM_u32(d));
}

static void handleErrors(void) {
  ERR_print_errors_fp(stderr);
  // Required for UPX to correctly compress
  ten4(NOP);
  abort();
}

int main() {
  uint32_t k[8];
  printf("Enter password: ");
  fflush(stdout);
  if (scanf("%u %u %u %u", &k[0], &k[1], &k[2], &k[3]) == 4) {
    if (check(k[0], 772928896, 176017) && check(k[0], 772928896, 215737) &&
        check(k[1], 2204180909, 224057) && check(k[1], 2204180909, 238291) &&
        check2(k[2], 3460307) && check(k[2], 4273479145, 163321) &&
        check2(k[3], 8840597) && check(k[3], 1334930147, 244837)) {
      EVP_CIPHER_CTX *ctx;
      int len;
      int plaintext_len;
      unsigned char plaintext[256];
      const unsigned char ciphertext[20] = {
          0x3a, 0x44, 0xcc, 0x77, 0x5c, 0x17, 0x5e, 0xc0, 0xdb, 0xe0,
          0xe7, 0xfa, 0xe3, 0x17, 0x4c, 0x21, 0xd0, 0x93, 0x7a, 0xc6,
      };
      int ciphertext_len = sizeof(ciphertext) / sizeof(ciphertext[0]);

      for (int i = 0; i != 4; ++i) {
        k[i + 4] = k[i];
      }
      unsigned char *key = (unsigned char *)k;
      unsigned char *iv = (unsigned char *)"welcometotsgctfaaa";

      if (!(ctx = EVP_CIPHER_CTX_new()))
        handleErrors();

      if (1 != EVP_DecryptInit_ex(ctx, EVP_chacha20(), NULL, key, iv))
        handleErrors();

      if (1 !=
          EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len))
        handleErrors();
      plaintext_len = len;

      if (1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len))
        handleErrors();
      plaintext_len += len;

      EVP_CIPHER_CTX_free(ctx);
      printf("%s\n", (char *)plaintext);
    } else {
      printf("Wrong!\n");
    }
  } else {
    printf("Bad format!\n");
  }
}
