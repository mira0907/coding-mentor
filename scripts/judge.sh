#!/usr/bin/env bash
# 評測講義題目。
#   ./scripts/judge.sh 3-1 solutions/3-1.cpp   指定題號與程式檔
#   ./scripts/judge.sh solutions/3-1.cpp       檔名就是題號時可以省略題號
#   ./scripts/judge.sh new 3-1                 用模板建立 solutions/3-1.cpp、3-1.md 並顯示題目
#   ./scripts/judge.sh list                    列出所有題目與你的最佳結果
# 其他參數（例如 --debug）會原樣交給 judge/judge.py。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="python3"

if [ $# -ge 1 ] && [ "$1" = "new" ]; then
  [ $# -ge 2 ] || { echo "用法: $0 new <題號>"; exit 1; }
  ID="$2"; FILE="$ROOT/solutions/$ID.cpp"
  [ -d "$ROOT/judge/problems/$ID" ] || { echo "找不到題目 $ID，可以用 '$0 list' 查題號"; exit 1; }
  mkdir -p "$ROOT/solutions"
  if [ -e "$FILE" ]; then echo "已存在: $FILE"; else cp "$ROOT/template/template.cpp" "$FILE"; echo "已建立 $FILE"; fi
  NOTE="$ROOT/solutions/$ID.md"                       # 練習紀錄
  if [ ! -e "$NOTE" ]; then sed "1s/<題號>/$ID/" "$ROOT/solutions/_template.md" > "$NOTE"; echo "已建立 ${NOTE}（AC 後記得填寫）"; fi
  "$PY" "$ROOT/judge/judge.py" show "$ID"
  exit 0
fi
if [ $# -ge 1 ] && [ "$1" = "list" ]; then exec "$PY" "$ROOT/judge/judge.py" list; fi

if [ $# -ge 2 ] && [[ "$2" == *.cpp ]]; then
  ID="$1"; FILE="$2"; shift 2
elif [ $# -ge 1 ] && [[ "$1" == *.cpp ]]; then
  ID=""; FILE="$1"; shift 1
else
  sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi
[ -n "$ID" ] || ID="$(basename "${FILE%.cpp}")"      # 沒給題號就用檔名
exec "$PY" "$ROOT/judge/judge.py" "$ID" "$FILE" "$@"
