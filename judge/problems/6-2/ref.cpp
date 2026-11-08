#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                              // n = 學校數，m = 通報線路數
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);        // adj[u] = u 收到通知後會轉告的學校
    vector<pair<int,int>> edges(m);        // 所有線路 (u, v)，縮點時要再用一次
    for (auto& [u, v] : edges) {           // u → v：u 收到後轉告 v
        cin >> u >> v;
        adj[u].push_back(v);
    }
    // dfn[u]：u 被拜訪的順序，0 表示還沒拜訪
    // low[u]：從 u 的子樹出發，最多經過一條非樹邊能到的最小 dfn（只算還在 stk 裡的點）
    // comp[u]：u 屬於第幾個 SCC
    // it[u]：u 已經處理到第幾個鄰居
    // stk：還沒分進任何 SCC 的點，依拜訪順序堆起來
    vector<int> dfn(n + 1, 0), low(n + 1, 0), comp(n + 1, 0), it(n + 1, 0), stk;
    vector<bool> inStk(n + 1, false);      // inStk[u] = u 目前是否在 stk 裡
    int timer_ = 0;                        // 時間戳計數器
    int sccCnt = 0;                        // 目前找到幾個 SCC
    // 用顯式堆疊模擬遞迴的 Tarjan，寫法同範例 6-A
    for (int s = 1; s <= n; s++) {         // s = 還沒拜訪過的起點
        if (dfn[s]) continue;
        vector<int> st = {s};              // st = 目前的遞迴路徑，最上面是正在處理的點
        dfn[s] = low[s] = ++timer_;
        stk.push_back(s); inStk[s] = true;
        while (!st.empty()) {
            int u = st.back();             // u = 正在處理的點
            if (it[u] < (int)adj[u].size()) {
                int v = adj[u][it[u]++];   // v = u 指向的下一個點
                if (!dfn[v]) {             // 樹邊：相當於遞迴呼叫 tarjan(v)
                    dfn[v] = low[v] = ++timer_;
                    stk.push_back(v); inStk[v] = true;
                    st.push_back(v);
                } else if (inStk[v]) low[u] = min(low[u], dfn[v]);   // v 還在堆疊中：可以回到 v
            } else {                       // u 的鄰居都處理完，相當於 return
                if (low[u] == dfn[u]) {    // u 是一個 SCC 的根
                    ++sccCnt;
                    while (true) {
                        int x = stk.back(); stk.pop_back();   // x = 屬於這個 SCC 的點
                        inStk[x] = false; comp[x] = sccCnt;
                        if (x == u) break;
                    }
                }
                st.pop_back();
                if (!st.empty()) {
                    int p = st.back();     // p = u 的父節點
                    low[p] = min(low[p], low[u]);
                }
            }
        }
    }
    // 縮點後只需要知道每個 SCC 的入邊、出邊有沒有
    // hasIn[c]：有沒有別的 SCC 的線路指向 c
    // hasOut[c]：c 有沒有線路指向別的 SCC
    vector<bool> hasIn(sccCnt + 1, false), hasOut(sccCnt + 1, false);
    for (auto [u, v] : edges)              // 線路 u → v
        if (comp[u] != comp[v]) { hasOut[comp[u]] = true; hasIn[comp[v]] = true; }
    int src = 0;                           // 入度 0 的 SCC 數（沒有人會通知它們）
    int sink = 0;                          // 出度 0 的 SCC 數（它們不會通知別人）
    for (int c = 1; c <= sccCnt; c++) {    // c = SCC 編號
        if (!hasIn[c]) src++;
        if (!hasOut[c]) sink++;
    }
    cout << src << " " << (sccCnt == 1 ? 0 : max(src, sink)) << "\n";   // 只有一個 SCC 時不用加線路
}
