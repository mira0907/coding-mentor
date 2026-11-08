# 暴力解：對每個路口 x，拿掉 x 和它的道路後重算連通性，
# 看有沒有兩個「原本互通、現在不通」的其他路口。
import sys

def comps(n, edges, removed):
    # 回傳 label[v]：v 所在連通塊的代表（不含 removed）
    par = list(range(n + 1))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for u, v in edges:
        if u == removed or v == removed:
            continue
        a, b = find(u), find(v)
        if a != b:
            par[a] = b
    return [find(v) for v in range(n + 1)]

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
    base = comps(n, edges, 0)
    ans = []
    for x in range(1, n + 1):
        lab = comps(n, edges, x)
        others = [v for v in range(1, n + 1) if v != x]
        cut = False
        for i in range(len(others)):
            for j in range(i + 1, len(others)):
                a, b = others[i], others[j]
                if base[a] == base[b] and lab[a] != lab[b]:
                    cut = True
        if cut:
            ans.append(x)
    print(len(ans))
    if ans:
        print(" ".join(map(str, ans)))

main()
