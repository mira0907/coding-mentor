"""編譯並執行 notes/syntax/*.md 裡的每個範例，檢查「輸出」區塊是否正確。

用法：python3 -I notes/syntax/check.py
每個 ```cpp 區塊後面接著的 ```text 區塊就是它的預期輸出。
"""
import pathlib, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent          # notes/syntax 資料夾
INCLUDE = HERE.parent.parent / "include"                # macOS 用的 bits/stdc++.h
PAIR = re.compile(r"```cpp\n(.*?)```\s*\n輸出：\s*\n```text\n(.*?)```", re.S)

failed = 0                                              # 失敗的範例數
total = 0                                               # 範例總數
with tempfile.TemporaryDirectory() as tmp:
    for md in sorted(HERE.glob("*.md")):
        if md.name.startswith("_"):
            continue
        for body, expect in PAIR.findall(md.read_text(encoding="utf-8")):
            total += 1
            src = pathlib.Path(tmp, "t.cpp")
            exe = pathlib.Path(tmp, "t")
            src.write_text("#include <bits/stdc++.h>\nusing namespace std;\nint main() {\n"
                           + body + "\nreturn 0;\n}\n", encoding="utf-8")
            r = subprocess.run(["clang++", "-std=c++17", "-Wall", "-Wextra", "-Wshadow",
                                "-I", str(INCLUDE), str(src), "-o", str(exe)],
                               capture_output=True, text=True)
            head = body.strip().splitlines()[0]
            if r.returncode != 0 or r.stderr.strip():
                failed += 1
                print(f"[編譯] {md.name}: {head}\n{r.stderr}")
                continue
            out = subprocess.run([str(exe)], capture_output=True, text=True).stdout
            if out != expect:
                failed += 1
                print(f"[輸出不符] {md.name}: {head}\n預期:\n{expect}實際:\n{out}")
print(f"{total - failed} / {total} 個範例正確")
sys.exit(1 if failed else 0)
