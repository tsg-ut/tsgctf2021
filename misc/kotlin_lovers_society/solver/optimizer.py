import struct
import random

class DataSegment():
  def __init__(self):
    self.data = b''
    self.offset = None
  
  def raw(self, data):
    self.data += data
    return self

  def rep(self, color, times):
    self.data += struct.pack("BB", times, color)
    return self

  def zero(self):
    self.data += b'\x00'
    return self

  def _msbp4(self):
    msbp4 = [False] * 4
    for i, v in enumerate(self.data):
      msbp4[(4 - i)  % 4] |= bool(v >> 7)
    return msbp4

def optimize_data_segments(segments):
  nop = DataSegment().raw(b'\x7F')
  sat, unsat = [], []

  qs = [[] for _ in range(4)]
  used = set()
  for segment in segments:
    msbp4 = segment._msbp4()
    if all(msbp4):
      unsat.append(segment)
      continue
    for i in range(4):
      if not msbp4[i]:
        qs[i].append(segment)

  for q in qs:
    random.shuffle(q)
  
  off = 0
  for _ in range(len(segments) - len(unsat)):
    segment = None
    while segment is None:
      while len(qs[off % 4]):
        seg = qs[off % 4].pop()
        if seg not in used:
          segment = seg
          break
      else:
        off += 1
        sat.append(nop)
    sat.append(segment)
    used.add(segment)
    off += len(segment.data)
  return sat + unsat

def align_data_segments(segments, base=0):
  offset = base
  for segment in segments:
    segment.offset = offset
    offset += len(segment.data)
  return segments
