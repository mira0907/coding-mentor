#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                                  // n = 點數，m = 邊數
    cin >> n >> m;
    vector<pair<int,int>> edges(m);            // edges[i] = 第 i 條邊的兩個端點 (u, v)
    vector<int> deg(n + 1, 0);                 // deg[x] = 點 x 的度數
    // auto& 讓 u、v 直接代表 edges 裡的那一格，讀進來的值才會存回 edges
    for (auto& [u, v] : edges) { cin >> u >> v; deg[u]++; deg[v]++; }
    // 依 (度數, 編號) 定向：從「小」指向「大」
    // less_(a, b)：a 是否排在 b 前面。度數小的在前，度數相同時編號小的在前
    auto less_ = [&](int a, int b) {
        return deg[a] != deg[b] ? deg[a] < deg[b] : a < b;
    };
    vector<vector<int>> out(n + 1);            // out[x] = 定向後從 x 指出去的點
    for (auto [u, v] : edges) {
        if (less_(u, v)) out[u].push_back(v);
        else out[v].push_back(u);
    }
    vector<int> mark(n + 1, 0);                // mark[x] == u 代表 x 是目前這個 u 的出鄰居
    long long tri = 0;                         // 三角形的個數
    for (int u = 1; u <= n; u++) {             // u = 三角形裡排序最前面的那個點
        for (int v : out[u]) mark[v] = u;          // 標記 u 的出鄰居
        for (int v : out[u])                       // v = u 指向的點
            for (int w : out[v])                   // w = v 指向的點
                if (mark[w] == u) tri++;           // u→v→w 且 u→w
    }
    cout << tri << "\n";
}
