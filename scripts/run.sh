#!/usr/bin/env bash
# 用法: ./scripts/run.sh <題目資料夾或 .cpp 檔>
# 編譯後，若有 tests/*.in 則逐一比對 *.out；否則直接執行（從鍵盤輸入）。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ $# -ge 1 ] || { echo "用法: $0 <題目資料夾或 .cpp 檔>"; exit 1; }

if [ -d "$1" ]; then DIR="$1"; SRC="$1/sol.cpp"; else SRC="$1"; DIR="$(dirname "$1")"; fi
BIN="$DIR/$(basename "${SRC%.cpp}")"

CXXFLAGS=(-std=c++17 -O2 -Wall -Wextra -Wshadow -DLOCAL -I"$ROOT/include"
          -fsanitize=address,undefined -g)
echo "編譯 $SRC ..."
clang++ "${CXXFLAGS[@]}" "$SRC" -o "$BIN"

shopt -s nullglob
INS=("$DIR"/tests/*.in)
NONEMPTY=()
for f in "${INS[@]}"; do [ -s "$f" ] && NONEMPTY+=("$f"); done

if [ ${#NONEMPTY[@]} -eq 0 ]; then
  echo "（沒有測資，直接執行，請輸入資料，Ctrl-D 結束）"
  "$BIN"
  exit
fi

pass=0; total=0
for in in "${NONEMPTY[@]}"; do
  total=$((total+1))
  out="${in%.in}.out"
  name="$(basename "$in")"
  start=$(perl -MTime::HiRes=time -e 'printf "%.0f", time*1000')
  actual="$("$BIN" < "$in")" || { echo "❌ $name 執行錯誤"; continue; }
  end=$(perl -MTime::HiRes=time -e 'printf "%.0f", time*1000')
  ms=$((end-start))
  if [ ! -s "$out" ]; then
    echo "➖ $name (${ms}ms) 無期望輸出，實際輸出："; echo "$actual"
  elif diff -bB <(echo "$actual") "$out" > /dev/null; then
    echo "✅ $name (${ms}ms)"; pass=$((pass+1))
  else
    echo "❌ $name (${ms}ms)"
    diff -bB <(echo "$actual") "$out" | sed 's/^/   /' || true
  fi
done
echo "結果：$pass / $total 通過"
