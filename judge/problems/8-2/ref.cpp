#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 路口數
    // m = 街道數
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> g(n + 1);  // g[u] = (v, 街道編號)：從 u 沿這條街道會到 v
    vector<int> deg(n + 1, 0);               // deg[u] = 路口 u 的度數，自環算 2
    for (int i = 0; i < m; i++) {            // i = 街道編號
        // u = 街道的一端
        // v = 街道的另一端，u = v 時是繞回原路口的環狀巷
        int u, v;
        cin >> u >> v;
        g[u].push_back({v, i});
        g[v].push_back({u, i});              // 自環會在 g[u] 出現兩次，兩次是同一個編號
        deg[u]++; deg[v]++;
    }
    for (int u = 1; u <= n; u++) sort(g[u].begin(), g[u].end());   // 鄰居由小到大，才會先試小的路口
    int odd = 0;                             // odd = 奇度點的個數
    int start = 0;                           // start = 出發的路口，0 表示還沒決定
    for (int u = 1; u <= n; u++)             // u = 檢查的路口
        if (deg[u] % 2 == 1) { odd++; if (start == 0) start = u; }   // 編號最小的奇度點
    if (odd != 0 && odd != 2) { cout << -1 << "\n"; return 0; }
    if (odd == 0)                            // 全是偶度點：從編號最小、有街道的路口出發
        for (int u = 1; u <= n; u++) if (deg[u] > 0) { start = u; break; }
    // Hierholzer，用堆疊取代遞迴，m = 2×10^5 時遞迴會太深
    vector<bool> used(m, false);             // used[i] = 街道 i 掃過了沒
    vector<int> ptr(n + 1, 0);               // ptr[u] = g[u] 中下一條要檢查的街道是第幾條
    vector<int> st = {start};                // st = 模擬遞迴的堆疊，存「走到一半」的路口
    vector<int> path;                        // path = 依「卡住」的順序記下的路口，最後要反轉
    path.reserve(m + 1);
    while (!st.empty()) {
        int u = st.back();                   // u = 堆疊頂端，也就是目前所在的路口
        while (ptr[u] < (int)g[u].size() && used[g[u][ptr[u]].second]) ptr[u]++;   // 跳過從另一端掃過的街道
        if (ptr[u] == (int)g[u].size()) {    // u 沒有街道可走了：加入答案，退回上一個路口
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = g[u][ptr[u]++];   // v = 走過去會到的路口，id = 這條街道的編號
            used[id] = true;
            st.push_back(v);
        }
    }
    if ((int)path.size() != m + 1) { cout << -1 << "\n"; return 0; }   // 有街道和起點不連通，沒有被掃到
    reverse(path.begin(), path.end());
    for (int i = 0; i <= m; i++) cout << path[i] << " \n"[i == m];   // i = 路線上的第幾個路口
}
