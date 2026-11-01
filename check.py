"""判分：6 个问题，期望答案固定，比较三条路的输出。"""
import subprocess, sys

EXPECTED = {
    "C4日期": "2025-07-15",
    "D4格式": "$#,##0.00",
    "B1的值": "空",
    "汇总B3日期": "2025-09-30",
    "D9公式": "=SUM(D4:D8)",
    "合并区": "5",
}

def norm(label, text):
    t = text.strip()
    if label == "B1的值":
        return "空" if ("空" in t or t == "") else t
    if label == "合并区":
        return "5" if "5" in t else ("1" if "1" in t and "5" not in t else t)
    return t

for script in ("a_manual.py", "b_manual.py", "c_openpyxl.py"):
    r = subprocess.run([sys.executable, script, "sales.xlsx"],
                       capture_output=True, text=True)
    print(f"===== {script} ({len(open(script).readlines())} 行) =====")
    if r.returncode:
        print("CRASH:", r.stderr.strip()[-300:]); continue
    ok = 0
    for line in r.stdout.strip().splitlines():
        label, _, ans = line.partition(":")
        want = EXPECTED[label.strip()]
        got = norm(label.strip(), ans)
        mark = "OK " if got == want else "MISS"
        ok += got == want
        print(f"{mark} {line.strip()}    (期望 {want})")
    print(f"--> {ok}/6\n")
