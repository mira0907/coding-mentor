#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 做法：把價格切成一段段「谷底 → 山頂」的上漲區段，用堆疊合併區段，
// 拆成一堆「互相獨立的獲利」，最後取最大的 K 個加總。O(N log N)。
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // n：時間點數
    // k：交易次數上限
    int n;
    ll k;
    cin >> n >> k;
    vector<ll> p(n);                          // p[i]：第 i 個時間點的價格
    for (auto& x : p) cin >> x;

    vector<pair<int, int>> st;                // st：還沒結算的區段，存（谷底位置, 山頂位置）
    vector<ll> gains;                         // gains：拆出來的獨立獲利
    // v：目前區段的谷底位置
    // q：目前區段的山頂位置
    int v = 0, q = -1;
    while (true) {
        for (v = q + 1; v + 1 < n && p[v] >= p[v + 1]; v++) {}   // 往右找下一個谷底
        for (q = v; q + 1 < n && p[q] <= p[q + 1]; q++) {}       // 從谷底往右找山頂
        if (q == v) break;                                        // 沒有上漲了
        // 新谷底比堆疊頂端的谷底還低：頂端區段之後不可能再合併，先結算
        while (!st.empty() && p[v] < p[st.back().first]) {
            gains.push_back(p[st.back().second] - p[st.back().first]);
            st.pop_back();
        }
        // 新山頂不低於頂端的山頂：可以合併成「舊谷底 → 新山頂」，
        // 拆成「舊山頂 − 新谷底」這筆獨立獲利，加上合併後的大區段
        while (!st.empty() && p[q] >= p[st.back().second]) {
            gains.push_back(p[st.back().second] - p[v]);
            v = st.back().first;
            st.pop_back();
        }
        st.push_back({v, q});
    }
    for (auto [a, b] : st) gains.push_back(p[b] - p[a]);   // a：谷底；b：山頂

    // 取最大的 k 筆獲利
    ll take = min<ll>(k, gains.size());       // take：實際要取幾筆
    nth_element(gains.begin(), gains.begin() + take, gains.end(), greater<ll>());
    ll best = 0;                              // best：最大獲利
    for (ll i = 0; i < take; i++) best += gains[i];
    cout << best << '\n';
    return 0;
}
