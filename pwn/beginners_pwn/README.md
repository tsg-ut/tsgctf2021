# Beginner's Pwn 2021

I heard pwners could utilize an off-by-one error to capture the flag.

Hint for beginners:

- First of all, download the attachments and see the source file.
- What you have to do is to guess the flag... No, fake the flag. That means you have to somehow make `strncmp(your_try, flag, length) == 0` hold.
- There is little attack surface. Check the spec of suspicious functions.

### 日本語問題文

pwnerはoff-bye-oneエラー使ってフラグが取れるって聞きました。

初心者向けヒント:

- まず、アタッチメントファイルをダウンロードしてソースコードを見てください
- あなたがすべきことは、フラグを推測すること...ではなくフラグを"偽装"することです。つまり `strncmp(your_try, flag, length) == 0` が成立するようになんとかしてください。
- 実際のところ、攻撃できそうな所は限られていると思います。怪しい関数の仕様を調べてみてください。

## Writeup

https://hackmd.io/@moratorium08/SJiWXXvNF

### estimated difficulty

warmup

