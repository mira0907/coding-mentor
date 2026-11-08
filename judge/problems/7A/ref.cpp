#include <bits/stdc++.h>
using namespace std;
using ll = long long;
int n;                                      // n = 村莊數
vector<vector<pair<int,int>>> adj;          // adj[u] = (v, w)：u、v 之間有長度 w 的道路
// 回傳 (最遠點, 距離)；用 stack 取代遞迴，避免鏈狀樹堆疊溢位
// s = 出發的村莊
pair<int,ll> farthest(int s) {
    vector<ll> dist(n + 1, -1);             // dist[v] = s 到 v 的距離，-1 表示還沒走到
    vector<int> st = {s};                   // st = 等待處理的點；樹上路徑唯一，處理順序不影響答案
    dist[s] = 0;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();   // u = 取出的點
        for (auto [v, w] : adj[u]) if (dist[v] < 0) {   // v = u 的鄰居，w = 道路長度
            dist[v] = dist[u] + w; st.push_back(v);
        }
    }
    int best = s;                           // best = 目前最遠的點
    for (int i = 1; i <= n; i++) if (dist[i] > dist[best]) best = i;
    return {best, dist[best]};
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> n;
    adj.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++) {       // i = 正在讀第幾條道路
        int u, v, w; cin >> u >> v >> w;    // 道路連接 u、v，長度 w
        adj[u].push_back({v, w}); adj[v].push_back({u, w});
    }
    int A = farthest(1).first;              // A = 離村莊 1 最遠的點，一定是直徑的一端
    cout << farthest(A).second << "\n";     // 從 A 出發的最遠距離就是直徑
}
