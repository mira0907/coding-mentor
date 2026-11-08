#!/usr/bin/env python3
"""講義題目的本機評測系統（judge）。

用法（在專案根目錄執行）：
    python3 judge/judge.py list                 列出所有題目與你的最佳結果
    python3 judge/judge.py show 3-2             顯示題目敘述
    python3 judge/judge.py 3-2 my.cpp           評測你的程式
    python3 judge/judge.py 3-2 my.cpp --debug   用 sanitizer 編譯，抓越界與未定義行為
    python3 judge/judge.py build 3-2|all        重新產生測資（通常不用手動執行）
    python3 judge/judge.py test 3-2|all         用參考解自我檢查（維護題目時用）

題目資料夾格式見 judge/README.md。
"""
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))          # judge/ 資料夾
REPO = os.path.dirname(ROOT)                                # 專案根目錄
PROBLEMS = os.path.join(ROOT, "problems")                   # 每題一個子資料夾
CACHE = os.path.join(ROOT, ".cache")                        # 測資與編譯產物，不進 git
RESULTS = os.path.join(ROOT, ".results.json")               # 每題你的最佳結果，不進 git
CXX = ["clang++", "-std=c++17", "-O2", "-Wall", "-I" + os.path.join(REPO, "include")]
DEBUG_FLAGS = ["-g", "-O1", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
SIZES = ("small", "mid", "max")                             # 測資規模：小（可暴力驗證）、中、最大
DEFAULT_COUNTS = {"small": 15, "mid": 4, "max": 2}          # 每種規模預設產生幾筆
TL_FACTOR = 2.0                                             # 本機時限 = max(題目時限, 參考解最慢 × 2 + 0.1)
COLOR = sys.stdout.isatty()                                 # 終端機才上色

VERDICT_NAME = {
    "AC": "AC  通過",
    "WA": "WA  答案錯誤",
    "TLE": "TLE 超過時限",
    "MLE": "MLE 超過記憶體",
    "RE": "RE  執行錯誤",
    "CE": "CE  編譯錯誤",
}


def paint(text, code):
    """終端機時替文字上色；code 是 ANSI 顏色碼"""
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def verdict_text(v):
    return paint(VERDICT_NAME[v], "32" if v == "AC" else "31" if v in ("WA", "RE", "CE") else "33")


# ---------- 題目資料 ----------

def problem_dir(pid):
    return os.path.join(PROBLEMS, pid)


def load_problem(pid):
    """讀取題目設定；找不到時列出相近的題號並結束程式"""
    path = os.path.join(problem_dir(pid), "problem.json")
    if not os.path.exists(path):
        ids = all_ids()
        hint = [i for i in ids if i.startswith(pid[:1])]
        sys.exit(f"找不到題目 {pid}。可用的題號：{' '.join(hint or ids)}")
    with open(path, encoding="utf-8") as f:
        prob = json.load(f)
    prob.setdefault("time_limit", 1.0)
    prob.setdefault("memory_mb", 256)
    prob.setdefault("checker", None)
    counts = dict(DEFAULT_COUNTS)
    counts.update(prob.get("tests", {}))
    prob["tests"] = counts
    return prob


def sort_key(pid):
    """題號排序：章 → 範例（A、B）在前 → 實作題（-1、-2、-3）"""
    ch = int(pid[0]) if pid[:1].isdigit() else 99
    return (ch, 0 if pid[1:2].isalpha() else 1, pid)


def all_ids():
    if not os.path.isdir(PROBLEMS):
        return []
    ids = [d for d in os.listdir(PROBLEMS) if os.path.exists(os.path.join(PROBLEMS, d, "problem.json"))]
    return sorted(ids, key=sort_key)


def fingerprint(pid):
    """題目檔案的雜湊值；檔案改變時測資要重新產生"""
    h = hashlib.sha256()
    d = problem_dir(pid)
    for root, _, files in sorted(os.walk(d)):
        for name in sorted(files):
            p = os.path.join(root, name)
            h.update(os.path.relpath(p, d).encode())
            with open(p, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:16]


# ---------- 編譯與執行 ----------

def compile_cpp(src, out, debug=False):
    """編譯 src 成 out；回傳 (是否成功, 編譯器訊息)"""
    cmd = CXX + (DEBUG_FLAGS if debug else []) + [src, "-o", out]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode == 0, p.stderr


def raise_stack():
    """子程序的堆疊開到系統允許的最大值，接近一般評測系統的設定"""
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    target = hard if hard != resource.RLIM_INFINITY else 512 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_STACK, (target, hard))
    except (ValueError, OSError):
        pass


def run(cmd, inp, out, wall_limit):
    """執行 cmd，stdin 讀 inp、stdout 寫 out。
    回傳 dict：status（ok / tle / re）、cpu 秒數、mem_mb、detail（錯誤說明）"""
    with open(inp, "rb") as fi, open(out, "wb") as fo, tempfile.TemporaryFile() as fe:
        start = time.perf_counter()
        p = subprocess.Popen(cmd, stdin=fi, stdout=fo, stderr=fe, preexec_fn=raise_stack)
        killed = []                                         # 計時器砍掉程式時記一筆
        timer = threading.Timer(wall_limit, lambda: (killed.append(1), p.kill()))
        timer.start()
        _, status, usage = os.wait4(p.pid, 0)
        timer.cancel()
        p.returncode = 0                                    # 已經自己回收，避免 Popen 再等一次
        wall = time.perf_counter() - start
        cpu = usage.ru_utime + usage.ru_stime
        mem = usage.ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
        fe.seek(0)
        err = fe.read().decode("utf-8", "replace")
    res = {"cpu": cpu, "wall": wall, "mem_mb": mem, "detail": "", "stderr": err}
    if killed:
        res["status"] = "tle"
    elif os.WIFSIGNALED(status):
        sig = os.WTERMSIG(status)
        res["status"] = "re"
        res["detail"] = {11: "記憶體區段錯誤（SIGSEGV），常見原因：陣列越界、遞迴太深",
                         6: "程式中止（SIGABRT），常見原因：sanitizer 偵測到錯誤、assert 失敗",
                         8: "算術錯誤（SIGFPE），常見原因：除以 0",
                         10: "匯流排錯誤（SIGBUS）"}.get(sig, f"被訊號 {sig} 終止")
    elif os.WEXITSTATUS(status) != 0:
        res["status"] = "re"
        res["detail"] = f"main 回傳 {os.WEXITSTATUS(status)}，不是 0"
    else:
        res["status"] = "ok"
    return res


def tokens(path):
    with open(path, "rb") as f:
        return f.read().split()


def compare(prob, pid, inp, ans, out):
    """比較輸出；回傳 (是否正確, 說明)"""
    if prob["checker"]:
        checker = os.path.join(problem_dir(pid), prob["checker"])
        p = subprocess.run([sys.executable, "-I", checker, inp, ans, out], capture_output=True, text=True)
        return p.returncode == 0, p.stdout.strip()
    a, b = tokens(ans), tokens(out)
    if a == b:
        return True, ""
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return False, f"第 {i + 1} 個輸出值不同：期望 {x.decode(errors='replace')}，你輸出 {y.decode(errors='replace')}"
    if len(b) < len(a):
        return False, f"輸出太短：期望 {len(a)} 個值，你只輸出 {len(b)} 個"
    return False, f"輸出太長：期望 {len(a)} 個值，你輸出了 {len(b)} 個"


# ---------- 產生測資 ----------

def tests_dir(pid):
    return os.path.join(CACHE, "tests", pid)


def load_meta(pid):
    path = os.path.join(tests_dir(pid), "meta.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build(pid, verify=True, quiet=False):
    """產生題目 pid 的測資：範例 → 小 → 中 → 最大。小測資會用暴力解驗證參考解。"""
    prob = load_problem(pid)
    d = problem_dir(pid)
    td = tests_dir(pid)
    shutil.rmtree(td, ignore_errors=True)
    os.makedirs(td)
    ref_bin = os.path.join(CACHE, "bin", f"ref_{pid}")
    os.makedirs(os.path.dirname(ref_bin), exist_ok=True)
    ok, msg = compile_cpp(os.path.join(d, "ref.cpp"), ref_bin)
    if not ok:
        sys.exit(f"[{pid}] 參考解編譯失敗：\n{msg}")
    tests = []                                              # 每筆測資的名稱、種類、參考解時間
    sd = os.path.join(d, "samples")
    for name in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
        if name.endswith(".in"):
            k = len(tests) + 1
            shutil.copy(os.path.join(sd, name), os.path.join(td, f"{k:02d}.in"))
            shutil.copy(os.path.join(sd, name[:-3] + ".out"), os.path.join(td, f"{k:02d}.ans"))
            tests.append({"name": f"{k:02d}", "kind": "sample"})
    gen = os.path.join(d, "gen.py")
    brute = os.path.join(d, "brute.py")
    for size in SIZES:
        for seed in range(1, prob["tests"][size] + 1):
            k = len(tests) + 1
            inp = os.path.join(td, f"{k:02d}.in")
            with open(inp, "wb") as f:
                g = subprocess.run([sys.executable, "-I", gen, str(seed), size], stdout=f, stderr=subprocess.PIPE)
            if g.returncode != 0:
                sys.exit(f"[{pid}] 產生器在 seed={seed} size={size} 失敗：\n{g.stderr.decode()}")
            tests.append({"name": f"{k:02d}", "kind": size, "seed": seed})
    ref_max = 0.0
    for t in tests:
        inp = os.path.join(td, t["name"] + ".in")
        ans = os.path.join(td, t["name"] + ".ans")
        if t["kind"] == "sample":
            r = run([ref_bin], inp, os.path.join(td, "tmp.out"), 60)
            good, why = compare(prob, pid, inp, ans, os.path.join(td, "tmp.out"))
            if r["status"] != "ok" or not good:
                sys.exit(f"[{pid}] 參考解在範例 {t['name']} 答錯：{why}")
        else:
            r = run([ref_bin], inp, ans, 60)
            if r["status"] != "ok":
                sys.exit(f"[{pid}] 參考解在測資 {t['name']} 執行失敗：{r['detail']}")
            if verify and t["kind"] == "small" and os.path.exists(brute):
                bout = os.path.join(td, "brute.out")
                with open(inp, "rb") as fi, open(bout, "wb") as fo:
                    subprocess.run([sys.executable, "-I", brute], stdin=fi, stdout=fo, check=True)
                good, why = compare(prob, pid, inp, ans, bout)
                if not good:
                    sys.exit(f"[{pid}] 參考解與暴力解在測資 {t['name']} 不一致：{why}")
        t["ref_cpu"] = round(r["cpu"], 3)
        ref_max = max(ref_max, r["cpu"])
    for f in ("tmp.out", "brute.out"):
        if os.path.exists(os.path.join(td, f)):
            os.remove(os.path.join(td, f))
    meta = {"fingerprint": fingerprint(pid), "tests": tests, "ref_max_cpu": round(ref_max, 3)}
    with open(os.path.join(td, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    if not quiet:
        print(f"[{pid}] 產生 {len(tests)} 筆測資，參考解最慢 {ref_max:.2f} 秒")
    return meta


def ensure_built(pid):
    meta = load_meta(pid)
    if meta is None or meta["fingerprint"] != fingerprint(pid):
        print(f"第一次評測 {pid}（或題目有更新），先產生測資……")
        meta = build(pid)
    return meta


# ---------- 評測 ----------

def head(path, n=8, width=100):
    """檔案前 n 行，太長的行截斷"""
    out = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f):
            if i == n:
                out.append("……")
                break
            line = line.rstrip("\n")
            out.append(line if len(line) <= width else line[:width] + "……")
    return "\n".join("    " + l for l in out) or "    （空的）"


def judge(pid, src, debug=False, quiet=False, record=True):
    """評測 src；回傳整體結果（AC、WA、TLE、MLE、RE、CE）。record = 是否記進成績"""
    prob = load_problem(pid)
    meta = ensure_built(pid)
    tl = max(prob["time_limit"], meta["ref_max_cpu"] * TL_FACTOR + 0.1)
    if debug:
        tl *= 5
    if not quiet:
        print(f"題目 {pid} {prob['title']}（{prob.get('level', '')}）")
        print(f"時限：題目 {prob['time_limit']:.1f} 秒，本機放寬為 {tl:.2f} 秒；記憶體 {prob['memory_mb']} MB")
    exe = os.path.join(CACHE, "bin", f"sub_{pid}")
    os.makedirs(os.path.dirname(exe), exist_ok=True)
    ok, msg = compile_cpp(os.path.abspath(src), exe, debug)
    if not ok:
        print(verdict_text("CE"))
        print(msg[:3000])
        if record:
            save_result(pid, "CE", 0, len(meta["tests"]))
        return "CE"
    if msg.strip() and not quiet:
        print(paint("編譯警告（不影響評測，但常常是 bug 的線索）：", "33"))
        print("\n".join(msg.strip().splitlines()[:12]))
    td = tests_dir(pid)
    passed = 0
    first_fail = None
    worst = "AC"
    order = ["AC", "WA", "MLE", "TLE", "RE"]
    for t in meta["tests"]:
        inp = os.path.join(td, t["name"] + ".in")
        ans = os.path.join(td, t["name"] + ".ans")
        out = os.path.join(td, t["name"] + ".user")
        r = run([exe], inp, out, tl * 1.5 + 0.5)
        if r["status"] == "tle" or r["cpu"] > tl:
            v, why = "TLE", f"用了 {max(r['cpu'], r['wall']):.2f} 秒以上"
        elif r["status"] == "re":
            v, why = "RE", r["detail"]
        elif r["mem_mb"] > prob["memory_mb"]:
            v, why = "MLE", f"用了 {r['mem_mb']:.0f} MB"
        else:
            good, why = compare(prob, pid, inp, ans, out)
            v = "AC" if good else "WA"
        passed += v == "AC"
        if order.index(v) > order.index(worst):
            worst = v
        if v != "AC" and first_fail is None:
            first_fail = (t, v, why, inp, ans, out, r)
        if not quiet:
            kind = {"sample": "範例", "small": "小", "mid": "中", "max": "大"}[t["kind"]]
            print(f"  #{t['name']} {kind:<2} {verdict_text(v):<16} {r['cpu']:5.2f}s {r['mem_mb']:6.1f}MB  {why if v != 'AC' else ''}")
    total = len(meta["tests"])
    if not quiet:
        print()
        print(f"結果：{verdict_text(worst)}，通過 {passed} / {total} 筆")
        if first_fail:
            t, v, why, inp, ans, out, r = first_fail
            print(f"\n第一筆沒通過的是 #{t['name']}（{v}）：{why}")
            if os.path.getsize(inp) <= 4000:
                print("  輸入：")
                print(head(inp, 15))
                if v == "WA":
                    print("  期望輸出：")
                    print(head(ans))
                    print("  你的輸出：")
                    print(head(out))
            else:
                print(f"  這筆是大測資（{os.path.getsize(inp) // 1024} KB），完整輸入在 {inp}")
            if r["stderr"].strip():
                print("  你的程式寫到 stderr 的內容（前幾行）：")
                print("\n".join("    " + l for l in r["stderr"].strip().splitlines()[:10]))
            if v == "RE" and not debug:
                print("  提示：加上 --debug 重跑，sanitizer 會指出出錯的那一行。")
    if record:
        save_result(pid, worst, passed, total)
    return worst


def save_result(pid, verdict, passed, total):
    """記錄每題的最佳結果"""
    data = load_results()
    old = data.get(pid)
    if old is None or passed >= old.get("passed", 0):
        data[pid] = {"verdict": verdict, "passed": passed, "total": total,
                     "time": time.strftime("%Y-%m-%d %H:%M")}
        os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
        with open(RESULTS, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)


# ---------- 指令 ----------

def pad(text, width):
    """補空白到指定的顯示寬度（中文字佔兩格）"""
    w = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)
    return text + " " * max(1, width - w)


def load_results():
    """讀取成績檔；檔案不存在或損壞時當作還沒有成績"""
    try:
        with open(RESULTS, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def cmd_list():
    data = load_results()
    solved = 0
    print(pad("題號", 7) + pad("難度", 7) + pad("題目", 22) + pad("出處", 22) + "你的最佳結果")
    for pid in all_ids():
        prob = load_problem(pid)
        res = data.get(pid)                         # 這題的最佳紀錄，沒交過是 None
        mark = "" if res is None else (paint("AC", "32") if res["verdict"] == "AC"
                                       else f"{res['verdict']} {res['passed']}/{res['total']}")
        solved += bool(res and res["verdict"] == "AC")
        print(pad(pid, 7) + pad(prob.get("level", ""), 7) + pad(prob["title"], 22)
              + pad(prob.get("source", ""), 22) + mark)
    print(f"\n已通過 {solved} / {len(all_ids())} 題")


def cmd_show(pid):
    load_problem(pid)
    with open(os.path.join(problem_dir(pid), "statement.md"), encoding="utf-8") as f:
        print(f.read())


def cmd_selftest(target):
    ids = all_ids() if target == "all" else [target]
    bad = []
    for pid in ids:
        build(pid, verify=True, quiet=True)
        v = judge(pid, os.path.join(problem_dir(pid), "ref.cpp"), quiet=True, record=False)
        meta = load_meta(pid)
        print(f"{pid:<6} {verdict_text(v)}  {len(meta['tests'])} 筆測資，參考解最慢 {meta['ref_max_cpu']:.2f}s")
        if v != "AC":
            bad.append(pid)
    print("全部正常" if not bad else f"有問題的題目：{' '.join(bad)}")
    return not bad


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "list":
        cmd_list()
    elif cmd == "show" and len(argv) == 3:
        cmd_show(argv[2])
    elif cmd == "build" and len(argv) == 3:
        for pid in (all_ids() if argv[2] == "all" else [argv[2]]):
            build(pid)
    elif cmd == "test" and len(argv) == 3:
        return 0 if cmd_selftest(argv[2]) else 1
    elif len(argv) >= 3:
        pid, src = argv[1], argv[2]
        if not os.path.exists(src):
            sys.exit(f"找不到程式檔 {src}")
        debug = "--debug" in argv[3:]
        return 0 if judge(pid, src, debug) == "AC" else 1
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
