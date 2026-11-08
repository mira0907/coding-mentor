#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct DSU {
    vector<int> p, sz;                   // p[x] = x 的父節點，sz[x] = 以 x 為根的組大小
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }   // 元素編號 0 到 n
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
    int n, m;                            // n = 村莊數，m = 可以架設的電線數
    cin >> n >> m;
    vector<array<ll,3>> e;              // 所有的邊，每個元素 (w, u, v)：u、v 之間的邊，花費 w
    for (int i = 1; i <= n; i++) {       // i = 村莊編號
        ll c; cin >> c;                  // c = 在村莊 i 蓋發電廠的花費
        e.push_back({c, 0, i});         // 虛擬發電廠 0 號點
    }
    for (int i = 0; i < m; i++) {        // i = 正在讀第幾條電線
        ll u, v, w; cin >> u >> v >> w;  // 電線連接村莊 u、v，花費 w
        e.push_back({w, u, v});
    }
    sort(e.begin(), e.end());            // 依花費 w 由小到大排序
    DSU dsu(n);                          // 0..n 共 n+1 個點
    ll total = 0;                        // 總花費
    for (auto [w, u, v] : e)
        if (dsu.unite(u, v)) total += w;
    cout << total << "\n";
}
