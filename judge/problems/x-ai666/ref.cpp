#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // n：時間點數
    // k：交易次數上限
    int n, k;
    cin >> n >> k;
    vector<ll> p(n);                  // p[i]：第 i 個時間點的價格
    for (auto& x : p) cin >> x;
    k = min(k, n / 2);                // 交易超過 n/2 次沒有意義
    const ll NEG = LLONG_MIN / 4;     // 代表「不可能的狀態」
    vector<ll> hold(k + 1, NEG);      // hold[j]：已經買了第 j 次、手上有貨時的最大獲利
    vector<ll> sold(k + 1, 0);        // sold[j]：完成了 j 次交易、手上沒貨時的最大獲利
    for (int i = 0; i < n; i++) {     // i：目前的時間點
        for (int j = k; j >= 1; j--) {    // j：第幾次交易；倒著跑，避免同一天先買又賣
            sold[j] = max(sold[j], hold[j] + p[i]);       // 今天賣出第 j 次
            hold[j] = max(hold[j], sold[j - 1] - p[i]);   // 今天買進第 j 次
        }
    }
    ll best = 0;                      // best：所有交易次數中的最大獲利
    for (int j = 0; j <= k; j++) best = max(best, sold[j]);
    cout << best << '\n';
    return 0;
}
