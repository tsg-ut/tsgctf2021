import soundfile as sf
import numpy as np
from utils import signals_to_string, string_to_signals

EPSILON = 1e-6

frames, _ = sf.read('../dist/result.wav')
mapping = {}
for i in range(2205):
  wave = np.sin(i * 440 / 44100 * (2 * np.pi))
  mapping[wave] = i
counts = [0] * 2205
cache = {}
for i, frame in enumerate(frames):
  if frame == 0:
    continue
  if frame in cache:
    n = cache[frame]
  else:
    n = None
    for wave in mapping.keys():
      if np.abs(frame - wave) < EPSILON:
        n = mapping[wave]
        cache[frame] = n
        break
  counts[n] += 1

shrink_counts = []
for i in range(1, 2205, 5):
  shrink_counts.append(counts[i])

count_diffs = []
for i in range(len(shrink_counts)):
  count_diffs.append(shrink_counts[i] - shrink_counts[i - 1])

reordered_diffs = []
for i in range(len(count_diffs)):
  reordered_diffs.append(count_diffs[i * 400 % len(count_diffs)])

leading_signals = [0] + string_to_signals('TSGCTF{') + [0]
for i in range(len(leading_signals) - 1):
  reordered_diffs[i] -= leading_signals[i + 1] - leading_signals[i]

value = 1
signals = []
for i in range(len(leading_signals) + 2, 474):
  diff = reordered_diffs[i % len(reordered_diffs)]
  signals.append(value)
  value += diff

print('TSGCTF{' + signals_to_string(signals))
