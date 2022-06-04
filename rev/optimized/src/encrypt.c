#include <openssl/conf.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void handleErrors(void) {
  ERR_print_errors_fp(stderr);
  abort();
}

int main(int argc, char **argv) {
  uint32_t k[8];
  k[0] = 772928896;
  k[1] = 2204180909;
  k[2] = 4273479145;
  k[3] = 1334930147;
  for (int i = 0; i != 4; ++i) {
    k[i + 4] = k[i];
  }
  if (argc != 2) {
    fprintf(stderr, "Usage: encrypt <FLAG>\n");
    return 1;
  }
  unsigned char ciphertext[65536];
  unsigned char *plaintext = (unsigned char *)argv[1];
  int plaintext_len = strlen(argv[1]);
  unsigned char *key = (unsigned char *)k;
  unsigned char *iv = (unsigned char *)"welcometotsgctfaaa";
  EVP_CIPHER_CTX *ctx;

  int len;

  int ciphertext_len;

  if (!(ctx = EVP_CIPHER_CTX_new()))
    handleErrors();

  if (1 != EVP_EncryptInit_ex(ctx, EVP_chacha20(), NULL, key, iv))
    handleErrors();

  if (1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
    handleErrors();
  ciphertext_len = len;

  if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len))
    handleErrors();
  ciphertext_len += len;

  EVP_CIPHER_CTX_free(ctx);

  printf("const unsigned char ciphertext[%d] = {", ciphertext_len);
  for (int i = 0; i != ciphertext_len; ++i) {
    printf("0x%x, ", ciphertext[i]);
  }
  printf("};\n");
}
