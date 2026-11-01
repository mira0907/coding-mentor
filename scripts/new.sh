#!/usr/bin/env bash
# 用法: ./scripts/new.sh <題目名稱>   例: ./scripts/new.sh cf-1900A
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ $# -ge 1 ] || { echo "用法: $0 <題目名稱>"; exit 1; }
DIR="$ROOT/problems/$1"
[ -e "$DIR" ] && { echo "已存在: $DIR"; exit 1; }
mkdir -p "$DIR/tests"
cp "$ROOT/template/template.cpp" "$DIR/sol.cpp"
touch "$DIR/tests/1.in" "$DIR/tests/1.out"
cat > "$DIR/README.md" <<MD
# $1

- 來源 / 連結：
- 難度 / 標籤：
- 日期：$(date +%Y-%m-%d)
- 狀態：❌ 未解決

## 題目摘要


## 卡住的地方


## 正解思路


## 複雜度

MD
echo "已建立 $DIR"
