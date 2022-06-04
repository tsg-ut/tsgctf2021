# TSGCTF3 Kotlin Lovers Society
# SGI Image Specification
# https://www.fileformat.info/format/sgiimage/spec/2a67b5c53bd84e8aa1a18ab1a6d3e832/view.htm

import struct
from PIL import Image
import numpy as np
import os
from optimizer import DataSegment, optimize_data_segments, align_data_segments

SIZE = 127

def get_header(filename):
  name = filename.encode('ascii')
  desc = b'TSGCTF3 Kotlin Lovers Society: This is a problem of SGI rather than Kotlin.'

  header = b''
  header += struct.pack(">h", 474)    # MAGIC
  header += struct.pack("B", 1)       # STORAGE: RLE enabled
  header += struct.pack("B", 1)       # BPC: 1byte per pixel
  header += struct.pack(">H", 3)      # DIMENSION: 2D RGB Image
  header += struct.pack(">H", SIZE)   # XSIZE: 127px width
  header += struct.pack(">H", SIZE)   # XSIZE: 127px height
  header += struct.pack(">H", 3)      # ZSIZE: RGB
  header += struct.pack(">l", 0)      # PIXMIN: Pixel value is 0 or greater
  header += struct.pack(">l", 255)    # PIXMAX: Pixel value is 255 or lesser
  header += struct.pack("4s", b"")    # DUMMY
  header += struct.pack("80s", name)  # NAME: Name of the image
  header += struct.pack(">l", 0)      # COLORMAP: No colormap
  header += struct.pack("404s", desc) # DUMMY

  assert len(header) == 512
  return header

def get_body():
  offset = [[None] * SIZE for _ in range(3)]
  ds_10 = DataSegment().raw((b'\xFF' * 64) + b'\x7F' + (b'\x00' * 128))
  segments = []

  # Channel: R
  for i in range(63):
    ds = DataSegment().rep(0, 63 - i).rep(0xFF, 63).rep(0x7F, 1).zero()
    offset[0][i] = (ds, 0)
    segments.append(ds)
  for i in range(63, SIZE):
    offset[0][i] = (ds_10, i - 63)

  # Channel: G
  for i in range(64):
    b2 = max(127 - i, i)
    ds = DataSegment().rep(i + 1, b2).zero()
    offset[1][i] = (ds, 0)
    segments.append(ds)
  for i in range(64, SIZE):
    b2 = max(127 - i, i)
    ds = DataSegment().rep(i + 1, b2)
    if i != SIZE - 1:
      ds.rep(0, SIZE - b2) # clean buffer
    ds.zero()
    offset[1][i] = (ds, 0)
    segments.append(ds)

  # Channel: B
  for i in range(63):
    offset[2][i] = (ds_10, i + 1)
  ds = DataSegment().rep(0, SIZE).zero()
  offset[2][63] = (ds, 0)
  segments.append(ds)
  for i in range(64, SIZE):
    ds = DataSegment().rep(0, 127 - i)
    if i != 64:
      ds.rep(0xFF, 2 * (i - 64))
    ds.rep(0x7F, 1).rep(0, 127 - i).zero()
    offset[2][i] = (ds, 0)
    segments.append(ds)

  # optimize segments
  offlen = 512 + SIZE * 4 * 3
  segments = optimize_data_segments(segments)
  segments.append(ds_10)
  segments = align_data_segments(segments, base=offlen)

  body = bytearray()
  for c in range(3):
    for l in range(SIZE):
      ds, off = offset[c][SIZE - l - 1]
      body += struct.pack(">l", ds.offset + off)
  for segment in segments:
    body += segment.data
  print("Body", len(body))
  print("Meta", SIZE * 4 * 3 * 2)
  print("Diff", len(body) - SIZE * 4 * 3 * 2)
  return bytes(body)

def main():
  # Generate an image
  name = 'kls_symbol'

  with open(f'{name}.rgb', 'wb') as f:
    f.write(get_header(f'{name}.rgb'))
    f.write(get_body())

  # Convert it into other format
  image = Image.open(f'{name}.rgb')
  image.save(f'{name}_plain.rgb')

  # Debug
  r, g, b = image.split()
  r.save(f'{name}_r.png')
  g.save(f'{name}_g.png')
  b.save(f'{name}_b.png')

  # Identitiy Check
  ref = np.array(Image.open(f'{name}.png'))
  got = np.array(Image.open(f'{name}.rgb', formats=['SGI']))
  assert np.array_equal(ref, got)

  # Show filesize
  for file in [f'{name}.rgb', f'{name}_plain.rgb', f'{name}.png', ]:
    print(file, os.path.getsize(file))
  return image


if __name__ == '__main__':
  image = main()
