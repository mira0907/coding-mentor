"""範例 4-A 的暴力解：列舉「哪些村莊蓋發電廠」和「架哪些電線」的所有組合，
檢查每個村莊都連得到發電廠，取最小總花費。只用在 n ≤ 6、m ≤ 8 的小測資。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    c = [int(x) for x in data[2:2 + n]]
    E = [(int(data[2 + n + 3 * i]), int(data[3 + n + 3 * i]), int(data[4 + n + 3 * i])) for i in range(m)]
    best = None
    for plants in range(1, 1 << n):              # plants 的第 i 位 = 村莊 i+1 是否蓋發電廠
        pc = sum(c[i] for i in range(n) if plants >> i & 1)
        for wires in range(1 << m):              # wires 的第 j 位 = 是否架第 j 條電線
            cost = pc + sum(E[j][2] for j in range(m) if wires >> j & 1)
            if best is not None and cost >= best:
                continue
            # 從所有發電廠出發，沿著選中的電線擴散，看能不能走遍全部村莊
            powered = [False] * (n + 1)
            stack = [i + 1 for i in range(n) if plants >> i & 1]
            for x in stack:
                powered[x] = True
            while stack:
                x = stack.pop()
                for j in range(m):
                    if wires >> j & 1:
                        u, v, _ = E[j]
                        for a, b in ((u, v), (v, u)):
                            if a == x and not powered[b]:
                                powered[b] = True
                                stack.append(b)
            if all(powered[1:]):
                best = cost
    print(best)


main()
