"""實作 1-2 傳話遊戲的暴力解：每個起點直接模擬傳話，用集合記誰聽過。"""
import sys

data = sys.stdin.read().split()
n = int(data[0])
a = [0] + [int(x) for x in data[1:1 + n]]
res = []
for s in range(1, n + 1):
    heard = set()                                # 這一輪聽過消息的人
    v = s
    while v not in heard:                        # 傳到聽過的人就停
        heard.add(v)
        v = a[v]
    res.append(len(heard))
print(" ".join(map(str, res)))
