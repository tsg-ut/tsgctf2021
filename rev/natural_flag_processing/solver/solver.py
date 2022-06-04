from pathlib import Path
import string

import torch
from torch import nn

FLAG_CHARS = string.ascii_letters + string.digits + "{}-"
CHARS = "^$" + FLAG_CHARS
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

model = Model(len(CHARS), 520)
model.load_state_dict(torch.load("../dist/model_final.pth"))
Wh = model.cell.weight_hh
Wi = model.cell.weight_ih
bias = model.cell.bias_ih + model.cell.bias_hh

state = model.out.weight.data[0,:].argmax()
answer = ""
while True:
    prev_state = Wh[state, :].argmax()
    answer += CHARS[Wi[state, :].argmax()]
    print(answer[::-1])
    if Wh[state, prev_state] == 0:
        break
    state = prev_state

print("FLAG:", answer[-2:0:-1])
assert answer[-2:0:-1] == Path("../src/flag.txt").read_text()
