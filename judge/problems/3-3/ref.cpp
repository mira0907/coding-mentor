#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;                          // 代表走不到

// s = 起點，g = 要在上面跑的圖（g[u] 存 (v, w) 表示 u → v、時間 w）
// 回傳 dist[v] = 在圖 g 上 s 到 v 的最短時間，走不到時為 INF
vector<ll> dijkstra(int s, const vector<vector<pair<int,int>>>& g) {
    int n = (int)g.size() - 1;                // n = 點數，編號 1 到 n
    vector<ll> dist(n + 1, INF);              // dist[v] = 目前找到的 s 到 v 最短時間
    // pq 存 (時間, 點)，greater<> 讓時間最小的先出來
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[s] = 0; pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();     // u = 取出的點，d = 放進堆積時它的時間
        if (d > dist[u]) continue;            // 過期的項目，跳過
        for (auto [v, w] : g[u]) {            // 每條邊 u → v，時間 w
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 路口數
    // m = 單向道路數
    // s = 醫院所在的路口
    // t = 災區所在的路口
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    // eu[i] = 第 i 條道路的起點
    // ev[i] = 第 i 條道路的終點
    // ew[i] = 走第 i 條道路要幾分鐘
    vector<int> eu(m), ev(m), ew(m);
    vector<vector<pair<int,int>>> g(n + 1);   // g[u] = 原圖的出邊 (v, w)
    vector<vector<pair<int,int>>> rg(n + 1);  // rg[v] = 反向圖的出邊 (u, w)：原圖的 u → v 反過來存
    for (int i = 0; i < m; i++) {             // i = 正在讀第幾條道路（從 0 開始）
        cin >> eu[i] >> ev[i] >> ew[i];
        g[eu[i]].push_back({ev[i], ew[i]});
        rg[ev[i]].push_back({eu[i], ew[i]});
    }
    vector<ll> ds = dijkstra(s, g);           // ds[v] = s 到 v 的最短時間
    vector<ll> dt = dijkstra(t, rg);          // dt[v] = v 到 t 的最短時間（反向圖上 t 到 v）
    ll D = ds[t];                             // D = s 到 t 的最短時間
    vector<int> type(m, 0);                   // type[i] = 第 i 條路的答案：0 = NONE，1 = SOME，2 = ALL
    if (D < INF) {
        vector<int> sp;                       // sp = 在某條最短路線上的道路編號
        vector<ll> pts;                       // pts = 這些道路的時間區間端點，排序去重後當座標
        for (int i = 0; i < m; i++) {         // i = 正在檢查的道路
            if (ds[eu[i]] == INF || dt[ev[i]] == INF) continue;
            if (ds[eu[i]] + ew[i] + dt[ev[i]] != D) continue;   // 3.1 節的判斷式
            sp.push_back(i);
            pts.push_back(ds[eu[i]]);              // 區間起點：救護車開上這條路的時刻
            pts.push_back(ds[eu[i]] + ew[i]);      // 區間終點：開下這條路的時刻
        }
        sort(pts.begin(), pts.end());
        pts.erase(unique(pts.begin(), pts.end()), pts.end());
        int k = pts.size();                   // k = 不同端點的個數，第 j 小段是 [pts[j], pts[j+1])
        // pos(x) = 時刻 x 在 pts 裡的位置
        auto pos = [&](ll x) { return int(lower_bound(pts.begin(), pts.end(), x) - pts.begin()); };
        vector<int> cover(k + 1, 0);          // 先當差分陣列，前綴和後 cover[j] = 蓋住第 j 小段的道路數
        for (int i : sp) {                    // i = 某條最短路線上的道路
            cover[pos(ds[eu[i]])]++;
            cover[pos(ds[eu[i]] + ew[i])]--;
        }
        for (int j = 1; j < k; j++) cover[j] += cover[j - 1];   // j = 第幾小段
        vector<int> bad(k + 1, 0);            // bad[j] = 前 j 小段裡，被兩條以上道路蓋住的段數
        for (int j = 0; j < k; j++) bad[j + 1] = bad[j] + (cover[j] >= 2);
        for (int i : sp) {                    // i = 某條最短路線上的道路
            int l = pos(ds[eu[i]]);           // l = 這條路區間的第一小段
            int r = pos(ds[eu[i]] + ew[i]);   // r = 區間結束的位置，蓋住第 l 到 r − 1 小段
            type[i] = (bad[r] - bad[l] == 0) ? 2 : 1;   // 區間內沒有別的路重疊才是 ALL
        }
    }
    const char* name[3] = {"NONE", "SOME", "ALL"};   // name[x] = type 為 x 時要輸出的字
    for (int i = 0; i < m; i++) cout << name[type[i]] << "\n";   // i = 道路編號（從 0 開始）
}
