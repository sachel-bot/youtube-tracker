#!/bin/bash
# YouTube tracker 每日刷新：抓最新 10 个视频 + 重建 HTML
# 由 launchd 触发，也可以手动跑

set -e

ROOT="/Users/xiqiao/youtube-tracker"
LOG_DIR="$ROOT/logs"
LOG_FILE="$LOG_DIR/refresh.log"
PYTHON="/usr/bin/python3"

mkdir -p "$LOG_DIR"

{
  echo ""
  echo "============================================================"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始刷新"
  echo "============================================================"

  cd "$ROOT/scripts"

  echo "▶ Step 2: 抓视频..."
  "$PYTHON" step2_fetch_videos.py

  echo ""
  echo "▶ Step 4: 重建 dashboard.html..."
  "$PYTHON" step4_build_dashboard.py

  echo ""
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 刷新完成"
} >> "$LOG_FILE" 2>&1
