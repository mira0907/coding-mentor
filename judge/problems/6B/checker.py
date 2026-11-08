"""範例 6-B 的檢查程式：python3 -I checker.py <輸入> <參考答案> <你的輸出>
參考答案是 IMPOSSIBLE 時，你也要輸出 IMPOSSIBLE；
參考答案有解時，你的輸出要是長度 n 的 01 字串，而且滿足每一個條件（不必和參考答案相同）。
正確時結束碼為 0，錯誤時印出原因、結束碼為 1。"""
import sys


def fail(msg):
    """印出錯誤原因並以結束碼 1 離開"""
    print(msg)
    sys.exit(1)


def main():
    inp, ans, out = sys.argv[1:4]
    with open(inp, "rb") as f:
        data = f.read().split()
    with open(ans, "rb") as f:
        ref = f.read().split()
    with open(out, "rb") as f:
        user = f.read().split()
    n, m = int(data[0]), int(data[1])
    ref_impossible = ref == [b"IMPOSSIBLE"]       # 參考解判定無解
    if not user:
        fail("沒有輸出")
    if len(user) > 1:
        fail(f"輸出太多：應該只有一個字串，你輸出了 {len(user)} 個")
    s = user[0]
    if s == b"IMPOSSIBLE":                        # 你說無解：要和參考解一致
        if ref_impossible:
            sys.exit(0)
        fail("這筆有解，你卻輸出 IMPOSSIBLE")
    # 檢查格式：長度 n、只有 0 和 1
    if len(s) != n or s.strip(b"01"):
        if ref_impossible:
            fail("這筆無解，應該輸出 IMPOSSIBLE")
        fail(f"格式錯誤：應該是長度 {n} 的 01 字串")
    # 逐條檢查條件 i a j b：開關 i 為 a 或開關 j 為 b
    for k in range(m):
        i, a, j, b = (int(t) for t in data[2 + 4 * k: 6 + 4 * k])
        if s[i - 1] - 48 != a and s[j - 1] - 48 != b:
            if ref_impossible:
                fail("這筆無解，應該輸出 IMPOSSIBLE")
            fail(f"第 {k + 1} 個條件「{i} {a} {j} {b}」不成立")
    if ref_impossible:                            # 理論上不會發生：參考解說無解，你的設定卻全部滿足
        fail("參考解判定無解，但你的設定滿足所有條件（題目可能有誤，請回報）")
    sys.exit(0)


main()
