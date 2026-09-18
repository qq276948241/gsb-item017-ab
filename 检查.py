# -*- coding: utf-8 -*-
import subprocess
import sys
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
tool = here / "看闸.py"

cases = [
    ("正常进出", "进 甲\n进 乙\n出 乙\n出 甲\n", 0, "闸机正常\n", ""),
    ("没进就出", "出 甲\n", 0, "闸机异常\n", ""),
    ("重复进", "进 甲\n进 甲\n", 0, "闸机异常\n", ""),
    ("走完还有人没出", "进 甲\n进 乙\n出 甲\n", 0, "闸机异常\n", ""),
    ("找不到进出", None, 1, "", "找不到进出\n"),
    ("空文件", "", 1, "", "进出不对\n"),
    ("行对不上样子", "进 甲\n出去 乙\n", 1, "", "进出不对\n"),
    ("人名是空的", "进 \n", 1, "", "进出不对\n"),
]

passed = 0
failed = 0


def run_case(title, content, want_code, want_out, want_err, cwd):
    global passed, failed
    if content is not None:
        (Path(cwd) / "进出").write_text(content, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(tool)],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    got_code = 0 if result.returncode == 0 else 1
    ok = (
        got_code == want_code
        and result.stdout == want_out
        and result.stderr == want_err
    )
    if ok:
        passed += 1
    else:
        failed += 1
        sys.stdout.write(
            "没过:%s 退出码=%r 标准输出=%r 错误输出=%r\n"
            % (title, result.returncode, result.stdout, result.stderr)
        )


for title, content, want_code, want_out, want_err in cases:
    with tempfile.TemporaryDirectory() as tmp:
        run_case(title, content, want_code, want_out, want_err, tmp)

run_case("原来目录的进出", None, 0, "闸机正常\n", "", str(here))

(here / "对照结果").write_text(
    "过了 %d 条\n没过 %d 条\n" % (passed, failed), encoding="utf-8"
)

if failed:
    sys.exit(1)
sys.exit(0)
