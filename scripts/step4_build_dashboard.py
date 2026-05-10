"""
Step 4 (V4): YouTube 营销情报 Dashboard
- 深色蓝紫视觉系统（#0A0E1A 底 + 主色 #6366F1）
- 6 KPI + 智能洞察 + 二级统计 + 3 SVG 图
- 5 预设按钮 + 8 筛选器（多选不自动关）+ 多频道对比看板
- 视频卡片商业信号 + 批量模式 + 网格/列表/灵感视图切换
- 5 Tabs（首页/拆解清单/品牌对比/历史趋势/竞品监测）+ 拆解清单 10 维
- 移动端：底部工具栏 + 抽屉筛选 + 单列卡片
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST_FILE = ROOT / "data" / "channels_list.json"
OUT_FILE = ROOT / "dashboard.html"

GROUP_LABELS = {
    "A_brand":          "A 竞品 + 自家",
    "B_ipad_vertical":  "B iPad 垂直/媒体",
    "C_top_tech":       "C 头部数码",
    "D_real_use":       "D iPad 真实使用",
    "E_lifestyle":      "E Lifestyle",
    "F_3c_brand":       "F 3C 品牌学习",
}
SELF_BRAND = "Typecase"
BRAND_COMPARE_DEFAULT = ["Typecase", "Apple", "Logitech", "ESR Gear"]
TOP_KOL = ["MKBHD", "iJustine", "Linus Tech Tips", "Casey Neistat", "Mrwhosetheboss", "Dave Lee"]
CONTENT_TAGS_ORDER = ["iPad配件相关", "创作", "学生", "商务", "其他Apple", "其他"]
LENGTH_ORDER       = ["Shorts", "Short", "Medium", "Long"]
HOT_LEVEL_ORDER    = ["🔥 上升爆款", "💥 强爆款", "⭐ 百万爆款", "🚀 现象级"]
VIDEO_TYPE_ORDER   = ["评测", "开箱", "对比", "装机/Setup", "教程", "教学", "vlog", "宣传片/广告", "产品发布", "推荐/Best", "其他"]


def main():
    list_data = json.loads(LIST_FILE.read_text())
    channels_meta = list_data["channels"]
    tree = {}
    for c in channels_meta:
        tree.setdefault(c["group"], []).append({
            "display_name": c["display_name"],
            "subscriber_count": c["subscriber_count"],
            "is_self": c["display_name"] == SELF_BRAND,
        })
    for k in tree:
        tree[k].sort(key=lambda x: -x["subscriber_count"])

    cfg = {
        "group_labels":           GROUP_LABELS,
        "channel_tree":           tree,
        "self_brand":             SELF_BRAND,
        "brand_compare_default":  BRAND_COMPARE_DEFAULT,
        "top_kol":                TOP_KOL,
        "content_tags_order":     CONTENT_TAGS_ORDER,
        "length_order":           LENGTH_ORDER,
        "hot_level_order":        HOT_LEVEL_ORDER,
        "video_type_order":       VIDEO_TYPE_ORDER,
    }
    cfg_json = json.dumps(cfg, ensure_ascii=False)

    # 注意：以下 HTML 模板里所有 JS 用到 \n / \t / \u 都写成 \\n / \\t / \\u
    html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta http-equiv="Cache-Control" content="no-store">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="YT Tracker">
<title>YouTube 北美 iPad 配件内容情报</title>
<style>
  :root {
    --bg: #0A0E1A;
    --card: #131826;
    --card-hover: #1A2032;
    --text: #F1F5F9;
    --text-muted: #94A3B8;
    --text-faint: #64748B;
    --primary: #6366F1;
    --primary-2: #3B82F6;
    --primary-bg: rgba(99,102,241,0.15);
    --primary-text: #C7D2FE;
    --purple: #A855F7;
    --purple-bg: rgba(168,85,247,0.15);
    --purple-text: #DDD6FE;
    --rose: #EC4899;
    --rose-bg: rgba(236,72,153,0.15);
    --rose-text: #F9A8D4;
    --up: #10B981;
    --down: #F43F5E;
    --warn: #F59E0B;
    --info: #06B6D4;
    --red-bg: rgba(239,68,68,0.15);
    --red-text: #FCA5A5;
    --orange-bg: rgba(245,158,11,0.15);
    --orange-text: #FCD34D;
    --green-bg: rgba(16,185,129,0.15);
    --green-text: #6EE7B7;
    --gray-bg: rgba(148,163,184,0.15);
    --gray-text: #CBD5E1;
    --border: #1E293B;
    --border-hover: #334155;
    --er-1: #34D399;
    --er-2: #6EE7B7;
    --er-3: #FCD34D;
    --er-4: #FDBA74;
    --er-5: #FCA5A5;
    --er-0: #94A3B8;
    --shadow: 0 4px 20px rgba(0,0,0,0.4);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.5);
    --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Microsoft YaHei", sans-serif;
    --font-mono: "JetBrains Mono", "SF Mono", ui-monospace, "Menlo", monospace;
  }
  * { box-sizing: border-box; }
  html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
  body { margin: 0; background: var(--bg); color: var(--text);
    font-family: var(--font-sans); font-size: 14px; line-height: 1.5;
    -webkit-tap-highlight-color: transparent; }
  a { color: inherit; text-decoration: none; }
  button { font-family: inherit; font-size: inherit; cursor: pointer; }
  input, select { font-family: inherit; }

  /* Header */
  header {
    position: sticky; top: 0; z-index: 100;
    background: rgba(10,14,26,0.95);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid var(--border);
  }
  .container { max-width: 1440px; margin: 0 auto; padding: 16px 28px; }
  .hero h1 { margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.01em; }
  .hero .subtitle { color: var(--text-muted); font-size: 13px; margin-top: 4px; font-weight: 500; }
  .meta-line { color: var(--text-faint); font-size: 11.5px; margin-top: 6px; display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }
  .meta-line b { color: var(--text); }
  .live-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--up); display: inline-block; margin-right: 5px; animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

  /* Tabs */
  .tabs { display: flex; gap: 2px; margin-top: 14px; flex-wrap: wrap; }
  .tab { padding: 8px 16px; border-radius: 10px; font-size: 13px; color: var(--text-muted);
    background: transparent; border: 1px solid transparent; font-weight: 500;
    transition: all 0.15s ease; min-height: 36px; display: inline-flex; align-items: center; gap: 6px; }
  .tab:hover { color: var(--text); background: var(--card); }
  .tab.active { background: var(--primary-bg); color: var(--primary-text); border-color: var(--primary); }
  .tab-badge { background: var(--primary); color: #0A0E1A; font-size: 10.5px; font-weight: 700;
    padding: 1px 7px; border-radius: 9px; min-width: 18px; text-align: center; }

  /* KPI bar */
  .kpi-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-top: 14px; }
  .kpi-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px; transition: border-color 0.15s; min-height: 110px; }
  .kpi-card:hover { border-color: var(--primary); }
  .kpi-card .icon { color: var(--text-muted); font-size: 14px; }
  .kpi-card .label { color: var(--text-muted); font-size: 12px; font-weight: 500; margin-bottom: 6px;
    text-transform: uppercase; letter-spacing: 0.04em; display: flex; align-items: center; justify-content: space-between; }
  .kpi-card .big { font-family: var(--font-mono); font-weight: 600; font-size: 30px; line-height: 1.1;
    letter-spacing: -0.02em; color: var(--text); }
  .kpi-card .big.green { color: var(--up); }
  .kpi-card .big.purple { color: var(--purple); }
  .kpi-card .sub { font-size: 11px; color: var(--text-faint); margin-top: 4px; }
  .kpi-card .sparkline { margin-top: 6px; }

  /* Insight banner */
  .insight {
    background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(168,85,247,0.06));
    border: 1px solid rgba(99,102,241,0.3);
    border-left: 3px solid var(--primary);
    border-radius: 10px; padding: 12px 16px; margin-top: 14px;
    font-size: 13px; color: var(--text); }
  .insight .title { font-weight: 600; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
  .insight ul { margin: 4px 0; padding-left: 18px; color: var(--text-muted); font-size: 12.5px; }
  .insight ul li { margin: 2px 0; }

  /* Stats row */
  .stat-row { display: flex; flex-wrap: wrap; gap: 10px; padding: 12px 0;
    border-top: 1px dashed var(--border); margin-top: 12px; align-items: center; font-size: 12.5px; color: var(--text-muted); }
  .stat-row .label { color: var(--text-faint); font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; margin-right: 4px; }
  .pill { padding: 3px 10px; border-radius: 12px; font-size: 11.5px; font-weight: 600;
    display: inline-flex; align-items: center; gap: 4px; border: 1px solid; }
  .pill.rising { background: var(--red-bg); color: var(--red-text); border-color: rgba(239,68,68,0.4); }
  .pill.strong { background: var(--orange-bg); color: var(--orange-text); border-color: rgba(245,158,11,0.4); }
  .pill.million { background: var(--red-bg); color: var(--red-text); border-color: rgba(239,68,68,0.4); }
  .pill.phenom { background: var(--purple-bg); color: var(--purple-text); border-color: rgba(168,85,247,0.4); }
  .pill.tag-iPad { background: var(--red-bg); color: var(--red-text); border-color: rgba(239,68,68,0.4); }
  .pill.tag-creation { background: var(--purple-bg); color: var(--purple-text); border-color: rgba(168,85,247,0.4); }
  .pill.tag-student { background: var(--primary-bg); color: var(--primary-text); border-color: rgba(99,102,241,0.4); }
  .pill.tag-business { background: var(--green-bg); color: var(--green-text); border-color: rgba(16,185,129,0.4); }
  .pill.tag-apple { background: var(--gray-bg); color: var(--gray-text); border-color: rgba(148,163,184,0.4); }
  .pill.high-rel { background: var(--red-bg); color: var(--red-text); border-color: rgba(239,68,68,0.4); }
  .pill.mid-rel { background: var(--orange-bg); color: var(--orange-text); border-color: rgba(245,158,11,0.4); }
  .pill.low-rel { background: var(--gray-bg); color: var(--gray-text); border-color: rgba(148,163,184,0.4); }
  .stat-row .num { color: var(--text); font-weight: 600; font-family: var(--font-mono); }

  /* Charts */
  .charts { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-top: 16px; }
  .chart-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 14px; }
  .chart-card .title { font-size: 12px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px; }
  .chart-card .desc { font-size: 11px; color: var(--text-faint); margin-bottom: 10px; }
  .chart-card svg { width: 100%; height: 200px; display: block; }

  /* Presets */
  .presets { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; overflow-x: auto; padding-bottom: 4px; }
  .preset-btn { padding: 8px 14px; border-radius: 10px; border: 1px solid var(--border);
    background: var(--card); color: var(--text-muted); font-size: 12.5px; font-weight: 500;
    white-space: nowrap; transition: all 0.15s; min-height: 38px; display: inline-flex; align-items: center; gap: 6px; }
  .preset-btn:hover { border-color: var(--primary); color: var(--text); }
  .preset-btn.active { background: var(--primary-bg); color: var(--primary-text); border-color: var(--primary); font-weight: 600; }

  /* Filter bar */
  .filter-bar { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 0 6px; }
  .filter-bar .actions { margin-left: auto; display: flex; gap: 6px; align-items: center; }
  .result-count { padding: 6px 12px; border-radius: 8px; background: var(--card);
    color: var(--text); font-size: 13px; font-weight: 600; border: 1px solid var(--border); }
  .result-count.warn { color: var(--warn); }
  .result-count.alert { color: var(--down); border-color: var(--down); }

  /* Custom Dropdown */
  .dd { position: relative; display: inline-block; }
  .dd-btn { padding: 9px 14px; border: 1px solid var(--border); border-radius: 8px;
    background: var(--card); cursor: pointer; font-size: 13px; color: var(--text);
    display: inline-flex; align-items: center; gap: 8px; transition: all 0.15s; min-height: 38px; }
  .dd-btn:hover { border-color: var(--border-hover); }
  .dd.open .dd-btn { border-color: var(--primary); }
  .dd-btn .count { color: var(--primary); font-weight: 700; }
  .dd-btn .arrow { color: var(--text-muted); transition: transform 0.2s; flex-shrink: 0; }
  .dd.open .dd-btn .arrow { transform: rotate(180deg); color: var(--primary); }
  .dd-panel { display: none; position: absolute; top: calc(100% + 6px); left: 0;
    background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    box-shadow: var(--shadow-lg); z-index: 50; min-width: 260px; max-height: 440px;
    overflow: auto; padding: 6px; }
  .dd.open .dd-panel { display: block; }
  .dd.right .dd-panel { left: auto; right: 0; }
  .dd-toolbar { display: flex; gap: 4px; padding: 4px; border-bottom: 1px solid var(--border);
    margin-bottom: 4px; }
  .dd-btn-toolbar { padding: 5px 10px; font-size: 11px; border: none; background: transparent;
    color: var(--primary); border-radius: 6px; cursor: pointer; font-weight: 500; }
  .dd-btn-toolbar:hover { background: var(--primary-bg); }
  .dd-btn-toolbar.done { margin-left: auto; color: var(--text); font-weight: 600; }
  .dd-item { padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 13px;
    display: flex; align-items: center; gap: 8px; user-select: none; min-height: 38px; }
  .dd-item:hover { background: var(--card-hover); }
  .dd-item.checked { background: var(--primary-bg); color: var(--primary-text); }
  .dd-item .check { width: 16px; height: 16px; border-radius: 4px; border: 1.5px solid var(--border-hover);
    flex-shrink: 0; display: flex; align-items: center; justify-content: center; transition: all 0.1s; }
  .dd-item.checked .check { background: var(--primary); border-color: var(--primary); }
  .dd-item.checked .check::after { content: "✓"; color: white; font-size: 11px; font-weight: 700; line-height: 1; }
  .dd-item .arrow-r { margin-left: auto; color: var(--text-faint); font-size: 11px; transition: transform 0.15s; }
  .dd-item.exp .arrow-r { transform: rotate(90deg); }
  .dd-children { padding-left: 22px; padding-bottom: 4px; }
  .dd-child { padding: 7px 10px; border-radius: 6px; cursor: pointer; font-size: 12.5px;
    display: flex; align-items: center; gap: 8px; min-height: 34px; }
  .dd-child:hover { background: var(--card-hover); }
  .dd-child.checked { background: var(--primary-bg); }
  .dd-child .check { width: 14px; height: 14px; border-radius: 3px; border: 1.5px solid var(--border-hover);
    flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
  .dd-child.checked .check { background: var(--primary); border-color: var(--primary); }
  .dd-child.checked .check::after { content: "✓"; color: white; font-size: 9px; font-weight: 700; }
  .dd-child .self { background: var(--rose); color: white; padding: 1px 6px;
    border-radius: 4px; font-size: 10px; font-weight: 700; margin-left: 4px; }
  .dd-child .subs { margin-left: auto; font-size: 11px; color: var(--text-faint); font-family: var(--font-mono); }

  /* Selected chips */
  .selected-bar { display: flex; gap: 6px; flex-wrap: wrap; padding: 4px 0 8px; align-items: center; }
  .selected-bar .label { font-size: 11px; color: var(--text-faint); margin-right: 4px;
    text-transform: uppercase; letter-spacing: 0.04em; }
  .chip { padding: 4px 10px; border-radius: 12px; font-size: 12px;
    display: inline-flex; align-items: center; gap: 5px; background: var(--card);
    border: 1px solid var(--border); color: var(--text); }
  .chip-x { cursor: pointer; opacity: 0.5; padding: 0 2px; font-size: 11px; }
  .chip-x:hover { opacity: 1; color: var(--down); }
  .chip-impact { color: var(--text-faint); font-size: 11px; font-family: var(--font-mono); }
  .chip-clear { background: transparent; border: 1px solid var(--down); color: var(--down);
    cursor: pointer; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; }
  .chip-relax { background: var(--primary-bg); color: var(--primary-text); border: 1px solid var(--primary);
    cursor: pointer; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }

  .empty-banner { background: var(--card); border: 1px solid var(--warn); border-radius: 10px;
    padding: 16px; margin: 16px 0; }
  .empty-banner .title { color: var(--warn); font-weight: 600; margin-bottom: 8px; font-size: 13px; }
  .empty-banner .suggest { display: flex; flex-direction: column; gap: 6px; }
  .empty-banner .suggest button { background: var(--card-hover); border: 1px solid var(--border-hover);
    color: var(--text); padding: 8px 12px; border-radius: 8px; text-align: left; font-size: 12px;
    cursor: pointer; transition: border-color 0.15s; }
  .empty-banner .suggest button:hover { border-color: var(--primary); }

  /* Sort + buttons */
  .btn { padding: 9px 14px; border: 1px solid var(--border); border-radius: 8px;
    background: var(--card); color: var(--text); font-size: 13px;
    display: inline-flex; align-items: center; gap: 6px; min-height: 38px; transition: all 0.15s; }
  .btn:hover { background: var(--card-hover); border-color: var(--border-hover); }
  .btn-primary { background: var(--primary); color: white; border-color: var(--primary); }
  .btn-primary:hover { background: #5557E0; }
  .btn-danger { color: var(--down); border-color: var(--border); }
  .btn-danger:hover { border-color: var(--down); }

  /* Main */
  main { max-width: 1440px; margin: 0 auto; padding: 20px 28px 100px; }

  /* Multi-channel compare */
  .compare-board { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px; margin-bottom: 20px; }
  .ccard { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 16px; position: relative; transition: border-color 0.15s; cursor: pointer; }
  .ccard:hover { border-color: var(--primary); }
  .ccard.is-self { border-color: var(--rose); }
  .ccard .head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .ccard .head .name { font-weight: 600; font-size: 14px; }
  .ccard .self-tag { background: var(--rose-bg); color: var(--rose-text); padding: 1px 7px;
    border-radius: 4px; font-size: 10px; font-weight: 700; border: 1px solid var(--rose); }
  .ccard .subs { color: var(--text-faint); font-size: 11.5px; font-family: var(--font-mono); margin-bottom: 10px; }
  .ccard .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
  .ccard .cell { color: var(--text-faint); font-size: 11px; }
  .ccard .cell b { display: block; font-family: var(--font-mono); font-size: 17px;
    color: var(--text); font-weight: 600; line-height: 1.2; margin-top: 2px; }
  .ccard .cell .rank { font-size: 12px; margin-left: 4px; }
  .ccard .score-row { display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--text-faint); }
  .ccard .score-bar { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
  .ccard .score-bar > span { display: block; height: 100%; background: var(--primary); }
  .ccard .score-num { font-family: var(--font-mono); font-weight: 600; color: var(--text); }
  .ccard .close { position: absolute; top: 8px; right: 8px; width: 24px; height: 24px; border-radius: 12px;
    background: var(--card-hover); border: none; color: var(--text-faint); cursor: pointer;
    display: flex; align-items: center; justify-content: center; font-size: 12px; }
  .ccard .close:hover { color: var(--down); }

  /* Bulk mode */
  .bulk-bar { background: var(--card); border: 1px solid var(--primary); border-radius: 10px;
    padding: 10px 14px; margin-bottom: 14px; display: flex; align-items: center; gap: 10px;
    flex-wrap: wrap; }
  .bulk-bar .selected-count { color: var(--primary-text); font-weight: 600; }

  /* Grid */
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 18px; }
  .grid.list-view { grid-template-columns: 1fr; gap: 8px; }
  .grid.inspire-view { grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 24px; }

  .empty { text-align: center; color: var(--text-muted); padding: 80px 0; font-size: 14px; grid-column: 1/-1; }

  /* Video Card */
  .video-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    overflow: hidden; box-shadow: var(--shadow); display: flex; flex-direction: column;
    transition: all 0.2s ease; position: relative; }
  .video-card:hover { transform: translateY(-2px); border-color: var(--border-hover); }
  .video-card.is-self { border-color: var(--rose); }
  .video-card.hot-million { border-color: rgba(239,68,68,0.5); }
  .video-card.hot-phenom { border-color: var(--purple); box-shadow: 0 0 0 1px rgba(168,85,247,0.3), var(--shadow); }
  .video-card .bulk-cb { position: absolute; left: 12px; top: 12px; z-index: 3;
    width: 24px; height: 24px; background: rgba(10,14,26,0.85); backdrop-filter: blur(6px);
    border: 2px solid var(--primary); border-radius: 6px; display: none;
    align-items: center; justify-content: center; cursor: pointer; color: white; font-weight: 700; }
  .video-card.bulk-mode .bulk-cb { display: flex; }
  .video-card.bulk-selected .bulk-cb { background: var(--primary); }
  .thumb-wrap { position: relative; aspect-ratio: 16/9; background: #000; }
  .thumb-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .duration { position: absolute; right: 8px; bottom: 8px; background: rgba(0,0,0,0.85);
    color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600;
    font-family: var(--font-mono); }
  .badges { position: absolute; left: 10px; top: 10px; display: flex; flex-direction: column; gap: 4px; }
  .hot-chip { display: inline-flex; align-items: center; gap: 4px; padding: 3px 9px;
    border-radius: 10px; font-size: 11px; font-weight: 600; border: 1px solid;
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
  .hot-chip.rising { background: rgba(239,68,68,0.85); color: white; border-color: rgba(239,68,68,0.4); }
  .hot-chip.strong { background: rgba(245,158,11,0.85); color: white; border-color: rgba(245,158,11,0.4); }
  .hot-chip.million { background: rgba(239,68,68,0.85); color: white; border-color: rgba(239,68,68,0.4); }
  .hot-chip.phenom { background: rgba(168,85,247,0.85); color: white; border-color: rgba(168,85,247,0.4); }

  .fav-btn { position: absolute; top: 10px; right: 10px; z-index: 2;
    width: 38px; height: 38px; min-width: 38px; min-height: 38px; border-radius: 19px;
    background: rgba(10,14,26,0.85); backdrop-filter: blur(8px); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    color: var(--text-muted); transition: all 0.15s; }
  .fav-btn:hover { color: var(--warn); transform: scale(1.06); border-color: var(--warn); }
  .fav-btn.active { color: var(--warn); background: rgba(245,158,11,0.2); border-color: var(--warn); }
  .hide-btn { position: absolute; top: 10px; right: 56px; z-index: 2;
    width: 32px; height: 32px; min-width: 32px; min-height: 32px; border-radius: 16px;
    background: rgba(10,14,26,0.85); backdrop-filter: blur(8px); border: 1px solid var(--border);
    color: var(--text-faint); font-size: 14px; opacity: 0; transition: opacity 0.15s; display: flex;
    align-items: center; justify-content: center; }
  .video-card:hover .hide-btn { opacity: 1; }

  .card-body { padding: 14px; flex: 1; display: flex; flex-direction: column; gap: 8px; }
  .card-row1 { display: flex; align-items: center; gap: 6px; font-size: 12px;
    color: var(--text-muted); flex-wrap: wrap; }
  .card-row1 .channel-name { color: var(--text); font-weight: 500; }
  .card-row1 .grp { padding: 1px 7px; border-radius: 5px; background: var(--gray-bg);
    color: var(--gray-text); font-size: 10.5px; font-weight: 500; }
  .card-row1 .self { padding: 1px 7px; border-radius: 5px; background: var(--rose-bg);
    color: var(--rose-text); font-size: 10.5px; font-weight: 700; border: 1px solid var(--rose);
    display: inline-flex; align-items: center; gap: 3px; }
  .card-row1 .vtype { padding: 1px 7px; border-radius: 5px; background: var(--card-hover);
    color: var(--text-muted); font-size: 10.5px; }

  .card-title { color: var(--text); font-size: 15px; font-weight: 600; line-height: 1.4;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical; display: -webkit-box; overflow: hidden;
    min-height: 42px; letter-spacing: -0.01em; }
  .card-title:hover { color: var(--primary-text); }

  /* Business signal */
  .biz-signal { display: flex; align-items: baseline; gap: 8px; padding: 8px 0;
    border-top: 1px dashed var(--border); }
  .biz-signal .er-num { font-size: 26px; font-weight: 700; font-family: var(--font-mono); line-height: 1; letter-spacing: -0.02em; }
  .biz-signal .er-label { font-size: 11px; color: var(--text-faint); cursor: help;
    border-bottom: 1px dotted var(--text-faint); }
  .biz-signal .deltas { margin-left: auto; display: flex; gap: 8px; font-size: 11px; color: var(--text-faint); font-family: var(--font-mono); }
  .biz-signal .deltas .delta { display: inline-flex; align-items: center; gap: 2px; }
  .biz-signal .deltas .delta.pos { color: var(--up); }
  .biz-signal .deltas .delta.neg { color: var(--down); }

  .card-stats { display: flex; gap: 12px; align-items: center; font-size: 12px;
    color: var(--text-muted); }
  .card-stats .item { display: inline-flex; align-items: center; gap: 5px; }
  .card-stats .num { color: var(--text); font-family: var(--font-mono); font-weight: 500; font-size: 13px; }

  .tag-row { display: flex; flex-wrap: wrap; gap: 4px; }
  .tag-c { padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 500; border: 1px solid; }
  .tag-c.iPad { background: var(--red-bg); color: var(--red-text); border-color: rgba(239,68,68,0.3); }
  .tag-c.create { background: var(--purple-bg); color: var(--purple-text); border-color: rgba(168,85,247,0.3); }
  .tag-c.student { background: var(--primary-bg); color: var(--primary-text); border-color: rgba(99,102,241,0.3); }
  .tag-c.business { background: var(--green-bg); color: var(--green-text); border-color: rgba(16,185,129,0.3); }
  .tag-c.apple { background: var(--gray-bg); color: var(--gray-text); border-color: rgba(148,163,184,0.3); }
  .tag-c.brand { background: var(--primary-bg); color: var(--primary-text); border-color: rgba(99,102,241,0.4); font-weight: 600; }
  .tag-c.kol { background: var(--orange-bg); color: var(--orange-text); border-color: rgba(245,158,11,0.4); font-weight: 700; }
  .tag-c.rising { background: var(--orange-bg); color: var(--orange-text); border-color: rgba(245,158,11,0.4); }
  .tag-c.seo { background: var(--green-bg); color: var(--green-text); border-color: rgba(16,185,129,0.3); }

  .meta-bottom { display: flex; align-items: center; justify-content: space-between;
    font-size: 11px; color: var(--text-faint); padding-top: 4px; }

  /* Brand compare table */
  .panel { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 24px; margin-bottom: 18px; }
  .panel h3 { margin: 0 0 14px; font-size: 16px; font-weight: 600; }
  .panel table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .panel th { text-align: left; padding: 10px 14px; color: var(--text-muted);
    font-weight: 500; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em;
    border-bottom: 1px solid var(--border); }
  .panel td { padding: 12px 14px; border-bottom: 1px solid var(--border); font-family: var(--font-mono); font-size: 13.5px; }
  .panel td.name { font-family: var(--font-sans); font-weight: 600; font-size: 14px; }
  .panel tr:last-child td { border-bottom: none; }
  .bar { height: 6px; background: var(--border); border-radius: 3px; overflow: hidden;
    min-width: 100px; max-width: 240px; display: inline-block; vertical-align: middle; margin-left: 8px; }
  .bar > span { display: block; height: 100%; background: var(--primary); }

  /* History */
  .history-empty { padding: 40px 0; text-align: center; color: var(--text-muted); }
  .history-empty .big { font-size: 16px; color: var(--text); margin-bottom: 8px; font-weight: 500; }
  .progress { height: 6px; background: var(--border); border-radius: 3px; overflow: hidden;
    max-width: 320px; margin: 14px auto; }
  .progress > span { display: block; height: 100%; background: var(--primary); }

  /* Tooltip */
  [data-tip] { position: relative; }
  [data-tip]:hover::after { content: attr(data-tip); position: absolute; bottom: 100%; left: 50%;
    transform: translateX(-50%) translateY(-6px); background: var(--card-hover); color: var(--text);
    padding: 6px 10px; border-radius: 6px; font-size: 11.5px; white-space: nowrap;
    box-shadow: var(--shadow); z-index: 999; border: 1px solid var(--border); pointer-events: none; }

  /* Workflow banner (favorites) */
  .workflow-banner { background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(168,85,247,0.05));
    border: 1px solid rgba(99,102,241,0.3); border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;
    position: relative; }
  .workflow-banner h4 { margin: 0 0 6px; font-size: 13px; font-weight: 600; }
  .workflow-banner ol { margin: 0; padding-left: 20px; color: var(--text-muted); font-size: 12px; }
  .workflow-banner ol li { margin: 2px 0; }
  .workflow-banner .close-x { position: absolute; top: 8px; right: 8px; cursor: pointer;
    color: var(--text-faint); padding: 4px 8px; }

  /* Toast */
  .toast { position: fixed; right: 20px; bottom: 80px; z-index: 300;
    background: var(--card-hover); color: var(--text); padding: 12px 18px; border-radius: 12px;
    font-size: 13px; font-weight: 500; box-shadow: var(--shadow-lg); border: 1px solid var(--border-hover);
    transform: translateY(80px); opacity: 0; transition: all 0.25s; max-width: 360px; }
  .toast.show { transform: translateY(0); opacity: 1; }

  /* Mobile */
  .mobile-bar { display: none; }
  .mobile-overlay { display: none; }
  .mobile-drawer { display: none; }
  .mobile-summary { display: none; }

  @media (max-width: 1280px) {
    .kpi-grid { grid-template-columns: repeat(3, 1fr); }
    .charts { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 768px) {
    .container { padding: 14px 16px; }
    main { padding: 16px 16px 100px; }
    .hero h1 { font-size: 17px; }
    .hero .subtitle { font-size: 12px; }
    .meta-line { font-size: 11px; gap: 8px; }
    .kpi-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
    .kpi-card { padding: 12px; min-height: 90px; }
    .kpi-card .big { font-size: 24px; }
    .kpi-card .label { font-size: 10.5px; }
    .charts { grid-template-columns: 1fr; }
    .filter-bar.desktop { display: none; }
    .filter-bar.mobile-summary { display: flex; }
    .selected-bar { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; padding-bottom: 4px; }
    .selected-bar::-webkit-scrollbar { display: none; }
    .selected-bar .chip { flex-shrink: 0; }
    .grid { grid-template-columns: 1fr; gap: 14px; }
    .compare-board { grid-template-columns: 1fr 1fr; }
    .stat-row { font-size: 11.5px; padding: 10px 0; }
    .preset-btn { padding: 8px 12px; font-size: 12px; min-height: 40px; }
    .tabs { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
    .tab { flex-shrink: 0; }
    .insight { padding: 12px; }
    .insight ul { font-size: 12px; }

    .card-title { font-size: 14.5px; min-height: 40px; }
    .biz-signal .er-num { font-size: 22px; }

    .mobile-bar { display: flex; position: fixed; bottom: 0; left: 0; right: 0;
      background: rgba(10,14,26,0.96); backdrop-filter: saturate(180%) blur(20px);
      -webkit-backdrop-filter: saturate(180%) blur(20px);
      border-top: 1px solid var(--border); padding: 8px 12px;
      padding-bottom: calc(8px + env(safe-area-inset-bottom));
      z-index: 99; gap: 6px; }
    .mobile-bar .btn { flex: 1; min-height: 44px; justify-content: center; font-size: 12.5px; padding: 6px 8px; }
    .mobile-bar .count-badge { background: var(--primary); color: white; padding: 1px 6px;
      border-radius: 9px; font-size: 10px; font-weight: 700; margin-left: 4px; }

    .mobile-overlay { display: block; position: fixed; inset: 0; background: rgba(0,0,0,0.6);
      z-index: 200; opacity: 0; pointer-events: none; transition: opacity 0.2s; }
    .mobile-overlay.show { opacity: 1; pointer-events: auto; }
    .mobile-drawer { display: flex; flex-direction: column; position: fixed;
      bottom: 0; left: 0; right: 0; max-height: 78vh;
      background: var(--card); border-radius: 16px 16px 0 0; box-shadow: 0 -10px 30px rgba(0,0,0,0.5);
      transform: translateY(100%); transition: transform 0.3s ease; z-index: 201;
      padding-bottom: env(safe-area-inset-bottom); border: 1px solid var(--border); border-bottom: none; }
    .mobile-drawer.show { transform: translateY(0); }
    .mobile-drawer .handle { padding: 12px; text-align: center; flex-shrink: 0; }
    .mobile-drawer .handle::before { content: ''; display: inline-block; width: 36px; height: 4px;
      border-radius: 2px; background: var(--border-hover); }
    .mobile-drawer-title { padding: 0 20px; font-size: 17px; font-weight: 700; flex-shrink: 0;
      display: flex; justify-content: space-between; align-items: center; }
    .mobile-drawer-title button { background: none; border: none; color: var(--text-muted); padding: 8px; }
    .mobile-drawer-content { flex: 1; overflow-y: auto; padding: 16px 20px; }
    .mobile-drawer-content .label { font-size: 11px; color: var(--text-muted); margin: 14px 0 6px;
      text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
    .mobile-drawer-content .label:first-child { margin-top: 0; }
    .mobile-drawer-content .dd { width: 100%; }
    .mobile-drawer-content .dd-btn { width: 100%; justify-content: space-between; min-height: 44px; }
    .mobile-drawer-content .dd.open .dd-panel { position: static; box-shadow: none;
      border: 1px solid var(--border); margin-top: 6px; max-height: 280px; }
    .mobile-drawer-actions { padding: 12px 16px; border-top: 1px solid var(--border);
      display: flex; gap: 8px; flex-shrink: 0; background: var(--card); }
    .mobile-drawer-actions .btn { flex: 1; min-height: 46px; font-weight: 600; justify-content: center; }

    .toast { right: 16px; left: 16px; bottom: 80px; text-align: center; }
  }
</style>
</head>
<body>
<header>
  <div class="container">
    <div class="hero">
      <h1>📺 YouTube 北美 iPad 配件内容情报</h1>
      <div class="subtitle">56 频道 · 8 维度数据 · 每日更新</div>
      <div class="meta-line">
        <span><span class="live-dot"></span>自动刷新已开</span>
        <span>数据版本 <b id="gen-at">—</b> <span id="gen-ago"></span></span>
        <span>频道 <b id="ch-count">—</b></span>
        <span>视频 <b id="vid-count">—</b></span>
      </div>
    </div>

    <nav class="tabs" id="tabs"></nav>

    <div id="kpi-grid" class="kpi-grid"></div>

    <div id="insight" class="insight" style="display:none"></div>

    <div id="stat-row" class="stat-row"></div>

    <div id="presets" class="presets"></div>

    <div class="filter-bar desktop" id="desktop-filters"></div>
    <div class="filter-bar mobile-summary"></div>

    <div class="selected-bar" id="selected-chips"></div>
  </div>
</header>

<main>
  <div id="view-home"></div>
  <div id="view-favorites" style="display:none"></div>
  <div id="view-brand" style="display:none"></div>
  <div id="view-history" style="display:none"></div>
  <div id="view-monitor" style="display:none"></div>
</main>

<!-- Mobile bottom bar -->
<div class="mobile-bar">
  <button class="btn" id="mb-filter">筛选 <span class="count-badge" id="mb-filter-count" style="display:none">0</span></button>
  <button class="btn" id="mb-sort">排序 · <span id="mb-sort-label">ER↓</span></button>
  <button class="btn" id="mb-fav">⭐ <span class="count-badge" id="mb-fav-count" style="display:none">0</span></button>
</div>

<!-- Mobile drawer -->
<div class="mobile-overlay" id="mb-overlay"></div>
<div class="mobile-drawer" id="mb-drawer">
  <div class="handle"></div>
  <div class="mobile-drawer-title"><span>筛选</span><button id="mb-drawer-close">✕</button></div>
  <div class="mobile-drawer-content" id="mb-drawer-content"></div>
  <div class="mobile-drawer-actions">
    <button class="btn" id="mb-drawer-reset">重置</button>
    <button class="btn btn-primary" id="mb-drawer-apply">应用</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const CFG = __CFG__;
const POLL_INTERVAL_MS = 60 * 1000;
const STORAGE_KEY = 'yt-tracker-v4';
const FAV_KEY = 'yt-tracker-favorites-v4';
const HIDE_KEY = 'yt-tracker-hidden-v4';
const TEARDOWN_KEY = 'yt-tracker-teardown-v4';

let DATA = null;
let HISTORY = null;
let state = loadState();
let pendingMobileState = null;
let bulkMode = false;
let bulkSelected = new Set();

// ========== State ==========
function defaultFilters() {
  return { time: 'all', groups: [], channels: [], contents: [], lengths: [], hots: [], vtypes: [], brands: [] };
}
function defaultState() {
  return { tab: 'home', filters: defaultFilters(), sort: 'er', expanded_groups: [], view_mode: 'grid', preset: '', workflow_banner_dismissed: false };
}
function loadState() { try { return Object.assign(defaultState(), JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')); } catch (e) { return defaultState(); } }
function saveState() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function getFavs() { try { return JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); } catch { return []; } }
function setFavs(arr) { localStorage.setItem(FAV_KEY, JSON.stringify(arr)); }
function getHidden() { try { return JSON.parse(localStorage.getItem(HIDE_KEY) || '[]'); } catch { return []; } }
function setHidden(arr) { localStorage.setItem(HIDE_KEY, JSON.stringify(arr)); }
function getTeardownData() { try { return JSON.parse(localStorage.getItem(TEARDOWN_KEY) || '{}'); } catch { return {}; } }
function setTeardownData(d) { localStorage.setItem(TEARDOWN_KEY, JSON.stringify(d)); }

// ========== Util ==========
function fmt(n) {
  if (n == null) return '—';
  if (n >= 1e7) return (n/1e6).toFixed(1) + 'M';
  if (n >= 1e6) return (n/1e6).toFixed(2) + 'M';
  if (n >= 1e3) return (n/1e3).toFixed(1) + 'K';
  return String(n);
}
function fmtPct(n, d=2) { return (n||0).toFixed(d) + '%'; }
function fmtDate(iso) {
  const d = new Date(iso);
  const diffH = Math.floor((Date.now() - d) / 3600000);
  if (diffH < 1) return Math.max(0, Math.floor((Date.now()-d)/60000)) + ' 分钟前';
  if (diffH < 24) return diffH + ' 小时前';
  const dd = Math.floor(diffH/24);
  if (dd === 1) return '昨天';
  if (dd < 7) return dd + ' 天前';
  if (dd < 30) return Math.floor(dd/7) + ' 周前';
  if (dd < 365) return Math.floor(dd/30) + ' 个月前';
  return d.toISOString().slice(0,10);
}
function fmtAgo(iso) {
  const d = new Date((iso||'').replace(' ', 'T'));
  const sec = Math.floor((Date.now() - d.getTime())/1000);
  if (sec < 60) return '(' + sec + ' 秒前)';
  if (sec < 3600) return '(' + Math.floor(sec/60) + ' 分钟前)';
  if (sec < 86400) return '(' + Math.floor(sec/3600) + ' 小时前)';
  return '(' + Math.floor(sec/86400) + ' 天前)';
}
function escHTML(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
function withinTime(iso, key) {
  if (key === 'all') return true;
  const days = parseFloat(key);
  if (!isFinite(days) || days <= 0) return true;
  const t = new Date(iso).getTime();
  if (!isFinite(t)) return true;
  return (Date.now() - t) <= days * 86400000;
}
function isMobile() { return window.matchMedia('(max-width: 768px)').matches; }

const ICONS = {
  play: '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
  thumb: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 22V11M2 13h5v9H4a2 2 0 01-2-2v-7zM7 11l5-9 1 1c.6.5.9 1.3.9 2v3h6a2 2 0 012 2l-2 7a2 2 0 01-2 2h-7"/></svg>',
  comment: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
  star_o: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2l2.4 7h7.6l-6.2 4.5L18.2 21 12 16.5 5.8 21l2.4-7.5L2 9h7.6z"/></svg>',
  star: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 7h7.6l-6.2 4.5L18.2 21 12 16.5 5.8 21l2.4-7.5L2 9h7.6z"/></svg>',
  download: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v12m0 0l-5-5m5 5l5-5M4 20h16"/></svg>',
  filter: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
  chevron: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="6 9 12 15 18 9"/></svg>',
};

// ========== Data ==========
async function fetchData() {
  const r = await fetch('data/channels_data.json?t=' + Date.now(), { cache: 'no-store' });
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return await r.json();
}
async function fetchHistoryIndex() {
  try { const r = await fetch('data/history/index.json?t=' + Date.now(), { cache: 'no-store' }); return r.ok ? await r.json() : null; } catch { return null; }
}

// ========== Channel meta ==========
function brandMentionOptions() {
  const set = new Set();
  if (DATA) DATA.videos.forEach(v => (v.brand_mentions||[]).forEach(b => set.add(b)));
  return Array.from(set).sort();
}
function channelAvgER(name) {
  if (!DATA) return 0;
  const vs = DATA.videos.filter(v => v.channel_name === name);
  if (!vs.length) return 0;
  return vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length;
}
function groupAvgER(group) {
  if (!DATA) return 0;
  const vs = DATA.videos.filter(v => v.channel_group === group);
  if (!vs.length) return 0;
  return vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length;
}

// ========== Filters ==========
function applyFilters(videos, opts={}) {
  const f = opts.filters || state.filters;
  const skipHidden = opts.skipHidden;
  const hidden = new Set(getHidden());
  return videos.filter(v => {
    if (!skipHidden && hidden.has(v.video_id)) return false;
    if (!withinTime(v.published_at, f.time)) return false;
    if (f.channels.length || f.groups.length) {
      const chMatch = f.channels.includes(v.channel_name);
      const grpMatch = f.groups.includes(v.channel_group);
      if (!(chMatch || grpMatch)) return false;
    }
    if (f.contents.length) {
      const tags = v.content_tags || [];
      if (!f.contents.some(c => tags.includes(c))) return false;
    }
    if (f.lengths.length && !f.lengths.includes(v.video_length_type)) return false;
    if (f.hots.length && !f.hots.includes(v.hot_level)) return false;
    if (f.vtypes.length && !f.vtypes.includes(v.video_type)) return false;
    if (f.brands.length) {
      const bms = v.brand_mentions || [];
      if (!f.brands.some(b => bms.includes(b))) return false;
    }
    return true;
  });
}
function applySort(videos, sort=state.sort) {
  const a = videos.slice();
  if (sort === 'er') a.sort((x,y) => (y.engagement_rate||0)-(x.engagement_rate||0));
  else if (sort === 'views') a.sort((x,y) => (y.view_count||0)-(x.view_count||0));
  else if (sort === 'comment_rate') a.sort((x,y) => (y.comment_rate||0)-(x.comment_rate||0));
  else if (sort === 'recent') a.sort((x,y) => new Date(y.published_at) - new Date(x.published_at));
  else if (sort === 'view_to_sub') a.sort((x,y) => (y.view_to_sub_ratio||0)-(x.view_to_sub_ratio||0));
  return a;
}

// 计算"移除某筛选后"会显示多少条
function countWithout(filterKey, value) {
  const f = JSON.parse(JSON.stringify(state.filters));
  if (Array.isArray(f[filterKey])) f[filterKey] = f[filterKey].filter(x => x !== value);
  else f[filterKey] = 'all';
  return applyFilters(DATA.videos, { filters: f }).length;
}
function activeFilterCount() {
  const f = state.filters;
  return (f.time !== 'all' ? 1 : 0) + f.groups.length + f.channels.length + f.contents.length + f.lengths.length + f.hots.length + f.vtypes.length + f.brands.length;
}

// ========== Custom Dropdown (多选不自动关) ==========
function makeDropdown({ label, options, multi, getSelected, onChange, alignRight=false }) {
  const wrap = document.createElement('span');
  wrap.className = 'dd' + (alignRight ? ' right' : '');
  wrap.innerHTML = '<button class="dd-btn"></button><div class="dd-panel"></div>';
  const btn = wrap.querySelector('.dd-btn');
  const panel = wrap.querySelector('.dd-panel');

  function selValue() { const s = getSelected(); return Array.isArray(s) ? s : [s]; }
  function refreshBtn() {
    const sel = selValue();
    let txt = label;
    if (multi) {
      if (sel.length > 0) txt += ' <span class="count">(' + sel.length + ')</span>';
    } else {
      const o = options.find(o => (o.value||o) === sel[0]);
      if (o && (o.value||o) !== options[0]?.value && (o.value||o) !== options[0]) {
        txt += ': <span class="count">' + (o.label||o) + '</span>';
      } else if (o) {
        txt += ': ' + (o.label||o);
      }
    }
    btn.innerHTML = txt + ' <span class="arrow">' + ICONS.chevron + '</span>';
  }
  function refreshItems() {
    const sel = selValue();
    panel.innerHTML = '';
    if (multi) {
      const tb = document.createElement('div');
      tb.className = 'dd-toolbar';
      tb.innerHTML = '<button class="dd-btn-toolbar" data-act="all">全选</button><button class="dd-btn-toolbar" data-act="clear">清空</button><button class="dd-btn-toolbar done" data-act="done">完成</button>';
      tb.onclick = e => {
        const act = e.target.dataset.act;
        if (act === 'all') { onChange(options.map(o => o.value||o)); refreshItems(); refreshBtn(); }
        else if (act === 'clear') { onChange([]); refreshItems(); refreshBtn(); }
        else if (act === 'done') { wrap.classList.remove('open'); }
      };
      panel.appendChild(tb);
    }
    options.forEach(opt => {
      const v = opt.value || opt;
      const lbl = opt.label || opt;
      const checked = sel.includes(v);
      const item = document.createElement('div');
      item.className = 'dd-item' + (checked ? ' checked' : '');
      item.innerHTML = (multi ? '<span class="check"></span>' : '') + '<span>' + escHTML(lbl) + '</span>';
      item.onclick = (e) => {
        e.stopPropagation();
        if (multi) {
          const cur = selValue().slice();
          const i = cur.indexOf(v);
          if (i >= 0) cur.splice(i, 1); else cur.push(v);
          onChange(cur);
          refreshItems(); refreshBtn();
        } else {
          onChange(v);
          wrap.classList.remove('open');
          refreshBtn();
        }
      };
      panel.appendChild(item);
    });
  }
  btn.onclick = e => {
    e.stopPropagation();
    document.querySelectorAll('.dd.open').forEach(d => { if (d !== wrap) d.classList.remove('open'); });
    wrap.classList.toggle('open');
    if (wrap.classList.contains('open')) refreshItems();
  };
  refreshBtn();
  return { el: wrap, refresh: () => { refreshBtn(); if (wrap.classList.contains('open')) refreshItems(); } };
}

function makeChannelTreeDropdown({ getGroups, getChannels, onChangeGroups, onChangeChannels }) {
  const wrap = document.createElement('span');
  wrap.className = 'dd';
  wrap.innerHTML = '<button class="dd-btn"></button><div class="dd-panel"></div>';
  const btn = wrap.querySelector('.dd-btn');
  const panel = wrap.querySelector('.dd-panel');

  function refresh() {
    const sgArr = getGroups();
    const scArr = getChannels();
    const cnt = sgArr.length + scArr.length;
    btn.innerHTML = '频道分组' + (cnt ? ' <span class="count">(' + cnt + ')</span>' : '') + ' <span class="arrow">' + ICONS.chevron + '</span>';
    if (wrap.classList.contains('open')) renderItems();
  }
  function renderItems() {
    const sgArr = getGroups();
    const scArr = getChannels();
    panel.innerHTML = '';
    const tb = document.createElement('div');
    tb.className = 'dd-toolbar';
    tb.innerHTML = '<span style="font-size:11px;color:var(--text-faint);padding:6px 10px">点大类=选整组 / 点 ▸ 展开看子频道</span><button class="dd-btn-toolbar done" data-act="done">完成</button>';
    tb.querySelector('[data-act=done]').onclick = () => { wrap.classList.remove('open'); };
    panel.appendChild(tb);

    Object.entries(CFG.group_labels).forEach(([gKey, gLabel]) => {
      const isChecked = sgArr.includes(gKey);
      const isExp = state.expanded_groups.includes(gKey);
      const item = document.createElement('div');
      item.className = 'dd-item' + (isChecked ? ' checked' : '') + (isExp ? ' exp' : '');
      item.innerHTML = '<span class="check"></span><span style="font-weight:500">' + escHTML(gLabel) + '</span><span class="arrow-r">▸</span>';
      item.onclick = (e) => {
        e.stopPropagation();
        const isArrow = e.target.classList.contains('arrow-r');
        if (isArrow) {
          const cur = state.expanded_groups.slice();
          const i = cur.indexOf(gKey);
          if (i >= 0) cur.splice(i, 1); else cur.push(gKey);
          state.expanded_groups = cur; saveState();
        } else {
          const cur = sgArr.slice();
          const i = cur.indexOf(gKey);
          if (i >= 0) cur.splice(i, 1); else cur.push(gKey);
          onChangeGroups(cur);
        }
        renderItems(); refresh();
      };
      panel.appendChild(item);

      if (isExp) {
        const cw = document.createElement('div');
        cw.className = 'dd-children';
        (CFG.channel_tree[gKey]||[]).forEach(ch => {
          const cn = ch.display_name;
          const checked = scArr.includes(cn);
          const c = document.createElement('div');
          c.className = 'dd-child' + (checked ? ' checked' : '');
          c.innerHTML = '<span class="check"></span><span>' + escHTML(cn) + '</span>'
            + (ch.is_self ? '<span class="self">⭐ 自家</span>' : '')
            + '<span class="subs">' + fmt(ch.subscriber_count) + '</span>';
          c.onclick = (e) => {
            e.stopPropagation();
            const cur = scArr.slice();
            const i = cur.indexOf(cn);
            if (i >= 0) cur.splice(i, 1); else cur.push(cn);
            onChangeChannels(cur);
            renderItems(); refresh();
          };
          cw.appendChild(c);
        });
        panel.appendChild(cw);
      }
    });
  }
  btn.onclick = e => {
    e.stopPropagation();
    document.querySelectorAll('.dd.open').forEach(d => { if (d !== wrap) d.classList.remove('open'); });
    wrap.classList.toggle('open');
    if (wrap.classList.contains('open')) renderItems();
  };
  refresh();
  return { el: wrap, refresh };
}

document.addEventListener('click', e => {
  if (!e.target.closest('.dd')) {
    document.querySelectorAll('.dd.open').forEach(d => d.classList.remove('open'));
  }
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelectorAll('.dd.open').forEach(d => d.classList.remove('open'));
});

// ========== Tabs ==========
function renderTabs() {
  const favCount = getFavs().length;
  const items = [
    { key: 'home', label: '首页' },
    { key: 'favorites', label: '拆解清单', badge: favCount > 0 ? favCount : null },
    { key: 'brand', label: '品牌对比' },
    { key: 'history', label: '历史趋势' },
    { key: 'monitor', label: '竞品监测' },
  ];
  document.getElementById('tabs').innerHTML = items.map(t =>
    `<button class="tab${t.key === state.tab ? ' active' : ''}" data-tab="${t.key}">${t.label}${t.badge != null ? '<span class="tab-badge">' + t.badge + '</span>' : ''}</button>`
  ).join('');
  document.querySelectorAll('.tab').forEach(b => b.onclick = () => {
    state.tab = b.dataset.tab; saveState(); render();
  });
}

// ========== KPI ==========
function makeSparkline(values, color) {
  if (!values || values.length < 2) return '';
  const max = Math.max(...values, 1);
  const min = Math.min(...values, 0);
  const range = max - min || 1;
  const w = 80, h = 20;
  const step = w / (values.length - 1);
  const points = values.map((v, i) => `${(i*step).toFixed(1)},${(h - ((v-min)/range)*h).toFixed(1)}`).join(' ');
  return `<svg class="sparkline" width="${w}" height="${h}"><polyline points="${points}" fill="none" stroke="${color}" stroke-width="1.5"/></svg>`;
}

function renderKPI(filtered) {
  const root = document.getElementById('kpi-grid');
  const total = filtered.reduce((s,v) => s + (v.view_count||0), 0);
  const avgER = filtered.length ? filtered.reduce((s,v) => s + (v.engagement_rate||0), 0) / filtered.length : 0;
  const highER = filtered.filter(v => (v.engagement_rate||0) >= 5).length;
  const week = filtered.filter(v => withinTime(v.published_at, '7'));
  const week100k = week.filter(v => v.view_count >= 1e5).length;
  const phenom = filtered.filter(v => v.hot_level === '🚀 现象级').length;

  const erColor = avgER >= 5 ? 'green' : '';
  root.innerHTML = `
    <div class="kpi-card"><div class="label">视频数</div><div class="big">${filtered.length}</div><div class="sub">已显示</div></div>
    <div class="kpi-card"><div class="label">总播放</div><div class="big">${fmt(total)}</div><div class="sub">累计</div></div>
    <div class="kpi-card" data-tip="Engagement Rate · 互动率 · (赞+评论)/播放 · >5% 优秀 / 2-5% 一般 / <2% 较差">
      <div class="label">平均 ER</div><div class="big ${erColor}">${avgER.toFixed(2)}<span style="font-size:14px;color:var(--text-muted);">%</span></div>
      <div class="sub">悬停看说明</div>
    </div>
    <div class="kpi-card"><div class="label">高 ER 内容</div><div class="big">${highER}</div><div class="sub">≥5% 互动率</div></div>
    <div class="kpi-card"><div class="label">本周新视频</div><div class="big">${week.length}</div><div class="sub">${week100k} 个 &gt;10万</div></div>
    <div class="kpi-card"><div class="label">现象级爆款</div><div class="big purple">${phenom}</div><div class="sub">&gt;500万播放</div></div>
  `;
}

// ========== Insight ==========
function generateInsights(filtered) {
  const insights = [];
  // 本周创作类 ER vs 总体平均
  const week = filtered.filter(v => withinTime(v.published_at, '7'));
  const allCreate = filtered.filter(v => (v.content_tags||[]).includes('创作'));
  if (allCreate.length) {
    const allER = allCreate.reduce((s,v) => s+(v.engagement_rate||0), 0) / allCreate.length;
    const weekCreate = week.filter(v => (v.content_tags||[]).includes('创作'));
    if (weekCreate.length >= 3) {
      const wER = weekCreate.reduce((s,v) => s+(v.engagement_rate||0), 0) / weekCreate.length;
      const diff = ((wER - allER) / Math.max(allER, 0.01) * 100);
      if (Math.abs(diff) >= 15) {
        insights.push(`创作类内容本周 ER ${diff > 0 ? '↑' : '↓'} ${Math.abs(diff).toFixed(0)}%（本周 ${wER.toFixed(2)}% vs 总体 ${allER.toFixed(2)}%）`);
      }
    }
  }
  // 竞品 A 组本周破百万
  const aWeek = week.filter(v => v.channel_group === 'A_brand' && v.view_count >= 1e6);
  if (aWeek.length) {
    aWeek.slice(0, 2).forEach(v => insights.push(`${v.channel_name} 本周新视频破百万：${v.title.slice(0, 40)}`));
  }
  // iPad 配件相关数量
  const ipadAcc = filtered.filter(v => (v.content_tags||[]).includes('iPad配件相关'));
  if (ipadAcc.length === 0) {
    insights.push('当前筛选下无 iPad 配件相关视频，建议放宽时间窗口或查看全部分组');
  } else if (ipadAcc.length <= 5) {
    insights.push(`iPad 配件相关视频仅 ${ipadAcc.length} 条，类目供给量低（蓝海机会）`);
  }
  // 头部 KOL 本周动态
  const kolWeek = week.filter(v => CFG.top_kol.includes(v.channel_name));
  if (kolWeek.length) {
    insights.push(`头部 KOL 本周共发布 ${kolWeek.length} 条视频（MKBHD/iJustine/LTT 等）`);
  }
  return insights;
}

function renderInsight(filtered) {
  const root = document.getElementById('insight');
  const insights = generateInsights(filtered);
  if (insights.length === 0 || !HISTORY || HISTORY.count < 2) {
    if (insights.length === 0 && HISTORY && HISTORY.count >= 2) { root.style.display = 'none'; return; }
    if (HISTORY && HISTORY.count < 7) {
      root.style.display = 'block';
      root.innerHTML = `<div class="title">📊 智能洞察</div><ul><li style="color:var(--text-faint)">洞察将在数据积累 7 天后开启（当前 ${HISTORY.count}/7 天）。先看下面的实时观察 ↓</li>${insights.map(i => '<li>' + escHTML(i) + '</li>').join('')}</ul>`;
      return;
    }
    if (insights.length === 0) { root.style.display = 'none'; return; }
  }
  root.style.display = 'block';
  root.innerHTML = `<div class="title">📊 本周观察</div><ul>${insights.map(i => '<li>' + escHTML(i) + '</li>').join('')}</ul>`;
}

// ========== Stat row ==========
function renderStatRow(filtered) {
  const root = document.getElementById('stat-row');
  const hot = (l) => filtered.filter(v => v.hot_level === l).length;
  const tag = (t) => filtered.filter(v => (v.content_tags||[]).includes(t)).length;
  const high_rel = filtered.filter(v => (v.relevance_score||0) >= 80).length;
  const mid_rel = filtered.filter(v => (v.relevance_score||0) >= 60 && (v.relevance_score||0) < 80).length;
  const low_rel = filtered.filter(v => (v.relevance_score||0) < 60).length;

  let html = '';
  if (hot('🔥 上升爆款') + hot('💥 强爆款') + hot('⭐ 百万爆款') + hot('🚀 现象级') > 0) {
    html += `<span class="label">爆款</span>`;
    if (hot('🔥 上升爆款')) html += `<span class="pill rising">🔥 上升 ${hot('🔥 上升爆款')}</span>`;
    if (hot('💥 强爆款'))   html += `<span class="pill strong">💥 强 ${hot('💥 强爆款')}</span>`;
    if (hot('⭐ 百万爆款')) html += `<span class="pill million">⭐ 百万 ${hot('⭐ 百万爆款')}</span>`;
    if (hot('🚀 现象级'))   html += `<span class="pill phenom">🚀 现象级 ${hot('🚀 现象级')}</span>`;
  }
  html += `<span class="label" style="margin-left:8px">相关性</span>`;
  html += `<span class="pill high-rel">🎯 高度相关 <b class="num">${high_rel}</b></span>`;
  html += `<span class="pill mid-rel">中等 <b class="num">${mid_rel}</b></span>`;
  html += `<span class="pill low-rel">低 <b class="num">${low_rel}</b></span>`;

  if (tag('iPad配件相关')) html += `<span class="pill tag-iPad">iPad配件 ${tag('iPad配件相关')}</span>`;
  if (tag('创作'))        html += `<span class="pill tag-creation">创作 ${tag('创作')}</span>`;
  if (tag('学生'))        html += `<span class="pill tag-student">学生 ${tag('学生')}</span>`;
  if (tag('商务'))        html += `<span class="pill tag-business">商务 ${tag('商务')}</span>`;
  root.innerHTML = html;
}

// ========== Charts ==========
function renderCharts(filtered) {
  let root = document.getElementById('charts-root');
  if (!root) {
    root = document.createElement('div');
    root.id = 'charts-root';
    root.className = 'charts';
    const home = document.getElementById('view-home');
    home.insertBefore(root, home.firstChild);
  }
  if (filtered.length === 0) { root.innerHTML = ''; return; }

  // Chart 1: 长度 × ER 散点
  const lenOrder = CFG.length_order;
  const w1 = 320, h1 = 200, pad = 30;
  const erMax = Math.max(...filtered.map(v => v.engagement_rate||0), 5);
  let pts1 = '';
  filtered.slice(0, 200).forEach(v => {
    const xi = lenOrder.indexOf(v.video_length_type);
    if (xi < 0) return;
    const x = pad + (xi + 0.5) * ((w1 - pad*2) / lenOrder.length);
    const y = h1 - pad - ((v.engagement_rate||0) / erMax) * (h1 - pad*2);
    const c = (v.engagement_rate||0) >= 5 ? '#10B981' : (v.engagement_rate||0) >= 2 ? '#F59E0B' : '#94A3B8';
    pts1 += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="3" fill="${c}" opacity="0.6"/>`;
  });
  let xlbl1 = '';
  lenOrder.forEach((l, i) => {
    const x = pad + (i + 0.5) * ((w1 - pad*2) / lenOrder.length);
    xlbl1 += `<text x="${x}" y="${h1 - 6}" text-anchor="middle" font-size="10" fill="#94A3B8" font-family="var(--font-mono)">${l}</text>`;
  });
  const ylbl1 = `<text x="${pad - 6}" y="${pad}" text-anchor="end" font-size="10" fill="#94A3B8">${erMax.toFixed(0)}%</text><text x="${pad - 6}" y="${h1 - pad}" text-anchor="end" font-size="10" fill="#94A3B8">0%</text>`;
  const axis1 = `<line x1="${pad}" y1="${h1 - pad}" x2="${w1 - pad}" y2="${h1 - pad}" stroke="#1E293B"/><line x1="${pad}" y1="${pad}" x2="${pad}" y2="${h1 - pad}" stroke="#1E293B"/>`;

  // Chart 2: KOL 影响力矩阵
  const channels = {};
  DATA.videos.forEach(v => {
    if (!channels[v.channel_name]) channels[v.channel_name] = { name: v.channel_name, subs: v.channel_subscriber_count, ers: [], group: v.channel_group };
    channels[v.channel_name].ers.push(v.engagement_rate || 0);
  });
  const chList = Object.values(channels).map(c => ({ ...c, avgER: c.ers.reduce((s,e) => s+e, 0)/c.ers.length }));
  const w2 = 320, h2 = 200;
  const erMax2 = Math.max(...chList.map(c => c.avgER), 5);
  const subsMin = Math.log10(Math.min(...chList.map(c => Math.max(c.subs, 100))));
  const subsMax = Math.log10(Math.max(...chList.map(c => c.subs), 1));
  let pts2 = '';
  chList.forEach(c => {
    const x = pad + (Math.log10(Math.max(c.subs, 100)) - subsMin) / (subsMax - subsMin || 1) * (w2 - pad*2);
    const y = h2 - pad - (c.avgER / erMax2) * (h2 - pad*2);
    const isSelf = c.name === CFG.self_brand;
    const fill = isSelf ? '#EC4899' : c.avgER >= 5 ? '#10B981' : '#6366F1';
    const r = isSelf ? 5 : 3;
    pts2 += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${r}" fill="${fill}" opacity="0.7"><title>${escHTML(c.name)} · ${fmt(c.subs)} · ER ${c.avgER.toFixed(2)}%</title></circle>`;
  });
  const axis2 = `<line x1="${pad}" y1="${h2 - pad}" x2="${w2 - pad}" y2="${h2 - pad}" stroke="#1E293B"/><line x1="${pad}" y1="${pad}" x2="${pad}" y2="${h2 - pad}" stroke="#1E293B"/>`;
  const lbl2 = `<text x="${pad - 6}" y="${pad}" text-anchor="end" font-size="10" fill="#94A3B8">${erMax2.toFixed(0)}%</text><text x="${pad}" y="${h2 - 6}" text-anchor="start" font-size="10" fill="#94A3B8">${fmt(Math.round(Math.pow(10, subsMin)))}</text><text x="${w2 - pad}" y="${h2 - 6}" text-anchor="end" font-size="10" fill="#94A3B8">${fmt(Math.round(Math.pow(10, subsMax)))}</text>`;

  // Chart 3: 类目供给（横向条）
  const groupCounts = {};
  Object.keys(CFG.group_labels).forEach(g => groupCounts[g] = 0);
  filtered.forEach(v => groupCounts[v.channel_group] = (groupCounts[v.channel_group]||0) + 1);
  const gMax = Math.max(...Object.values(groupCounts), 1);
  const w3 = 320, h3 = 200;
  const barH = 22, gap = 6;
  let bars = '';
  Object.entries(CFG.group_labels).forEach(([g, lbl], i) => {
    const cnt = groupCounts[g];
    const bw = (cnt / gMax) * (w3 - 130);
    const y = 14 + i * (barH + gap);
    bars += `<text x="6" y="${y + 14}" font-size="11" fill="#CBD5E1">${escHTML(lbl)}</text>`;
    bars += `<rect x="124" y="${y}" width="${bw.toFixed(0)}" height="${barH}" fill="#6366F1" opacity="0.6" rx="3"/>`;
    bars += `<text x="${(124 + bw + 6).toFixed(0)}" y="${y + 14}" font-size="11" fill="#94A3B8" font-family="var(--font-mono)">${cnt}</text>`;
  });

  root.innerHTML = `
    <div class="chart-card"><div class="title">视频长度 × ER</div><div class="desc">看哪种长度容易出高 ER（绿=高 / 橙=中 / 灰=低）</div><svg viewBox="0 0 ${w1} ${h1}" preserveAspectRatio="xMidYMid meet">${axis1}${ylbl1}${xlbl1}${pts1}</svg></div>
    <div class="chart-card"><div class="title">频道 KOL 影响力矩阵</div><div class="desc">X=订阅数(log) Y=平均 ER · 右上=顶级 KOL · 左上=性价比 · 玫瑰红=Typecase</div><svg viewBox="0 0 ${w2} ${h2}" preserveAspectRatio="xMidYMid meet">${axis2}${lbl2}${pts2}</svg></div>
    <div class="chart-card"><div class="title">类目内容供给</div><div class="desc">各分组视频数（低=机会蓝海）</div><svg viewBox="0 0 ${w3} ${h3}" preserveAspectRatio="xMidYMid meet">${bars}</svg></div>
  `;
}

// ========== Presets ==========
const PRESETS = [
  { key: '24h_rising', label: '🔥 24h 上升爆款', apply: () => ({ time: '1', hots: ['🔥 上升爆款'] }) },
  { key: '7d_strong',  label: '💥 7 天强爆款',   apply: () => ({ time: '7', hots: ['💥 强爆款', '⭐ 百万爆款', '🚀 现象级'] }) },
  { key: 'high_er',    label: '🎯 高 ER 优质',   apply: () => ({}) },  // 通过 sort=er + 暗 filter
  { key: 'channel_hot',label: '📈 频道爆款',     apply: () => ({}) },  // sort=view_to_sub
  { key: 'phenom',     label: '🚀 现象级',       apply: () => ({ hots: ['🚀 现象级'] }) },
];
function applyPreset(key) {
  const f = defaultFilters();
  let sort = state.sort;
  if (key === '24h_rising') { f.time = '1'; f.hots = ['🔥 上升爆款', '💥 强爆款']; sort = 'er'; }
  else if (key === '7d_strong') { f.time = '7'; f.hots = ['💥 强爆款', '⭐ 百万爆款', '🚀 现象级']; sort = 'views'; }
  else if (key === 'high_er') { sort = 'er'; }
  else if (key === 'channel_hot') { sort = 'view_to_sub'; }
  else if (key === 'phenom') { f.hots = ['🚀 现象级']; sort = 'views'; }
  state.filters = f; state.sort = sort; state.preset = state.preset === key ? '' : key;
  saveState(); render();
}
function renderPresets() {
  const root = document.getElementById('presets');
  root.innerHTML = PRESETS.map(p =>
    `<button class="preset-btn${state.preset === p.key ? ' active' : ''}" data-preset="${p.key}">${p.label}</button>`
  ).join('');
  root.querySelectorAll('[data-preset]').forEach(b => b.onclick = () => applyPreset(b.dataset.preset));
}

// ========== Filters ==========
function renderFilters(rootId, mobile=false) {
  const root = document.getElementById(rootId);
  root.innerHTML = '';
  const fs = mobile ? pendingMobileState.filters : state.filters;
  const setKey = (key, val) => { fs[key] = val; if (!mobile) { saveState(); state.preset = ''; render(); } };

  root.appendChild(makeDropdown({
    label: '时间', multi: false,
    options: [{value:'all',label:'全部'},{value:'1',label:'近 24h'},{value:'7',label:'近 7 天'},{value:'30',label:'近 30 天'},{value:'90',label:'近 90 天'}],
    getSelected: () => fs.time,
    onChange: v => setKey('time', v),
  }).el);

  root.appendChild(makeChannelTreeDropdown({
    getGroups: () => fs.groups,
    getChannels: () => fs.channels,
    onChangeGroups: v => setKey('groups', v),
    onChangeChannels: v => setKey('channels', v),
  }).el);

  root.appendChild(makeDropdown({ label: '内容类型', multi: true, options: CFG.content_tags_order, getSelected: () => fs.contents, onChange: v => setKey('contents', v) }).el);
  root.appendChild(makeDropdown({ label: '时长', multi: true, options: CFG.length_order, getSelected: () => fs.lengths, onChange: v => setKey('lengths', v) }).el);
  root.appendChild(makeDropdown({ label: '爆款', multi: true, options: CFG.hot_level_order, getSelected: () => fs.hots, onChange: v => setKey('hots', v) }).el);
  root.appendChild(makeDropdown({ label: '视频类型', multi: true, options: CFG.video_type_order, getSelected: () => fs.vtypes, onChange: v => setKey('vtypes', v) }).el);
  root.appendChild(makeDropdown({ label: '品牌提及', multi: true, options: brandMentionOptions(), getSelected: () => fs.brands, onChange: v => setKey('brands', v) }).el);

  if (!mobile) {
    root.appendChild(makeDropdown({
      label: '排序', multi: false, alignRight: true,
      options: [
        {value:'er',label:'ER ↓'},
        {value:'views',label:'播放量 ↓'},
        {value:'comment_rate',label:'评论率 ↓'},
        {value:'view_to_sub',label:'播放/订阅比 ↓'},
        {value:'recent',label:'发布时间 ↓'},
      ],
      getSelected: () => state.sort,
      onChange: v => { state.sort = v; saveState(); render(); },
    }).el);

    // 实时结果数
    const filtered = applyFilters(DATA.videos);
    const cnt = filtered.length;
    const cls = cnt === 0 ? 'alert' : cnt < 10 ? 'warn' : '';
    const rc = document.createElement('span');
    rc.className = 'result-count ' + cls;
    rc.textContent = '显示 ' + cnt + ' 条';
    root.appendChild(rc);

    const actions = document.createElement('span');
    actions.className = 'actions';

    const viewBtn = document.createElement('button');
    viewBtn.className = 'btn';
    const viewLabels = { grid: '网格', list: '列表', inspire: '灵感' };
    viewBtn.innerHTML = '视图: ' + viewLabels[state.view_mode || 'grid'];
    viewBtn.onclick = () => {
      const order = ['grid', 'list', 'inspire'];
      state.view_mode = order[(order.indexOf(state.view_mode || 'grid') + 1) % order.length];
      saveState(); render();
    };
    actions.appendChild(viewBtn);

    const bulkBtn = document.createElement('button');
    bulkBtn.className = 'btn' + (bulkMode ? ' btn-primary' : '');
    bulkBtn.textContent = bulkMode ? '退出批量' : '批量模式';
    bulkBtn.onclick = () => {
      bulkMode = !bulkMode;
      if (!bulkMode) bulkSelected.clear();
      render();
    };
    actions.appendChild(bulkBtn);

    const clr = document.createElement('button');
    clr.className = 'btn btn-danger';
    clr.textContent = '清空筛选';
    clr.onclick = () => { state.filters = defaultFilters(); state.preset = ''; saveState(); render(); };
    actions.appendChild(clr);

    const csv = document.createElement('button');
    csv.className = 'btn';
    csv.innerHTML = ICONS.download + ' 导出 CSV';
    csv.onclick = () => exportCSV();
    actions.appendChild(csv);

    root.appendChild(actions);
  }
}

// ========== Selected chips ==========
function renderSelectedChips() {
  const root = document.getElementById('selected-chips');
  const f = state.filters;
  const items = [];
  if (f.time !== 'all') {
    const lbl = {1:'近24h',7:'近7天',30:'近30天',90:'近90天'}[f.time] || f.time;
    items.push({ label: '时间: ' + lbl, key: 'time', value: f.time, impact: countWithout('time', null) });
  }
  f.groups.forEach(g => items.push({ label: CFG.group_labels[g] || g, key: 'groups', value: g, impact: countWithout('groups', g) }));
  f.channels.forEach(c => items.push({ label: '频道: ' + c, key: 'channels', value: c, impact: countWithout('channels', c) }));
  f.contents.forEach(c => items.push({ label: c, key: 'contents', value: c, impact: countWithout('contents', c) }));
  f.lengths.forEach(l => items.push({ label: l, key: 'lengths', value: l, impact: countWithout('lengths', l) }));
  f.hots.forEach(h => items.push({ label: h, key: 'hots', value: h, impact: countWithout('hots', h) }));
  f.vtypes.forEach(v => items.push({ label: v, key: 'vtypes', value: v, impact: countWithout('vtypes', v) }));
  f.brands.forEach(b => items.push({ label: b, key: 'brands', value: b, impact: countWithout('brands', b) }));

  if (items.length === 0) { root.innerHTML = ''; return; }
  const cur = applyFilters(DATA.videos).length;
  root.innerHTML = '<span class="label">已选</span>'
    + items.map((it, i) => {
      const delta = it.impact - cur;
      const sign = delta > 0 ? '+' : '';
      return `<span class="chip">${escHTML(it.label)} <span class="chip-impact">(${sign}${delta})</span><span class="chip-x" data-i="${i}">✕</span></span>`;
    }).join('')
    + `<button class="chip-clear">清空全部</button>`
    + (cur < 10 && items.length >= 2 ? `<button class="chip-relax">智能放宽</button>` : '');

  root.querySelectorAll('.chip-x').forEach((x, i) => x.onclick = () => {
    const it = items[i];
    if (it.key === 'time') state.filters.time = 'all';
    else state.filters[it.key] = state.filters[it.key].filter(v => v !== it.value);
    state.preset = ''; saveState(); render();
  });
  root.querySelector('.chip-clear').onclick = () => { state.filters = defaultFilters(); state.preset = ''; saveState(); render(); };
  const relax = root.querySelector('.chip-relax');
  if (relax) relax.onclick = () => {
    // 移除影响最大的 1 个 filter（impact 最大的）
    let best = null;
    items.forEach(it => { if (!best || it.impact > best.impact) best = it; });
    if (best) {
      if (best.key === 'time') state.filters.time = 'all';
      else state.filters[best.key] = state.filters[best.key].filter(v => v !== best.value);
      state.preset = ''; saveState(); render();
      showToast('放宽筛选: 已移除 ' + best.label);
    }
  };
}

// ========== Mobile drawer ==========
function openMobileDrawer() {
  pendingMobileState = JSON.parse(JSON.stringify({ filters: state.filters, sort: state.sort }));
  renderFilters('mb-drawer-content', true);
  document.getElementById('mb-overlay').classList.add('show');
  document.getElementById('mb-drawer').classList.add('show');
  document.body.style.overflow = 'hidden';
}
function closeMobileDrawer() {
  document.getElementById('mb-overlay').classList.remove('show');
  document.getElementById('mb-drawer').classList.remove('show');
  document.body.style.overflow = '';
  pendingMobileState = null;
}
function applyMobileDrawer() {
  if (pendingMobileState) {
    state.filters = pendingMobileState.filters;
    state.sort = pendingMobileState.sort;
    state.preset = '';
    saveState();
  }
  closeMobileDrawer(); render();
}

// ========== Video Card ==========
function renderVideoCard(v) {
  const grpLbl = CFG.group_labels[v.channel_group] || v.channel_group;
  const isSelf = v.channel_name === CFG.self_brand;
  const isKol = CFG.top_kol.includes(v.channel_name);
  let frameClass = '';
  if (v.hot_level === '🚀 现象级') frameClass = 'hot-phenom';
  else if (v.hot_level === '⭐ 百万爆款') frameClass = 'hot-million';
  if (isSelf) frameClass += ' is-self';
  if (bulkMode) frameClass += ' bulk-mode';
  if (bulkSelected.has(v.video_id)) frameClass += ' bulk-selected';

  const er = v.engagement_rate || 0;
  let erColor;
  if (er >= 8) erColor = 'var(--er-1)';
  else if (er >= 5) erColor = 'var(--er-2)';
  else if (er >= 3) erColor = 'var(--er-3)';
  else if (er >= 1) erColor = 'var(--er-4)';
  else if (er > 0) erColor = 'var(--er-5)';
  else erColor = 'var(--er-0)';

  // ER deltas
  const chAvg = channelAvgER(v.channel_name);
  const grpAvg = groupAvgER(v.channel_group);
  let deltaCh = '', deltaGrp = '';
  if (chAvg > 0) {
    const d = ((er - chAvg) / chAvg) * 100;
    if (Math.abs(d) >= 5) deltaCh = `<span class="delta ${d > 0 ? 'pos' : 'neg'}">${d > 0 ? '↑' : '↓'}${Math.abs(d).toFixed(0)}% vs 频道</span>`;
  }
  if (grpAvg > 0) {
    const d = ((er - grpAvg) / grpAvg) * 100;
    if (Math.abs(d) >= 5) deltaGrp = `<span class="delta ${d > 0 ? 'pos' : 'neg'}">${d > 0 ? '↑' : '↓'}${Math.abs(d).toFixed(0)}% vs 分组</span>`;
  }

  let badges = '';
  if (v.hot_level) {
    let bc = 'rising';
    if (v.hot_level === '🚀 现象级') bc = 'phenom';
    else if (v.hot_level === '⭐ 百万爆款') bc = 'million';
    else if (v.hot_level === '💥 强爆款') bc = 'strong';
    badges += `<span class="hot-chip ${bc}">${v.hot_level}</span>`;
  }
  // 频道爆款百分比（封顶）
  if (v.view_to_sub_tier === '频道爆款') {
    const r = v.view_to_sub_ratio || 0;
    let lbl = r > 1000 ? '>1000% 🚀' : '+' + r.toFixed(0) + '%';
    badges += `<span class="hot-chip strong">⭐ ${lbl}</span>`;
  }

  const tagPriority = ['iPad配件相关','创作','学生','商务','其他Apple'];
  const tagClassMap = {'iPad配件相关':'iPad','创作':'create','学生':'student','商务':'business','其他Apple':'apple'};
  const ctags = (v.content_tags||[]).filter(t => tagPriority.includes(t));
  const ctagsHtml = ctags.map(t => `<span class="tag-c ${tagClassMap[t]}">${t}</span>`).join('');
  const brandsHtml = (v.brand_mentions||[]).map(b => `<span class="tag-c brand">${b}</span>`).join('');
  const vtypeHtml = v.video_type && v.video_type !== '其他' ? `<span class="vtype">${v.video_type}</span>` : '';
  const kolHtml = isKol ? '<span class="tag-c kol">头部 KOL</span>' : '';
  const risingHtml = v.hot_level === '🔥 上升爆款' ? '<span class="tag-c rising">24h 上升</span>' : '';
  // SEO 长尾：发布 > 30 天 + 频道爆款（暗示长尾依然有量）
  const ageDays = (Date.now() - new Date(v.published_at).getTime()) / 86400000;
  const seoHtml = (ageDays > 90 && v.view_to_sub_tier === '频道爆款') ? '<span class="tag-c seo">SEO 长尾</span>' : '';

  const isFav = getFavs().includes(v.video_id);

  return `
    <div class="video-card ${frameClass}" data-vid="${v.video_id}">
      <div class="bulk-cb">${bulkSelected.has(v.video_id) ? '✓' : ''}</div>
      <button class="hide-btn" data-act="hide" data-vid="${v.video_id}" title="隐藏">✕</button>
      <button class="fav-btn ${isFav ? 'active' : ''}" data-act="fav" data-vid="${v.video_id}" title="收藏">${isFav ? ICONS.star : ICONS.star_o}</button>
      <a href="${v.video_url}" target="_blank" rel="noopener" class="thumb-wrap">
        <img src="${v.thumbnail_url}" alt="" loading="lazy" onerror="this.src='https://i.ytimg.com/vi/${v.video_id}/hqdefault.jpg'">
        <div class="badges">${badges}</div>
        <div class="duration">${v.duration || ''}</div>
      </a>
      <div class="card-body">
        <div class="card-row1">
          <span class="channel-name">${escHTML(v.channel_name)}</span>
          ${isSelf ? '<span class="self">⭐ 自家</span>' : ''}
          <span class="grp">${grpLbl}</span>
          <span class="grp">${v.video_length_type}</span>
          ${vtypeHtml}
        </div>
        <a class="card-title" href="${v.video_url}" target="_blank" rel="noopener" title="${escHTML(v.title)}">${escHTML(v.title)}</a>
        <div class="biz-signal">
          <span class="er-num" style="color:${erColor}">${er.toFixed(2)}<span style="font-size:14px;color:var(--text-faint);font-weight:500;">%</span></span>
          <span class="er-label" data-tip="Engagement Rate · 互动率 · (赞+评论)/播放">ER</span>
          <span class="deltas">${deltaCh}${deltaGrp}</span>
        </div>
        <div class="card-stats">
          <span class="item">${ICONS.play}<span class="num">${fmt(v.view_count)}</span></span>
          <span class="item">${ICONS.thumb}<span class="num">${fmt(v.like_count)}</span></span>
          <span class="item">${ICONS.comment}<span class="num">${fmt(v.comment_count)}</span></span>
          <span class="item" style="margin-left:auto">评论率 ${(v.comment_rate||0).toFixed(2)}%</span>
        </div>
        ${(ctagsHtml || brandsHtml || kolHtml || risingHtml || seoHtml) ? `<div class="tag-row">${ctagsHtml}${brandsHtml}${kolHtml}${risingHtml}${seoHtml}</div>` : ''}
        <div class="meta-bottom"><span>${fmtDate(v.published_at)}</span></div>
      </div>
    </div>`;
}

// ========== Compare Board ==========
function renderCompareBoard(filtered) {
  const channels = state.filters.channels;
  if (channels.length < 2) return '';
  // 计算每频道指标
  const stats = channels.map(name => {
    const vs = filtered.filter(v => v.channel_name === name);
    const all = DATA.videos.filter(v => v.channel_name === name);
    const subs = all[0]?.channel_subscriber_count || 0;
    const tot = vs.reduce((s,v) => s+(v.view_count||0), 0);
    const aer = vs.length ? vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length : 0;
    const hot = vs.filter(v => v.hot_level).length;
    const high_er = vs.filter(v => (v.engagement_rate||0) >= 5).length;
    return { name, subs, count: vs.length, tot, aer, hot, high_er, isSelf: name === CFG.self_brand };
  });
  // 排名
  const rankBy = (key) => {
    const sorted = [...stats].sort((a,b) => b[key] - a[key]);
    return name => sorted.findIndex(s => s.name === name);
  };
  const rkSubs = rankBy('subs'), rkCount = rankBy('count'), rkTot = rankBy('tot'), rkER = rankBy('aer'), rkHot = rankBy('hot');
  const medal = ri => ri === 0 ? '🥇' : ri === 1 ? '🥈' : ri === 2 ? '🥉' : '';
  // 综合评分
  const N = stats.length;
  const scored = stats.map(s => {
    const score = ((N - rkSubs(s.name)) + (N - rkCount(s.name)) + (N - rkER(s.name)) + (N - rkHot(s.name))) / (4 * N) * 100;
    return { ...s, score };
  });

  const html = scored.map(s => `
    <div class="ccard ${s.isSelf ? 'is-self' : ''}" data-channel="${escHTML(s.name)}">
      <button class="close" data-close="${escHTML(s.name)}">✕</button>
      <div class="head">
        <span class="name">${escHTML(s.name)}</span>
        ${s.isSelf ? '<span class="self-tag">⭐ 自家</span>' : ''}
      </div>
      <div class="subs">${fmt(s.subs)} 订阅</div>
      <div class="grid2">
        <div class="cell">视频<b>${s.count}<span class="rank">${medal(rkCount(s.name))}</span></b></div>
        <div class="cell">总播放<b>${fmt(s.tot)}<span class="rank">${medal(rkTot(s.name))}</span></b></div>
        <div class="cell">平均 ER<b>${s.aer.toFixed(2)}%<span class="rank">${medal(rkER(s.name))}</span></b></div>
        <div class="cell">爆款<b>${s.hot}<span class="rank">${medal(rkHot(s.name))}</span></b></div>
      </div>
      <div class="cell" style="margin-bottom:8px">高 ER 视频 (≥5%)<b>${s.high_er}</b></div>
      <div class="score-row">
        <span>综合实力</span>
        <span class="score-bar"><span style="width:${s.score.toFixed(0)}%"></span></span>
        <span class="score-num">${s.score.toFixed(0)}/100</span>
      </div>
    </div>
  `).join('');
  return '<div class="compare-board">' + html + '</div>';
}

// ========== Bulk bar ==========
function renderBulkBar(visibleVideos) {
  if (!bulkMode) return '';
  return `
    <div class="bulk-bar">
      <span class="selected-count">已选 ${bulkSelected.size} 个</span>
      <button class="btn" id="bulk-all">全选当前页</button>
      <button class="btn" id="bulk-none">全部取消</button>
      <button class="btn btn-primary" id="bulk-fav">⭐ 加入拆解清单</button>
      <button class="btn" id="bulk-link">复制链接</button>
      <button class="btn" id="bulk-csv">${ICONS.download} 导出 CSV</button>
      <button class="btn" id="bulk-exit" style="margin-left:auto">退出批量</button>
    </div>`;
}
function bindBulkBar(visible) {
  const all = document.getElementById('bulk-all');
  const none = document.getElementById('bulk-none');
  const fav = document.getElementById('bulk-fav');
  const link = document.getElementById('bulk-link');
  const csv = document.getElementById('bulk-csv');
  const exit = document.getElementById('bulk-exit');
  if (all) all.onclick = () => { visible.forEach(v => bulkSelected.add(v.video_id)); render(); };
  if (none) none.onclick = () => { bulkSelected.clear(); render(); };
  if (fav) fav.onclick = () => {
    const cur = new Set(getFavs());
    bulkSelected.forEach(id => cur.add(id));
    setFavs(Array.from(cur)); showToast('已加入拆解清单 ' + bulkSelected.size + ' 个'); bulkSelected.clear(); bulkMode = false; render();
  };
  if (link) link.onclick = () => {
    const urls = Array.from(bulkSelected).map(id => DATA.videos.find(v => v.video_id === id)?.video_url).filter(Boolean).join('\\n');
    navigator.clipboard?.writeText(urls).then(() => showToast('已复制 ' + bulkSelected.size + ' 个链接'));
  };
  if (csv) csv.onclick = () => {
    const data = visible.filter(v => bulkSelected.has(v.video_id));
    exportCSV(data, 'bulk');
  };
  if (exit) exit.onclick = () => { bulkMode = false; bulkSelected.clear(); render(); };
}

// ========== Home View ==========
function renderHomeView() {
  const root = document.getElementById('view-home');
  // charts
  const filtered = applyFilters(DATA.videos);
  const sorted = applySort(filtered);

  let html = '';
  html += '<div id="charts-root" class="charts"></div>';
  html += renderBulkBar(sorted);
  html += renderCompareBoard(filtered);

  if (sorted.length === 0) {
    const f = state.filters;
    let banner = '';
    if (activeFilterCount() > 0) {
      // 计算每个 filter 移除后 result 数
      const sugs = [];
      ['groups','channels','contents','lengths','hots','vtypes','brands'].forEach(k => {
        f[k].forEach(val => {
          const cnt = countWithout(k, val);
          if (cnt > 0) sugs.push({ k, val, cnt });
        });
      });
      if (f.time !== 'all') {
        const cnt = countWithout('time', null);
        if (cnt > 0) sugs.push({ k: 'time', val: f.time, cnt });
      }
      sugs.sort((a,b) => b.cnt - a.cnt);
      banner = `<div class="empty-banner"><div class="title">⚠️ 无符合条件视频</div><div class="suggest">`
        + sugs.slice(0, 3).map((s, i) => `<button data-sug="${i}">移除「${escHTML(s.k === 'time' ? '时间' : s.val)}」→ 显示 ${s.cnt} 条</button>`).join('')
        + `</div></div>`;
    }
    html += banner;
    html += '<div class="empty">没有符合筛选条件的视频</div>';
  } else {
    const cls = 'grid' + (state.view_mode === 'list' ? ' list-view' : state.view_mode === 'inspire' ? ' inspire-view' : '');
    html += `<div class="${cls}">` + sorted.map(renderVideoCard).join('') + '</div>';
  }
  root.innerHTML = html;
  renderCharts(filtered);
  bindCardActions(root);
  bindBulkBar(sorted);

  // 空状态建议按钮
  root.querySelectorAll('[data-sug]').forEach(b => b.onclick = (e) => {
    const i = parseInt(b.dataset.sug);
    const sugs = []; const f = state.filters;
    ['groups','channels','contents','lengths','hots','vtypes','brands'].forEach(k => f[k].forEach(val => sugs.push({k, val})));
    if (f.time !== 'all') sugs.push({ k: 'time' });
    sugs.sort((a,b) => countWithout(b.k, b.val) - countWithout(a.k, a.val));
    const s = sugs[i];
    if (s.k === 'time') state.filters.time = 'all';
    else state.filters[s.k] = state.filters[s.k].filter(x => x !== s.val);
    state.preset = ''; saveState(); render();
  });

  // 多频道对比卡的关闭
  root.querySelectorAll('[data-close]').forEach(b => b.onclick = () => {
    const name = b.dataset.close;
    state.filters.channels = state.filters.channels.filter(c => c !== name);
    saveState(); render();
  });
  root.querySelectorAll('.ccard[data-channel]').forEach(c => c.onclick = (e) => {
    if (e.target.dataset.close) return;
    const name = c.dataset.channel;
    state.filters.channels = [name];
    state.filters.groups = [];
    saveState(); render();
  });
}

// ========== Favorites View ==========
function renderFavoritesView() {
  const root = document.getElementById('view-favorites');
  const favIds = getFavs();
  const favSet = new Set(favIds);
  const favs = DATA.videos.filter(v => favSet.has(v.video_id));
  const sorted = applySort(favs);

  let html = '';
  if (!state.workflow_banner_dismissed) {
    html += `<div class="workflow-banner">
      <span class="close-x" onclick="state.workflow_banner_dismissed=true; saveState(); render();">✕</span>
      <h4>💡 拆解工作流</h4>
      <ol>
        <li>浏览首页或点筛选预设 → 找候选爆款</li>
        <li>启动批量模式 → 选 5-10 条 → 加入此清单</li>
        <li>在此 Tab 给每条填 10 维（前 5 维代码自动填，后 5 维你手填）</li>
        <li>[批量复制链接] → 粘贴到 Claude.ai 网页</li>
        <li>让 Claude 拆 Hook + Body + CTA + 公式</li>
        <li>公式入 Obsidian <code>30_内容弹药库/</code></li>
      </ol>
    </div>`;
  }

  html += `<div class="filter-bar"><span class="result-count">${favs.length} 条</span>
    <div class="actions">
      <button class="btn" id="fav-tbl">表格视图</button>
      <button class="btn" id="fav-card">卡片视图</button>
      ${favs.length > 0 ? `<button class="btn" id="fav-md">${ICONS.download} 复制 Markdown</button>
      <button class="btn" id="fav-csv">${ICONS.download} 导出 CSV (10 维)</button>
      <button class="btn btn-danger" id="fav-clear">清空收藏</button>` : ''}
      <span style="font-size:11px;color:var(--text-faint);margin-left:auto">跨平台联动: <button class="btn" disabled>Reddit</button> <button class="btn" disabled>Trends</button> <button class="btn" disabled>TikTok</button></span>
    </div></div>`;

  if (favs.length === 0) {
    html += '<div class="empty">还没有收藏视频。在首页或批量模式中点 ⭐ 加入。</div>';
  } else {
    // 默认卡片视图
    const td = getTeardownData();
    html += '<div class="grid">' + sorted.map(v => {
      const t = td[v.video_id] || {};
      return renderTeardownCard(v, t);
    }).join('') + '</div>';
  }
  root.innerHTML = html;

  const tbl = document.getElementById('fav-tbl');
  if (tbl) tbl.onclick = () => showTeardownTable(sorted);
  const md = document.getElementById('fav-md');
  if (md) md.onclick = () => exportMarkdown(sorted);
  const csv = document.getElementById('fav-csv');
  if (csv) csv.onclick = () => exportTeardownCSV(sorted);
  const clr = document.getElementById('fav-clear');
  if (clr) clr.onclick = () => { if (confirm('清空全部收藏？')) { setFavs([]); render(); showToast('已清空'); } };
  bindCardActions(root);
}

const TEARDOWN_DIMS = [
  { key: 'hook', label: 'Hook', auto: false },
  { key: 'pain', label: 'Pain Point', auto: false },
  { key: 'arc', label: 'Story Arc', auto: false },
  { key: 'visual', label: 'Visual Style', auto: false },
  { key: 'audio', label: 'Audio', auto: false },
  { key: 'cta', label: 'CTA', auto: false },
  { key: 'engage_hook', label: 'Engagement Hook', auto: true },
  { key: 'key_frame', label: 'Key Frame', auto: true },
  { key: 'format_type', label: 'Format Type', auto: true },
  { key: 'perf_signal', label: 'Performance Signal', auto: true },
];

function autoFillTeardown(v) {
  // 后 5 维自动填
  const pf = v.engagement_rate >= 5 ? '高互动' : v.engagement_rate >= 2 ? '中等' : '低';
  return {
    engage_hook: '评论率 ' + (v.comment_rate||0).toFixed(2) + '%',
    key_frame: v.video_length_type + ' · ' + (v.duration || ''),
    format_type: v.video_type + ' / ' + (v.content_tags||[]).join('+'),
    perf_signal: 'ER ' + (v.engagement_rate||0).toFixed(2) + '% · ' + fmt(v.view_count) + ' views · ' + (v.hot_level || '普通') + ' · ' + pf,
  };
}

function renderTeardownCard(v, td) {
  const auto = autoFillTeardown(v);
  const progress = td.progress || '待拆';
  const progressClass = progress === '已沉淀公式' ? 'green' : progress === '拆解中' ? 'orange' : '';
  return `
    <div class="video-card" data-vid="${v.video_id}" style="border-color:${progress === '已沉淀公式' ? 'var(--up)' : 'var(--border)'}">
      <a href="${v.video_url}" target="_blank" class="thumb-wrap">
        <img src="${v.thumbnail_url}" alt="" loading="lazy">
        <div class="duration">${v.duration || ''}</div>
      </a>
      <div class="card-body">
        <div class="card-row1"><span class="channel-name">${escHTML(v.channel_name)}</span></div>
        <a class="card-title" href="${v.video_url}" target="_blank">${escHTML(v.title)}</a>
        <div style="font-size:11px;color:var(--text-faint);font-family:var(--font-mono)">ER ${(v.engagement_rate||0).toFixed(2)}% · ▶ ${fmt(v.view_count)}</div>
        <div style="border-top:1px dashed var(--border);padding-top:8px;margin-top:4px;display:flex;flex-direction:column;gap:6px">
          ${TEARDOWN_DIMS.slice(0, 6).map(d => `
            <div style="font-size:11px"><span style="color:var(--text-faint);min-width:90px;display:inline-block">${d.label}:</span>
              <input type="text" data-vid="${v.video_id}" data-key="${d.key}" value="${escHTML(td[d.key]||'')}" placeholder="${d.auto ? '(自动)' : '手填...'}"
                style="background:var(--card-hover);border:1px solid var(--border);color:var(--text);padding:3px 6px;border-radius:4px;width:calc(100% - 96px);font-size:11px;font-family:var(--font-sans)"></div>
          `).join('')}
          <div style="font-size:10.5px;color:var(--text-faint);padding-top:4px;border-top:1px dashed var(--border)">
            <div>Engagement Hook: <b style="color:var(--text-muted)">${auto.engage_hook}</b></div>
            <div>Key Frame: <b style="color:var(--text-muted)">${auto.key_frame}</b></div>
            <div>Format Type: <b style="color:var(--text-muted)">${auto.format_type}</b></div>
            <div>Performance Signal: <b style="color:var(--text-muted)">${auto.perf_signal}</b></div>
          </div>
          <div style="display:flex;gap:6px;align-items:center;font-size:11px">
            <span style="color:var(--text-faint)">进度:</span>
            <select data-vid="${v.video_id}" data-key="progress" style="background:var(--card-hover);border:1px solid var(--border);color:var(--text);padding:3px 6px;border-radius:4px;font-size:11px">
              <option ${progress === '待拆' ? 'selected' : ''}>待拆</option>
              <option ${progress === '拆解中' ? 'selected' : ''}>拆解中</option>
              <option ${progress === '已沉淀公式' ? 'selected' : ''}>已沉淀公式</option>
            </select>
            <button class="btn btn-danger" style="margin-left:auto;padding:4px 10px;font-size:11px;min-height:28px" data-rm-fav="${v.video_id}">移除</button>
          </div>
          <textarea data-vid="${v.video_id}" data-key="notes" placeholder="备注..." style="background:var(--card-hover);border:1px solid var(--border);color:var(--text);padding:6px;border-radius:4px;font-size:11px;font-family:var(--font-sans);resize:vertical;min-height:40px">${escHTML(td.notes||'')}</textarea>
        </div>
      </div>
    </div>`;
}

function showTeardownTable(videos) {
  const root = document.getElementById('view-favorites');
  const td = getTeardownData();
  const cols = ['Title', 'Channel', 'ER', 'Views', 'Hook', 'Pain', 'Arc', 'Visual', 'Audio', 'CTA', '进度'];
  let rows = '';
  videos.forEach(v => {
    const t = td[v.video_id] || {};
    rows += `<tr>
      <td class="name" style="max-width:200px;overflow:hidden;text-overflow:ellipsis"><a href="${v.video_url}" target="_blank">${escHTML(v.title.slice(0, 40))}</a></td>
      <td>${escHTML(v.channel_name)}</td>
      <td>${(v.engagement_rate||0).toFixed(2)}%</td>
      <td>${fmt(v.view_count)}</td>
      <td>${escHTML(t.hook || '')}</td>
      <td>${escHTML(t.pain || '')}</td>
      <td>${escHTML(t.arc || '')}</td>
      <td>${escHTML(t.visual || '')}</td>
      <td>${escHTML(t.audio || '')}</td>
      <td>${escHTML(t.cta || '')}</td>
      <td>${escHTML(t.progress || '待拆')}</td>
    </tr>`;
  });
  root.innerHTML = `<button class="btn" id="back-card" style="margin-bottom:14px">← 卡片视图</button>
    <div class="panel" style="overflow-x:auto"><table><thead><tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>`;
  document.getElementById('back-card').onclick = () => render();
}

// ========== Brand Compare View ==========
function renderBrandCompareView() {
  const root = document.getElementById('view-brand');
  const brands = CFG.brand_compare_default;
  const stats = brands.map(name => {
    const vs = DATA.videos.filter(v => v.channel_name === name);
    const tot = vs.reduce((s,v) => s+(v.view_count||0), 0);
    const aer = vs.length ? vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length : 0;
    const hot = vs.filter(v => v.hot_level).length;
    const max = vs.length ? Math.max(...vs.map(v => v.view_count||0)) : 0;
    const week = vs.filter(v => withinTime(v.published_at, '7'));
    return { name, count: vs.length, tot, aer, hot, max, weekCount: week.length, subs: vs[0]?.channel_subscriber_count || 0, isSelf: name === CFG.self_brand };
  });
  const maxTot = Math.max(...stats.map(s => s.tot), 1);
  let html = '<div class="panel"><h3>核心竞品横向对比</h3>'
    + '<table><thead><tr><th>频道</th><th>订阅</th><th>视频</th><th>本周新</th><th>平均 ER</th><th>最高单条</th><th>爆款</th><th>总播放</th></tr></thead><tbody>';
  stats.forEach(s => {
    html += `<tr><td class="name">${s.isSelf ? '⭐ ' : ''}${escHTML(s.name)}</td><td>${fmt(s.subs)}</td><td>${s.count}</td><td>${s.weekCount}</td><td>${s.aer.toFixed(2)}%</td><td>${fmt(s.max)}</td><td>${s.hot}</td><td>${fmt(s.tot)}<span class="bar"><span style="width:${(s.tot/maxTot*100).toFixed(0)}%"></span></span></td></tr>`;
  });
  html += '</tbody></table></div>';

  // A 组全量
  const aChannels = (CFG.channel_tree.A_brand||[]).map(c => c.display_name);
  const aStats = aChannels.map(name => {
    const vs = DATA.videos.filter(v => v.channel_name === name);
    return {
      name, count: vs.length, subs: vs[0]?.channel_subscriber_count || 0,
      aer: vs.length ? vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length : 0,
      hot: vs.filter(v => v.hot_level).length,
      tot: vs.reduce((s,v) => s+(v.view_count||0), 0),
      isSelf: name === CFG.self_brand,
    };
  });
  aStats.sort((a,b) => b.subs - a.subs);
  html += '<div class="panel"><h3>A 组竞品全量</h3><table><thead><tr><th>频道</th><th>订阅</th><th>视频</th><th>平均 ER</th><th>爆款</th><th>总播放</th></tr></thead><tbody>';
  aStats.forEach(s => {
    html += `<tr><td class="name">${s.isSelf ? '⭐ ' : ''}${escHTML(s.name)}</td><td>${fmt(s.subs)}</td><td>${s.count}</td><td>${s.aer.toFixed(2)}%</td><td>${s.hot}</td><td>${fmt(s.tot)}</td></tr>`;
  });
  html += '</tbody></table></div>';
  root.innerHTML = html;
}

// ========== History View ==========
function renderHistoryView() {
  const root = document.getElementById('view-history');
  const cnt = HISTORY?.count || 0;
  const need = 7;
  let html = '<div class="panel"><h3>历史趋势</h3>';
  if (cnt < need) {
    html += `<div class="history-empty"><div class="big">需要积累 ${need} 天数据，才能显示趋势</div><div>已积累 ${cnt} 天 / 还需 ${need - cnt} 天</div><div class="progress"><span style="width:${(cnt/need*100).toFixed(0)}%"></span></div><div style="margin-top:14px;font-size:12px;color:var(--text-faint)">每天 9:00 自动跑完会保存当日快照到 <code>data/history/{YYYY-MM-DD}.json</code></div></div>`;
  } else {
    html += '<div>（数据已积累足够，趋势图开发中）</div>';
  }
  html += '</div>';
  root.innerHTML = html;
}

// ========== Monitor View（竞品监测）==========
function renderMonitorView() {
  const root = document.getElementById('view-monitor');
  const aChannels = (CFG.channel_tree.A_brand||[]).map(c => c.display_name);
  const aWeek = DATA.videos.filter(v => v.channel_group === 'A_brand' && withinTime(v.published_at, '7'));
  aWeek.sort((a,b) => new Date(b.published_at) - new Date(a.published_at));
  const stats = aChannels.map(name => ({
    name,
    weekVids: aWeek.filter(v => v.channel_name === name),
    weekHot: aWeek.filter(v => v.channel_name === name && (v.view_count >= 1e5 || v.hot_level)).length,
  }));
  let html = '<div class="panel"><h3>本周 A 组竞品动态</h3>';
  html += `<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));gap:10px;margin-bottom:18px">`
    + stats.map(s => `<div class="ccard ${s.name === CFG.self_brand ? 'is-self' : ''}"><div class="head"><span class="name">${escHTML(s.name)}</span></div><div style="font-size:13px;font-family:var(--font-mono);color:var(--text)">本周 <b>${s.weekVids.length}</b> 条 · 爆款 <b>${s.weekHot}</b></div></div>`).join('')
    + '</div>';
  html += `<h3 style="margin-top:24px">本周新视频 (${aWeek.length} 条)</h3>`;
  if (aWeek.length === 0) {
    html += '<div class="empty">本周 A 组无新视频</div>';
  } else {
    html += '<div class="grid">' + aWeek.map(renderVideoCard).join('') + '</div>';
  }
  html += '</div>';
  root.innerHTML = html;
  bindCardActions(root);
}

// ========== Card actions ==========
function bindCardActions(root) {
  root.querySelectorAll('.fav-btn').forEach(b => b.onclick = (e) => {
    e.stopPropagation(); e.preventDefault();
    const vid = b.dataset.vid;
    const cur = getFavs();
    const i = cur.indexOf(vid);
    if (i >= 0) { cur.splice(i, 1); setFavs(cur); showToast('已取消收藏'); }
    else { cur.push(vid); setFavs(cur); showToast('已加入拆解清单'); }
    render();
  });
  root.querySelectorAll('.hide-btn').forEach(b => b.onclick = (e) => {
    e.stopPropagation(); e.preventDefault();
    const vid = b.dataset.vid;
    const cur = getHidden();
    if (!cur.includes(vid)) { cur.push(vid); setHidden(cur); showToast('已隐藏'); }
    render();
  });
  root.querySelectorAll('.bulk-cb').forEach(c => c.onclick = (e) => {
    e.stopPropagation(); e.preventDefault();
    const card = c.closest('.video-card');
    const vid = card.dataset.vid;
    if (bulkSelected.has(vid)) bulkSelected.delete(vid);
    else bulkSelected.add(vid);
    render();
  });
  // 拆解清单输入
  root.querySelectorAll('input[data-key], textarea[data-key], select[data-key]').forEach(inp => {
    inp.onchange = () => {
      const td = getTeardownData();
      const vid = inp.dataset.vid;
      td[vid] = td[vid] || {};
      td[vid][inp.dataset.key] = inp.value;
      setTeardownData(td);
    };
  });
  root.querySelectorAll('[data-rm-fav]').forEach(b => b.onclick = () => {
    const vid = b.dataset.rmFav;
    setFavs(getFavs().filter(x => x !== vid));
    render();
  });
}

// ========== Export ==========
function exportCSV(videos=null, suffix='filtered') {
  const data = videos || applyFilters(DATA.videos);
  const cols = ['video_id','channel_name','channel_group','title','view_count','like_count','comment_count','engagement_rate','comment_rate','duration','published_at','hot_level','video_length_type','video_type','content_tags','brand_mentions','view_to_sub_ratio','relevance_score','video_url'];
  const rows = data.map(v => cols.map(c => {
    let val = v[c];
    if (Array.isArray(val)) val = val.join('; ');
    val = val == null ? '' : String(val);
    if (/[",\n]/.test(val)) val = '"' + val.replace(/"/g, '""') + '"';
    return val;
  }).join(','));
  const csv = '﻿' + cols.join(',') + '\n' + rows.join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `youtube-tracker-${suffix}-${new Date().toISOString().slice(0,10)}.csv`;
  a.click(); URL.revokeObjectURL(url);
  showToast(`已导出 ${data.length} 条 CSV`);
}
function exportTeardownCSV(videos) {
  const td = getTeardownData();
  const dims = TEARDOWN_DIMS.map(d => d.key);
  const cols = ['video_id','title','channel_name','er','views','progress', ...dims, 'notes','url'];
  const rows = videos.map(v => {
    const t = td[v.video_id] || {};
    const auto = autoFillTeardown(v);
    return cols.map(c => {
      let val;
      if (c === 'er') val = (v.engagement_rate||0).toFixed(2);
      else if (c === 'views') val = v.view_count;
      else if (c === 'url') val = v.video_url;
      else if (c === 'progress') val = t.progress || '待拆';
      else if (c === 'notes') val = t.notes || '';
      else if (dims.includes(c)) val = t[c] || auto[c] || '';
      else val = v[c];
      if (val == null) val = '';
      val = String(val);
      if (/[",\n]/.test(val)) val = '"' + val.replace(/"/g, '""') + '"';
      return val;
    }).join(',');
  });
  const csv = '﻿' + cols.join(',') + '\n' + rows.join('\n');
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `youtube-tracker-teardown-${new Date().toISOString().slice(0,10)}.csv`;
  a.click(); URL.revokeObjectURL(url);
  showToast('已导出拆解清单 ' + videos.length + ' 条');
}
function exportMarkdown(videos) {
  const md = videos.map(v => `- [${v.title}](${v.video_url}) · ${v.channel_name} · ▶ ${fmt(v.view_count)} · ER ${(v.engagement_rate||0).toFixed(2)}%`).join('\n');
  navigator.clipboard?.writeText(md).then(() => showToast('Markdown 已复制到剪贴板'));
}

// ========== Master Render ==========
function render() {
  document.getElementById('view-home').style.display = state.tab === 'home' ? 'block' : 'none';
  document.getElementById('view-favorites').style.display = state.tab === 'favorites' ? 'block' : 'none';
  document.getElementById('view-brand').style.display = state.tab === 'brand' ? 'block' : 'none';
  document.getElementById('view-history').style.display = state.tab === 'history' ? 'block' : 'none';
  document.getElementById('view-monitor').style.display = state.tab === 'monitor' ? 'block' : 'none';

  const filtered = applyFilters(DATA.videos);

  renderTabs();
  renderKPI(filtered);
  renderInsight(filtered);
  renderStatRow(filtered);
  renderPresets();
  renderFilters('desktop-filters');
  renderSelectedChips();

  if (state.tab === 'home') renderHomeView();
  else if (state.tab === 'favorites') renderFavoritesView();
  else if (state.tab === 'brand') renderBrandCompareView();
  else if (state.tab === 'history') renderHistoryView();
  else if (state.tab === 'monitor') renderMonitorView();

  // mobile badges
  const fcnt = activeFilterCount();
  const fcb = document.getElementById('mb-filter-count');
  if (fcnt > 0) { fcb.textContent = fcnt; fcb.style.display = 'inline-block'; } else { fcb.style.display = 'none'; }
  const favCnt = getFavs().length;
  const favb = document.getElementById('mb-fav-count');
  if (favCnt > 0) { favb.textContent = favCnt; favb.style.display = 'inline-block'; } else { favb.style.display = 'none'; }
  const sortMap = { er: 'ER↓', views: '播放↓', comment_rate: '评论率↓', view_to_sub: '播放/订阅↓', recent: '最新' };
  document.getElementById('mb-sort-label').textContent = sortMap[state.sort] || '';
}

function updateMeta() {
  document.getElementById('gen-at').textContent = DATA.generated_at;
  document.getElementById('gen-ago').textContent = fmtAgo(DATA.generated_at);
  document.getElementById('ch-count').textContent = DATA.channel_count;
  document.getElementById('vid-count').textContent = DATA.video_count;
}

async function init() {
  document.getElementById('mb-filter').onclick = openMobileDrawer;
  document.getElementById('mb-fav').onclick = () => { state.tab = 'favorites'; saveState(); render(); };
  document.getElementById('mb-sort').onclick = () => {
    const opts = ['er','views','comment_rate','view_to_sub','recent'];
    const cur = opts.indexOf(state.sort);
    state.sort = opts[(cur + 1) % opts.length];
    saveState(); render();
    showToast('排序: ' + ({er:'ER↓',views:'播放↓',comment_rate:'评论率↓',view_to_sub:'播放/订阅↓',recent:'最新'}[state.sort]));
  };
  document.getElementById('mb-overlay').onclick = closeMobileDrawer;
  document.getElementById('mb-drawer-close').onclick = closeMobileDrawer;
  document.getElementById('mb-drawer-reset').onclick = () => { pendingMobileState.filters = defaultFilters(); renderFilters('mb-drawer-content', true); };
  document.getElementById('mb-drawer-apply').onclick = applyMobileDrawer;

  try {
    DATA = await fetchData();
    HISTORY = await fetchHistoryIndex();
    updateMeta();
    render();
  } catch (e) {
    document.getElementById('view-home').innerHTML =
      '<div class="empty">❌ 加载数据失败: ' + escHTML(e.message) +
      '<br>请用 <code>http://localhost:8765/dashboard.html</code> 或云端 GitHub Pages 网址打开</div>';
    return;
  }
  setInterval(checkUpdate, POLL_INTERVAL_MS);
  setInterval(() => { if (DATA) document.getElementById('gen-ago').textContent = fmtAgo(DATA.generated_at); }, 30000);
}

async function checkUpdate() {
  try {
    const newData = await fetchData();
    if (newData.generated_at !== DATA.generated_at) {
      const oldVid = DATA.video_count;
      DATA = newData;
      HISTORY = await fetchHistoryIndex();
      updateMeta(); render();
      const delta = DATA.video_count - oldVid;
      showToast('🔄 数据已更新 (' + DATA.video_count + ' 条' + (delta ? ', 变化 ' + (delta > 0 ? '+' : '') + delta : '') + ')');
    }
  } catch (e) { console.warn('轮询失败:', e.message); }
}

init();
</script>
</body>
</html>
"""
    html = html.replace("__CFG__", cfg_json)
    OUT_FILE.write_text(html, encoding="utf-8")
    print(f"✅ 写入 {OUT_FILE}  ({OUT_FILE.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
