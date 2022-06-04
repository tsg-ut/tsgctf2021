# Kotlin Lovers Society 日本語writeup

## 問題概要
以下の画像をSGIフォーマットに変換してPOSTするとフラグが得られます．
但し，ファイルサイズは3760bytesまでです．

![](../solver/result/kls_symbol.png)

ちなみに，最初に言っておくとKotlinはマジで関係ない．

## 調査
### ステップ1: ファイルサイズを気にせず変換
- `Pillow`で変換する
  - 問題のサーバーもPillowを使っているので試す価値はある
  - しかし出てくるファイルは49KBで論外
- [convertio](https://convertio.co/ja/png-sgi/)で変換する
  - 裏で何が動いているのかわからないが，6215bytesのファイルが出てくる

同じ画像ファイルでもファイルサイズが違います．不思議〜〜

### ステップ2: SGIエンコードの仕様と実装
1995年くらいに策定された仕様ですが，Wikipediaとかもあるのでそこまで苦労せずに仕様を見つけることができます．
また，`Pillow`の実装を読むと理解が捗ります．

- [The SGI Image File Format](http://paulbourke.net/dataformats/sgirgb/sgiversion.html)
- [SigImagePlugin.py](https://github.com/python-pillow/Pillow/blob/master/src/PIL/SgiImagePlugin.py)

どうやら，先頭512バイトはヘッダになっていていろいろな情報を含んでいるようです．

|      Size  | Type   | Name      | Description   |
|-|-|-|-|
|    2 bytes | short  | MAGIC     | IRIS image file magic number |
|    1 byte  | char   | STORAGE   | Storage format |
|    1 byte  | char   | BPC       | Number of bytes per pixel channel  |
|    2 bytes | ushort | DIMENSION | Number of dimensions |
|    2 bytes | ushort | XSIZE     | X size in pixels  |
|    2 bytes | ushort | YSIZE     | Y size in pixels  |
|    2 bytes | ushort | ZSIZE     | Number of channels |
|    4 bytes | long   | PIXMIN    | Minimum pixel value |
|    4 bytes | long   | PIXMAX    | Maximum pixel value |
|    4 bytes | char   | DUMMY     | Ignored |
|   80 bytes | char   | IMAGENAME | Image name |
|    4 bytes | long   | COLORMAP  | Colormap ID |
|  404 bytes | char   | DUMMY     | Ignored |

注目するべきは，最初の方にある`STORAGE`というフィールドです．

> STORAGE - specifies whether the image is stored using run
	length encoding (RLE) or not (VERBATIM).   If RLE is used, the value 
  of this byte will be 1.  Otherwise the value of this byte will be 0.
	The only allowed values for this field are  0 and 1.

とあるように，`VERBATIM`と`RLE`の2種類のエンコード方法があります．
`VERBATIM`は何もエンコードせずにバイナリとして吐くだけなのでファイルサイズが爆発しそうです．
今回の画像はかなりシンプルなので[ランレングス圧縮](https://en.wikipedia.org/wiki/Run-length_encoding)が刺さりそう．

しかし，`Pillow`の`SgiImagePlugin.py`を読むと以下のように書いてあります．

```py
def _save(im, fp, filename):
    #snip#

    # Run-Length Encoding Compression - Unsupported at this time
    rle = 0
```
RLEエンコードされたSGI画像の読み込みはできるけど，書き出しはサポートされていないんですね．
なので，ステップ1で出てきたファイルサイズがやたらと大きかったわけです．(127x127x3+512で48899bytes)

convertioは裏で何を使っているのか知りませんが，RLEエンコードした画像を吐いてくれています．
しかしRLEエンコードされていてもサイズが2500bytesあまりオーバーしています．
RLEエンコードの仕様をもう少し理解し，出力を手動で最適化する必要がありそうです．

### ステップ3: RLEエンコードの仕様
仕様書のRLEエンコードの部分をもう少し理解します．
RLEエンコードがオンになっていると，画像をチャンネルとy座標ごとに細切れにし，1次元のデータ`row`の集合として保存するようになります．つまり，`画像の高さ`x`画像のチャンネル数`の数だけ`row`があり，これを`tablen`と呼びます．今回は，一辺127でRGBの3チャンネルなので`tablen`は127x3=381です．

RLEエンコードでは512バイトのヘッダの次に各`row`の情報がどこに配置されているかを指示するデータ領域があります．データ領域は`start`と`length`で表現され，画像の`start`byte目を起点として`length`個の命令が連続して配置してあるという情報を含みます．

| Size  | Type   | Name      | Description |
|-|-|-|-|
| tablen longs | long   | STARTTAB  | Start table |
| tablen longs | long   | LENGTHTAB | Length table |


それぞれの数字は32bit整数なので，今回の場合はこのデータ領域に381x4x2=3048bytesかかります．
ヘッダの512bytesを含めると，最低限必要な領域だけで3560bytesありますね．
問題で要求されているのは3760bytes以下ですから，200bytesの余裕しかありません．

残り200bytesの部分には，実際にRLEエンコードされた各`row`のデータを格納します．
実データは命令とオペランドの繰り返しで，命令に従いデータが画像の左側から詰められていきます．
```
[命令|データ][命令|データ][命令|データ]...
```

命令`op`は常に1バイトでその値によって意味が違います:
- `0x00` <= `op` <= `0x7F`のとき: 後続の1バイトを`op`回だけ繰り返す
  - 例えば，`053F`であれば，`row`の左側5ピクセルに`3F3F3F3F3F`が詰め込まれます
- `0x80` <= `op` <= `0xFF`のとき: 後続の`op & 0x7F`バイトをコピーする
  - 例えば，`850102030405`であれば，`row`の左側5ピクセルに`0102030405`が詰め込まれます

前者がいわゆるランレングス圧縮で，後者は愚直なデータコピーですね．

ところで，我々は381`row`sの情報を200bytesで記述しなければなりません．
いくらRLEでサボれるとはいえ，この形式では1`row`あたり0.5byteは到底不可能であることがわかります．

## 解法
KotlinのシンボルをSGIの仕様にのっとってコードゴルフしていきます．

### Shared Data Segment
実は，ヒントがSGIの仕様書に書いてあります．

> It is possible for two identical rows to share compressed scanline
> data.  A completely white image could be written as a single compressed
> scanrow and having all table entries point to that scanrow.
>
> Another little hack that should work is if you are writing out a RGB 
> RLE file, and a particular scan line is achromatic (greyscale), you 
> could just make the r, g and b rows point to the same data!!

前述のように各`row`のデータの格納領域は`start`と`length`という2つの情報によって指定されていますが，複数の`row`が同じ領域を共有することができます．
これは，問題画像の以下の領域で活用できそうです．

(Rの下半分とBの上半分の図)

これにより64`row`s程度の情報を省略できます．

### Early Return
データ領域の命令`0x00`や`0x80`は長さ0のデータを展開するという意味合いになり，実質的には何もしない命令に見えます．
`Pillow`はこれをどう扱うのでしょうか?

[SigRleDecoder.c](https://github.com/python-pillow/Pillow/blob/master/src/libImaging/SgiRleDecode.c#L85-L87)を読むと，その命令があった場合はその`row`の展開をその場で停止し，次の`row`に移るとされています．

よって，`row`の命令の最後に`0x00`や`0x80`を置いてもうまくデコードに成功します．
これ単体ではデータ量が増えるだけですが，これを使ったテクニックがいくつか存在します．

### Data on Lengthtab
Early Returnを使うと，`length`で指定された命令数を無視して`row`のデコードが中止できます．
よって，`length`に十分に大きい任意の整数を入れたとしても，全データ領域の終端を`0x00`で指定しておけばエンコード自体は成功します．

また，`start`で指定するオフセットはヘッダも入れた画像先頭からのオフセットで，何故かLengthtab領域も指定することができます．

よって，本来は命令長を格納するLengthtab領域に`row`のデータを格納することができます(!)
これをすると，全`row`の末尾に`0x00`を付加するため余計な300bytes程度が増えますが，Lengthtab領域全体の1524bytesをデータの保持に使えるため差し引きではかなりお得です．

しかし，少しだけ気をつけなければいけない点があります．
Lengthtab領域は本来命令長を保存する領域なので，`length`が0などになると対応する`row`の画像のデコードがうまく行われません．また，`length`が符号付き整数として扱われる都合，最上位ビットが1だと負数となり同様にうまくいきません．Lengthtab領域におけるデータ配置をうまく工夫することで，`length`としても有効ながらデータとしても読み取れる状態を作らないといけません．

### Buffer Reuse
`row`の長さ(=画像幅127)に対して命令数が不足している場合や，Early Returnを用いた場合などにおいて，
必要な画素が全て書き込まれない状況が発生し得ます．
そのような場合，何が起こるのでしょうか?

RLEエンコードされたデータは，[一時的なバッファ](https://github.com/python-pillow/Pillow/blob/master/src/libImaging/SgiRleDecode.c#L250)に展開されます．
その後，バッファが満たされているという前提で画像にコピーされます．
よって，バッファに十分な画素が入っていない場合は，**直前に**バッファに入っていた値が再利用されます．

何故か知らないのですが，RLEデータの展開は画像の下から上に向かって行われ，バッファはチャンネルごとに独立です．
よって，直前にバッファに入っていた値というのは同じチャンネルの1つ下の`row`を指します．

この仕様を利用すると，上の行と下の行に共通部分があった場合，上の行のデータの一部を省略できる可能性があります．
具体的には，以下の部分でこのテクニックを利用できます．

### Data as Instruction
ここまでのテクニックを実践すればかなり近いサイズまで持ってこれていると思います．
もしかしたら，このテクニックなしでも制約を満たせる可能性もあるかも．

さて，最後のテクニックですが，今までは命令(繰り返し回数)であるbyteと輝度でアルバイトを分けていました．
これを変え命令でもあり輝度でもあると解釈できるbyteを作り出すことはできないでしょうか?

例えば，R,Bチャンネルには輝度`0xff`のセルが多くあります．
これを命令と解釈すると，「続く127ピクセルのデータをコピーせよ」となります．
今回の画像幅は127ぴったりなので，これを使うことができそうです．

具体的には，以下のようなデータを用意します．
```
FF FF FF FF ... FF 7F 00 00 00 ... 00 00 00
```
`start`で`FF`のどれかを指定すると，R, Bチャンネルに数多くある「左が`FF`である場所から右が`00`」みたいなパターンが表現できます．
指定する`FF`を変えることで，`FF`の長さが変えられるので，結果的にこのデータ列だけでR,Bチャンネルの約128`row`sのデータをまとめて格納できることになります．

おそらく，上の全てのテクニックを全て実装すれば多少の余裕を持って制約を満たす画像を生成できるのではないでしょうか．
