#include <bits/stdc++.h>
using namespace std;
struct DSU {
    // p[x]：x 的父節點，p[x] == x 代表 x 是這一組的根
    // sz[x]：以 x 為根的這一組有幾個鄉鎮，只有根的值有意義
    vector<int> p, sz;
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }   // n = 鄉鎮數；一開始每個鄉鎮自成一組
    // 回傳 x 所在組的根，並路徑壓縮
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    // 合併 a、b 所在的組；已經同組時回傳 false
    bool unite(int a, int b) {
        a = find(a); b = find(b);             // 之後 a、b 代表兩組各自的根
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);        // 小的接到大的下面
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 鄉鎮數
    // m = 道路數
    // q = 詢問數
    int n, m, q;
    cin >> n >> m >> q;
    vector<array<int,3>> e(m);                // e[i] = {w, u, v}：連接 u、v 的道路，耐風等級 w
    for (auto& [w, u, v] : e) cin >> u >> v >> w;
    vector<array<int,3>> qs(q);               // qs[i] = {x, v, i}：第 i 筆詢問，颱風等級 x、出發鄉鎮 v
    for (int i = 0; i < q; i++) {             // i = 詢問編號（從 0 開始）
        cin >> qs[i][1] >> qs[i][0];
        qs[i][2] = i;
    }
    sort(e.begin(), e.end(), greater<>());    // 道路依耐風等級由大到小
    sort(qs.begin(), qs.end(), greater<>());  // 詢問依颱風等級由大到小
    DSU dsu(n);                               // 目前「還開著的道路」把鄉鎮分成的連通塊
    vector<int> ans(q);                       // ans[i] = 第 i 筆詢問的答案
    int ptr = 0;                              // ptr = 下一條還沒加入的道路在 e 裡的位置
    for (auto [x, v, id] : qs) {              // 颱風等級 x，從 v 出發，這是第 id 筆詢問
        while (ptr < m && e[ptr][0] >= x) {   // 耐風等級 ≥ x 的道路在這次颱風中還開著
            dsu.unite(e[ptr][1], e[ptr][2]);
            ptr++;
        }
        ans[id] = dsu.sz[dsu.find(v)];        // v 所在連通塊的大小，就是能到達的鄉鎮數
    }
    for (int i = 0; i < q; i++) cout << ans[i] << "\n";   // i = 詢問編號，依輸入順序輸出
}
