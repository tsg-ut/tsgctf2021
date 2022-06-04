from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import string
from typing import List, final

import numpy as np
import torch
from torch import nn
np.random.seed(0)

FLAG_CHARS = string.ascii_letters + string.digits + "{}-"
CHARS = "^$" + FLAG_CHARS
def sanity_check(text):
    assert text[:7] == "TSGCTF{"
    assert text[-1:] == "}"
    assert all([t in FLAG_CHARS for t in text])

# generate
flag = Path("./flag.txt").read_text()
POSITIVE = 0.999
LOGIT = np.arctanh(POSITIVE)
SCALE = LOGIT * 2.0
BIAS = -SCALE * 1.5

sanity_check(flag)

@dataclass
class Delta:
    state: int
    char: str
    next_state: int

def Counter():
    i = 0
    while True:
        yield i
        i += 1

def dump_pu(rules: List[Delta], init_state: int, final_state: int, perm: np.ndarray) -> str:
    out = "@startuml automaton\ndigraph automaton {\n"
    out += 'rankdir="LR"\n'
    out += f'{perm[init_state]} [label="init" fillcolor="yellow" style="filled"]\n'

    good_states = list(range(init_state, final_state+1))
    for i in good_states[1:-1]:
        out += f'{perm[i]} [fillcolor="yellow" style="filled"]\n'
    out += f'{perm[final_state]} [label="accept ({perm[final_state]})" fillcolor="yellow" style="filled"]\n'
    for delta in rules:
        if delta.state in good_states and delta.next_state in good_states:
            out += f'{perm[delta.state]} -> {perm[delta.next_state]} [label="{delta.char}" color="red" fontcolor="red"]\n'
        else:
            out += f'{perm[delta.state]} -> {perm[delta.next_state]} [label="{delta.char}"]\n'

    out += "{rank = same; "
    for i in good_states:
        out += f"{perm[i]} "
    out += "}\n"

    out += "}\n@enduml"
    return out

counter = Counter()
rules: List[Delta] = []
assigned = defaultdict(list)

s = next(counter)
for f in ("^" + flag + "$"):
    sn = next(counter)
    rules.append(Delta(s, f, sn))
    assigned[s].append(f)
    s = sn
final_state = s

def dummy1(state):
    global counter
    global assigned
    siz = np.random.randint(1, 5)
    orig: str = assigned[state][0]
    if orig in string.ascii_lowercase:
        chars = [orig.upper()]
    elif orig in string.ascii_uppercase:
        chars = [orig.lower()]
    else:
        return
    chars += [assigned[s][0] for s in range(state+1, state+1+siz)]
    new_states = []
    s = state
    for c in chars:
        sn = next(counter)
        rules.append(Delta(s, c, sn))
        assigned[s].append(c)
        new_states.append(sn)
        s = sn
    assert len(chars) == siz+1
    assert len(new_states) == siz+1
    if np.random.rand() < 0.5:
        # make loop
        back = np.random.randint(1, siz+1)
        rules.append(Delta(s, chars[back], new_states[back]))
        assigned[s].append(chars[back])
    else:
        # fake eos
        for c in "}$":
            sn = next(counter)
            rules.append(Delta(s, c, sn))
            assigned[s].append(c)
            new_states.append(sn)
            s = sn

def dummy2(state):
    global counter
    global assigned
    siz = np.random.randint(1, 5)
    chars = [np.random.choice(sorted(set(FLAG_CHARS) - set(assigned[state])), replace=False, size=np.random.randint(1, 3))]
    chars += [np.random.choice(sorted(FLAG_CHARS), replace=False, size=np.random.randint(1, 5)) for _ in range(siz)]
    new_states = []
    s = state
    for cs in chars:
        sn = next(counter)
        for c in cs:
            rules.append(Delta(s, c, sn))
            assigned[s].append(c)
        new_states.append(sn)
        s = sn
    assert len(chars) == siz+1
    assert len(new_states) == siz+1
    if np.random.rand() < 0.5:
        # make loop
        back = np.random.randint(1, siz+1)
        for c in chars[back]:
            rules.append(Delta(s, c, new_states[back]))
            assigned[s].append(c)

for i in range(1, final_state-6):
    if np.random.rand() < 0.5:
        dummy1(i)

for _ in range(3):
    for i in range(1, final_state-1):
        if np.random.rand() < 0.5:
            dummy2(i)
# print(assigned)

n_states = next(counter)
print("len of flag:", len(flag))
print("# of states:", n_states)
print("# of chars:", len(CHARS))

# shuffle state number
perm = np.random.permutation(n_states)
Path("./automaton.pu").write_text(dump_pu(rules, 0, final_state, perm))

Wh = torch.zeros((n_states, n_states))
Wx = torch.zeros((n_states, len(CHARS)))
for delta in rules:
    ns = perm[delta.next_state]
    s = perm[delta.state]
    Wh[ns, s] = 0 if delta.state == 0 else SCALE
    Wx[ns, CHARS.index(delta.char)] = (SCALE * 2) if delta.state == 0 else SCALE
print(np.where(Wx.numpy() == 2 * SCALE), CHARS.index("^"))
print("final state:", perm[final_state])

# create model
def embedding(text):
    global CHARS
    x = torch.zeros((len(text), len(CHARS)))
    for i, t in enumerate(text):
        x[i, CHARS.index(t)] = 1.0
    return x

class Model(nn.Module):
    def __init__(self, inpt, hidden):
        super().__init__()
        self.cell = nn.RNNCell(inpt, hidden)
        self.out = nn.Linear(hidden, 1)
    def forward(self, xs):
        h = None
        for x in xs:
            h = self.cell(x, h)
        return self.out(h)

def inference(model, text):
    model.eval()
    with torch.no_grad():
        x = embedding("^" + text + "$").unsqueeze(1)
        y = model(x)[0].sigmoid().cpu().item()
    print(text, y)

model = Model(len(CHARS), n_states)
model.cell.weight_hh.data[:,:] = Wh
model.cell.weight_ih.data[:,:] = Wx
model.cell.bias_hh.data[:] = -12.0 # Oops, this should've been BIAS but no problem.
model.cell.bias_ih.data[:] = 0
model.out.weight.data[:,:] = 0
model.out.weight.data[0,perm[final_state]] = 1.0
model.out.bias.data[:] = 0

torch.save(model.state_dict(), "../dist/model_final.pth")
print("model saved.")

inference(model, "TSGCTF{HOGEHOGE}")
inference(model, "INVALIDCTF{}")
inference(model, flag[:-1])
inference(model, flag+"}")
inference(model, "T"+flag)
inference(model, "8"+flag)
inference(model, flag[:-7] + "OM4toN}")
inference(model, flag)