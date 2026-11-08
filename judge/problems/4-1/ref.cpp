#include <bits/stdc++.h>
using namespace std;
struct DSU {
    vector<int> p, sz;                   // p[x] = x 的父節點，sz[x] = 以 x 為根的組大小
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }   // 一開始每個點自成一組
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }       // 找 x 的根並路徑壓縮
    bool unite(int a, int b) {           // 合併 a、b 所在的組，已經同組時回傳 false
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                        // n = 城市數，m = 道路數
    cin >> n >> m;
    DSU dsu(n);
    int comps = n;                   // 目前的連通塊數，一開始每座城市自成一塊
    for (int i = 0; i < m; i++) {    // i = 正在讀第幾條道路
        int u, v;                    // 這條道路連接 u、v
        cin >> u >> v;
        if (dsu.unite(u, v)) comps--;   // 連起兩個不同的連通塊，塊數少 1
    }
    cout << comps - 1 << "\n";       // k 個連通塊至少要再修 k − 1 條路
}
