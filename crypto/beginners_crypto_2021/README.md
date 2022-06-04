# Beginner's Crypto 2021

## Author

@hakatashi

## Description

_J'ai apporté avec moi les trois mousquetaires du ramen._

Hint for beginners:

* The attached file contains a Python script named `beginners_crypto_2021.py` and a text file named `output.txt`. These two files indicate that the latter text file was the result of running the former Python script.
* You can see that the Python script reads the file `flag.txt`, encrypts it, and outputs it. Since `flag.txt` is not included in the distribution file, you will have to guess from the output results to find and answer the contents of the original `flag.txt`. This will be the purpose of this question.
* You will need a cryptographic library called [Pycryptodome](https://pycryptodome.readthedocs.io/) to run the attached Python script. Please run `pip install pycryptodome` to install it beforehand.
* In the Python script, there is a line `from secret import e` that reads the secret parameter `e` from `secret.py`, which is used to encrypt the flag. `secret.py` is of course not included in the distribution, so you will have to guess it.
  * To run the script locally, you will need to create a temporary `secret.py` or rewrite the source code to define the parameters directly.
* Once you get a numerical value that represents the flag, convert it to a string using the reverse procedure of reading `flag.txt` and answer it. If you have the correct flag format (`TSGCTF{...}`), you've won!

- [dist](dist)

---

```
c1「うっす、よろしく。」
c2「がんばります、よろしく。」
c3「よっす、どうも。」
```

初心者向けヒント:

* 添付されたファイルには `beginners_crypto_2021.py` というPythonスクリプトと `output.txt` というテキストファイルが含まれています。この2つのファイルは、前者のPythonスクリプトを実行した結果が後者のテキストファイルであったということを表しています。
* Pythonスクリプトでは、`flag.txt`というファイルを読み込み、暗号化して出力していることがわかります。`flag.txt` は配布ファイルの中には含まれないので、出力結果から推測して、元の `flag.txt` の内容を求め、回答してください。これが今回の問題の目的となります。
* 添付されたPythonスクリプトを実行するには[Pycryptodome](https://pycryptodome.readthedocs.io/)という暗号ライブラリが必要になります。`pip install pycryptodome` を実行してあらかじめインストールしておいてください。
* Pythonスクリプト中に `from secret import e` という行がありますが、この行ではフラグを暗号化する際に用いる秘密のパラメーター `e` を `secret.py` から読み取っています。`secret.py` は当然配布ファイルには含まれていないので、問題から推測して答えてください。
  * 手元で動かす際には仮の `secret.py` を作成するか、ソースコードを書き換えてパラメーターを直接定義する必要があります。
* フラグを表す数値が得られたら、それを `flag.txt` を読み取った時と逆の手順を用いて文字列に直し、回答してください。正しいフラグ形式 (`TSGCTF{...}`) になっていたら、あなたの勝ちです！

- [dist](dist)

## Estimated Difficulty

Beginner
