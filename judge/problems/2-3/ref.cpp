#include <bits/stdc++.h>
using namespace std;
vector<vector<int>> adj;                 // adj[u] = 和 u 有網路線相連的伺服器
// tin[u]：DFS 第一次進入 u 的時間戳
// tout[u]：DFS 離開 u 的時間戳
vector<int> tin, tout;
vector<vector<int>> kids;                // kids[u] = u 的子節點，依進入順序排列，所以 tin 由小到大
// 回傳 a 是否為 b 的祖先（a == b 也算）
bool isAnc(int a, int b) { return tin[a] <= tin[b] && tout[b] <= tout[a]; }
// x = 關機的伺服器，u = 另一台伺服器（u != x）
// 回傳 x 關機後 u 落在哪一塊：0 表示 x 子樹外面那一塊，否則是 u 所在子樹的根（x 的某個子節點）
int part(int x, int u) {
    if (!isAnc(x, u)) return 0;
    const vector<int>& ch = kids[x];     // ch = x 的子節點們
    // 找最後一個 tin <= tin[u] 的子節點，u 就在它的子樹裡
    // lo = 二分搜尋範圍的左端（ch 的索引）
    // hi = 二分搜尋範圍的右端
    int lo = 0, hi = (int)ch.size() - 1;
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2;     // 偏右的中點，避免 lo = mid 時卡住
        if (tin[ch[mid]] <= tin[u]) lo = mid;
        else hi = mid - 1;
    }
    return ch[lo];
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 伺服器數
    // q = 詢問數
    int n, q;
    cin >> n >> q;
    adj.assign(n + 1, {});
    for (int i = 0; i < n - 1; i++) {    // i = 正在讀第幾條網路線
        // a = 網路線的一端
        // b = 網路線的另一端
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    tin.assign(n + 1, 0); tout.assign(n + 1, 0); kids.assign(n + 1, {});
    vector<int> par(n + 1, 0);           // par[u] = u 在 DFS 樹上的父節點，根的父節點設為 0
    int timer_ = 0;                      // 時間戳計數器，進入或離開一個點都加 1
    // 不用遞迴的 DFS，鏈狀的樹深度可達 2×10⁵
    vector<pair<int,int>> st;            // 模擬遞迴的堆疊，每格存 (點, 下一個要看的鄰居是第幾個)
    tin[1] = ++timer_;
    st.push_back({1, 0});
    while (!st.empty()) {
        // u = 堆疊頂端的點
        // i = u 下一個要看的鄰居索引
        auto& [u, i] = st.back();
        if (i < (int)adj[u].size()) {
            int v = adj[u][i++];         // v = u 的第 i 個鄰居，看完後 i 加 1
            if (v == par[u]) continue;   // 樹沒有環，不是父節點就是子節點
            par[v] = u;
            kids[u].push_back(v);
            tin[v] = ++timer_;
            st.push_back({v, 0});        // push_back 之後 u、i 這兩個參照就失效了
        } else {
            tout[u] = ++timer_;
            st.pop_back();
        }
    }
    string out;                          // 所有答案先接成一個字串，最後一次輸出
    for (int k = 0; k < q; k++) {        // k = 第幾筆詢問
        // x = 關機的伺服器
        // u = 要通訊的第一台
        // v = 要通訊的第二台
        int x, u, v;
        cin >> x >> u >> v;
        bool ok;                         // u、v 在 x 關機後能否通訊
        if (u == x || v == x) ok = false;        // 關機的伺服器本身不能通訊
        else ok = (part(x, u) == part(x, v));    // 落在同一塊才連得到
        out += ok ? "YES\n" : "NO\n";
    }
    cout << out;
}
