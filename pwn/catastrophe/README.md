# Catastrophe

I love breaking analyses proven to be safe.

### Hint 1.

I heard "value restriction" is important for the soundness of
the OCaml type system.

### Hint 2.

Well, you may think this chall is "unsound hole challenge of
the strage (non-famous?) language"?

This is "partially" no.
First, OCaml is famous! :)

Joking aside (not joking!),
you may notice that this challenge
1. complies to an OCaml VM binary (not native binary!) using `ocamlc` (not `ocamlopt`)
2. executes the VM binary using `ocamlrun`

Here pro tipes: OCaml's VM interpreter is implemented in C!
(c.f.  https://github.com/ocaml/ocaml/tree/4.12/runtime)

That means ...
Let's just leave it at that.


## Catastrophe (日本語)

人の作った型システムを破壊するのが趣味です


### Hint 1.

「value restriction」というのがOCamlの型システムの健全性には大切だってどっかで聞きました

### Hint 2.

えっと、ここまで聞いたら、あなたはこの問題は「謎言語のunsound
bug問」だと思ったりしているかもしれません。

これは、ちょっと違います。
というのも、OCamlは謎言語じゃないから！

という冗談はさておいて（冗談のつもりはないですけど！）、
この問題に取り掛かるにあたって、あなたは次のことに気づくでしょう
1. まずOCamlのVM(nativeなバイナリではなく)に、`ocamlc` を使って( `ocamlopt` ではなく)コンパイルをしている
2. そして、そのバイナリを `ocamlrun`を用いて実行している


ここでPro Tipsをご紹介：OcamlのVMインタプリタはCで実装されています。
(c.f.  https://github.com/ocaml/ocaml/tree/4.12/runtime)

これが意味するところは、、、
話はここまでにしておきましょう

## Writeup

https://hackmd.io/@moratorium08/Sk7puL84Y

### estimated difficulty

Hard

