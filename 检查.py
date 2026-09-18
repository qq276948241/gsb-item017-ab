# -*- coding: utf-8 -*-
import sys
import tempfile
import subprocess
from pathlib import Path

here = Path(__file__).resolve().parent
tool = here / "看闸.py"

cases = [
    ("正常进出", "进 甲\n进 乙\n出 乙\n出 甲\n", "闸机正常\n", "", True),
    ("没进就出", "出 甲\n", "闸机异常\n", "", True),
    ("重复进门", "进 甲\n进 甲\n", "闸机异常\n", "", True),
    ("有人没出", "进 甲\n", "闸机异常\n", "", True),
    ("动作不对", "逛 甲\n", "", "进出不对\n", False),
    ("字段多了", "进 甲 乙\n", "", "进出不对\n", False),
    ("名字空的", "进 \n", "", "进出不对\n", False),
    ("空文件", "", "", "进出不对\n", False),
    ("没有文件", None, "", "找不到进出\n", False),
]

passed = 0
failed = 0


def check(name, cwd, stdout, stderr, zero_exit, create=False, content=""):
    global passed, failed
    path = Path(cwd) / "进出"
    if create:
        path.write_bytes(content.encode("utf-8"))
    r = subprocess.run(
        [sys.executable, str(tool)],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ok = (
        r.stdout == stdout.encode("utf-8")
        and r.stderr == stderr.encode("utf-8")
        and (r.returncode == 0) == zero_exit
    )
    if ok:
        passed += 1
        sys.stdout.write("过了：" + name + "\n")
    else:
        failed += 1
        sys.stdout.write(
            "没过：" + name
            + " 退出=" + str(r.returncode)
            + " 标准输出=" + repr(r.stdout)
            + " 错误输出=" + repr(r.stderr) + "\n"
        )


for name, content, stdout, stderr, zero_exit in cases:
    with tempfile.TemporaryDirectory() as d:
        check(
            name, d, stdout, stderr, zero_exit,
            content is not None, content or "",
        )

check("原来目录的进出", here, "闸机正常\n", "", True)

Path("对照结果").write_text(
    "过了 " + str(passed) + " 条\n没过 " + str(failed) + " 条\n",
    encoding="utf-8",
)

if failed:
    sys.exit(1)
