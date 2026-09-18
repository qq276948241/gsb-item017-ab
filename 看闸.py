# -*- coding: utf-8 -*-
import sys
from pathlib import Path

path = Path("进出")
if not path.is_file():
    sys.stderr.write("找不到进出\n")
    sys.exit(1)
raw = path.read_bytes()
if len(raw) == 0:
    sys.stderr.write("进出不对\n")
    sys.exit(1)
text = raw.decode("utf-8")
lines = text.split("\n")
if lines[-1] == "":
    lines.pop()
if not lines:
    sys.stderr.write("进出不对\n")
    sys.exit(1)
inside = set()
for line in lines:
    parts = line.split(" ")
    if len(parts) != 2 or parts[0] not in ("进", "出") or parts[1] == "":
        sys.stderr.write("进出不对\n")
        sys.exit(1)
    name = parts[1]
    if parts[0] == "进":
        if name in inside:
            sys.stdout.write("闸机异常\n")
            sys.exit(0)
        inside.add(name)
    else:
        if name not in inside:
            sys.stdout.write("闸机异常\n")
            sys.exit(0)
        inside.remove(name)
if inside:
    sys.stdout.write("闸机异常\n")
else:
    sys.stdout.write("闸机正常\n")
