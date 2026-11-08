#!/usr/bin/env python3
"""從講義 notes/graph-theory.md 匯入一題到 judge/problems/<題號>/。

會建立：problem.json、statement.md、samples/1.in、samples/1.out、ref.cpp
（ref.cpp 就是講義解答裡的程式碼，一字不改）。gen.py、brute.py 要另外寫。

用法：python3 -I judge/tools/import_from_notes.py 3-1     （實作題 3-1）
      python3 -I judge/tools/import_from_notes.py 3A      （範例 3-A）
已存在的 gen.py、brute.py、checker.py 不會被覆蓋。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NOTES = os.path.join(REPO, "notes", "graph-theory.md")       # 講義檔
CN = "一二三四五六七八"


def block_after(text, start):
    """從 start 開始，回傳到下一個同級或更高級標題為止的文字"""
    level = len(re.match(r"#+", text[start:]).group(0))
    nxt = re.compile(r"^#{1,%d} " % level, re.M).search(text, start + 1)
    return text[start: nxt.start() if nxt else len(text)]


def parse_sample(section):
    """從題目段落的 ```text 區塊取出範例輸入與輸出"""
    m = re.search(r"```text\n(.*?)\n```", section, re.S)
    if not m or "範例輸出" not in m.group(1):
        sys.exit("找不到範例輸入／輸出")
    a, b = m.group(1).split("範例輸出", 1)
    inp = a.replace("範例輸入", "", 1).strip("\n") + "\n"
    out = b.strip("\n") + "\n"
    return inp, out


def main(pid):
    text = open(NOTES, encoding="utf-8").read()
    if re.fullmatch(r"[1-8][AB]", pid):                       # 範例題，例如 3A
        ch, letter = pid[0], pid[1]
        m = re.search(rf"^### 範例 {ch}-{letter} (.+)$", text, re.M)
        if not m:
            sys.exit(f"講義裡找不到 範例 {ch}-{letter}")
        heading = m.group(1).strip()
        section = block_after(text, m.start())
        title, level = re.match(r"(.+?)（(.+)）$", heading).groups()
        level = level.split("，")[-1]
        stmt = section.split("**解答**")[0].rstrip()
        code_src = section
        source = f"第{CN[int(ch) - 1]}章 範例 {ch}-{letter}"
    elif re.fullmatch(r"[1-8]-[1-3]", pid):                   # 實作題，例如 3-1
        ch = int(pid[0])
        p = re.search(rf"^### 第{CN[ch - 1]}章 實作題\s*$", text, re.M)
        s = re.search(rf"^### 第{CN[ch - 1]}章 實作題詳解\s*$", text, re.M)
        if not p or not s:
            sys.exit(f"講義裡找不到第{CN[ch - 1]}章的實作題")
        probs = block_after(text, p.start())
        sols = block_after(text, s.start())
        m = re.search(rf"^#### 實作 {pid} (.+)$", probs, re.M)
        heading = m.group(1).strip()
        stmt = block_after(probs, m.start()).rstrip()
        title, level = re.match(r"(.+?)（(.+)）$", heading).groups()
        sm = re.search(rf"^#### 實作 {pid} ", sols, re.M)
        code_src = block_after(sols, sm.start())
        source = f"第{CN[ch - 1]}章 實作 {pid}"
    else:
        sys.exit("題號格式：範例用 3A、3B，實作題用 3-1、3-2、3-3")

    code = re.search(r"```cpp\n(.*?)\n```", code_src, re.S)
    if not code:
        sys.exit("找不到解答程式碼")
    d = os.path.join(REPO, "judge", "problems", pid)
    os.makedirs(os.path.join(d, "samples"), exist_ok=True)
    first_line, rest = stmt.split("\n", 1)
    with open(os.path.join(d, "statement.md"), "w", encoding="utf-8") as f:
        f.write(f"# {pid} {title}（{level}）\n\n出處：講義{source}\n" + rest.rstrip() + "\n")
    with open(os.path.join(d, "ref.cpp"), "w", encoding="utf-8") as f:
        f.write(code.group(1) + "\n")
    inp, out = parse_sample(stmt)
    with open(os.path.join(d, "samples", "1.in"), "w", encoding="utf-8") as f:
        f.write(inp)
    with open(os.path.join(d, "samples", "1.out"), "w", encoding="utf-8") as f:
        f.write(out)
    pj = os.path.join(d, "problem.json")
    conf = json.load(open(pj, encoding="utf-8")) if os.path.exists(pj) else {}
    conf.update({"id": pid, "title": title, "level": level, "source": source})
    conf.setdefault("time_limit", 1.0)
    conf.setdefault("memory_mb", 256)
    conf.setdefault("checker", None)
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(conf, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"已匯入 {pid} {title}（{level}）→ {d}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
