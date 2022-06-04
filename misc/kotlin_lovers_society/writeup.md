###### tags: `TSG CTF 2021`

# TSG CTF 2021 Kotlin Lovers Society Author's Writeup

author: [@m1kit](https://twitter.com/m1kit)

## Task Overview

If you convert the following image to SGI format and POST it, you will get a flag.
However, the file size is limited to 3760bytes.

![](https://i.imgur.com/oIzkoiZ.png)

Note that Kotlin is totally unrelated to this task.

## Hints

- <details>
      <summary>Hint 1:</summary>
      <a href="https://www.fileformat.info/format/sgiimage/spec/2a67b5c53bd84e8aa1a18ab1a6d3e832/view.htm">SGI Image Spec</a>
  </details>
- <details>
      <summary>Hint 2:</summary>
      <a href="https://github.com/python-pillow/Pillow/blob/master/src/libImaging/SgiRleDecode.c">SGI Image Decoder</a>
  </details>
- <details>
      <summary>Hint 3:</summary>
      You can use lengthtab data region.
  </details>

🙈 Solution below

👇

👇

👇

👇

👇

👇

## Solution

### Step 1. Just RLE

As we can find in [the SGI Image Spec](https://www.fileformat.info/format/sgiimage/spec/2a67b5c53bd84e8aa1a18ab1a6d3e832/view.htm),
we can use run-length encoding in a SGI Image.
By encoding the image with RLE enabled, we can obtain the image within 6300bytes.

### Step 2. Shared data region

The spec says:

> It is possible for two identical rows to share compressed scanline data.
> A completely white image could be written as a single compressed scanrow and having all table entries point to that scanrow.
> Another little hack that should work is if you are writing out a RGB RLE file,
> and a particular scan line is achromatic (greyscale), you could just make the r, g and b rows point to the same data!!

In the image, there are some common data sequences.
![](https://i.imgur.com/3w8LMzj.png)

By sharing these data sequence we can reduce $\frac 16$ of the RLE data size.

### Step 3.　 Abuse Buffer

Surprisingly, we don't have to store data for these regions:
![](https://i.imgur.com/mRMHCvI.png)

Look at the [SGIImageDecoder](https://github.com/python-pillow/Pillow/blob/master/src/libImaging/SgiRleDecode.c#L250).
They are using the same buffer again and again, without clearing it.
So, if your image does not contain enough information for a row, the remaining is kept untouched and there is a ghost data written in that part.
The ghost data contains a previous row's data, so you can "copy-paste" previous row's information.

Therefore, by not having data for the region the decoder automatically copy data from one row down.

### Step 4. R.I.P. tablen

If you look closely at the decoder, you will find [a behavior that aborts the line expansion at that stage
if there is a byte in the RLE data that implies zero repetition](https://github.com/python-pillow/Pillow/blob/master/src/libImaging/SgiRleDecode.c#L85) (`0x00` or `0x80`).
Then, why do we need `tablen` region?

By putting our rows in `tablen` region, we can save about 1500 bytes.
Note that we need to keep each length positive number, so that the decoder read a few data we need.
Thankfully, we can modify our data arrangement to avoid negative numbers. You may also insert some padding bytes.

### (Optional) Step 5. Data as a Instruction, Instruction as a Data

Did you notice you can represent these data region within only 200 bytes?
![](https://i.imgur.com/3w8LMzj.png)

`0xFF` means "copy next 127 bytes to buffer" if interpreted as an instruction, and "white pixel" if interpreted as data.
So, by placing data like below you can represent all these lines.

```
 64* 0xFF
  1* 0x7F
128* 0x00
```
