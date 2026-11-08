"""範例 6-A 的暴力解：每次拿掉一條道路，用並查集重算連通塊數；變多了就是關鍵道路。"""
import sys


def components(n, edges, skip):
    """拿掉第 skip 條道路（從 0 起算）後的連通塊數"""
    par = list(range(n + 1))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    cnt = n
    for k, (u, v) in enumerate(edges):
        if k == skip:
            continue
        a, b = find(u), find(v)
        if a != b:
            par[a] = b
            cnt -= 1
    return cnt


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
    base = components(n, edges, -1)              # 原本的連通塊數
    ans = [k + 1 for k in range(m) if components(n, edges, k) > base]
    print(len(ans))
    if ans:
        print(" ".join(map(str, ans)))


main()
