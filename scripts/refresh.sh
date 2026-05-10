#!/bin/bash
# YouTube tracker 每日刷新：抓数据 → 重建 HTML → 历史快照 → 自动 git push
# 由 launchd 触发（每天 9:00），也可以手动跑

ROOT="/Users/xiqiao/youtube-tracker"
LOG_DIR="$ROOT/logs"
LOG_FILE="$LOG_DIR/refresh.log"
PYTHON="/usr/bin/python3"
HISTORY_DIR="$ROOT/data/history"

mkdir -p "$LOG_DIR" "$HISTORY_DIR"

{
  echo ""
  echo "============================================================"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始刷新"
  echo "============================================================"

  cd "$ROOT/scripts" || exit 1

  echo "▶ Step 2: 抓视频..."
  if ! "$PYTHON" step2_fetch_videos.py; then
    echo "  ❌ 抓数据失败，跳过 push"
    exit 1
  fi

  echo ""
  echo "▶ Step 4: 重建 dashboard.html..."
  if ! "$PYTHON" step4_build_dashboard.py; then
    echo "  ❌ 重建 HTML 失败"
    exit 1
  fi

  echo ""
  echo "▶ 历史快照..."
  TODAY=$(date +%Y-%m-%d)
  cp "$ROOT/data/channels_data.json" "$HISTORY_DIR/$TODAY.json"
  echo "  ✅ 写入 $HISTORY_DIR/$TODAY.json"

  # 维护 index.json (前端 fetch 用)
  cd "$HISTORY_DIR"
  ls -1 *.json 2>/dev/null | grep -v 'index.json' | sed 's/\.json$//' | sort | python3 -c "
import sys, json
dates = [l.strip() for l in sys.stdin if l.strip()]
print(json.dumps({'snapshots': dates, 'count': len(dates)}, indent=2))
" > index.json
  SNAP_COUNT=$(python3 -c "import json; print(json.load(open('$HISTORY_DIR/index.json'))['count'])")
  echo "  ✅ 已积累 $SNAP_COUNT 天快照"

  # 删 90 天前的快照
  find "$HISTORY_DIR" -name '*.json' -mtime +90 -not -name 'index.json' -delete 2>/dev/null

  echo ""
  echo "▶ Git: 同步云端..."
  cd "$ROOT" || exit 1

  if git diff --quiet -- data dashboard.html 2>/dev/null; then
    echo "  数据无变化，跳过 commit/push"
  else
    git add data dashboard.html
    if git commit -m "Auto refresh: $(date '+%Y-%m-%d %H:%M')" 2>&1; then
      if git push origin main 2>&1; then
        echo "  ✅ 已 push 到 https://sachel-bot.github.io/youtube-tracker/"
      else
        echo "  ⚠️  push 失败（数据已 commit，下次会一起 push）"
      fi
    else
      echo "  ⚠️  commit 失败"
    fi
  fi

  echo ""
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 刷新完成"
} >> "$LOG_FILE" 2>&1
