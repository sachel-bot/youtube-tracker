"""
Step 4 (V5): 5 个紧急修复
1) 折叠式顶部概览 - 默认折叠成一行 + localStorage 记忆
2) 桌面 ≥1024 左侧栏筛选 280px sticky
3) 多选下拉真改：tempSelected + [确定]/[取消] 按钮
4) 视频区域占主区 75%
5) 智能洞察自动更新（已有 setInterval 60s 轮询）
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

    # 用 r-string 防 \n 陷阱
    html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta http-equiv="Cache-Control" content="no-store">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>YouTube 北美 iPad 配件内容情报</title>
<style>
  :root, :root[data-theme="dark"] {
    --bg: #0A0E1A; --card: #131826; --card-hover: #1A2032;
    --text: #F1F5F9; --text-muted: #94A3B8; --text-faint: #64748B;
    --primary: #6366F1; --primary-bg: rgba(99,102,241,0.15); --primary-text: #C7D2FE;
    --purple: #A855F7; --purple-bg: rgba(168,85,247,0.15); --purple-text: #DDD6FE;
    --rose: #EC4899; --rose-bg: rgba(236,72,153,0.15); --rose-text: #F9A8D4;
    --up: #10B981; --down: #F43F5E; --warn: #F59E0B;
    --red-bg: rgba(239,68,68,0.15); --red-text: #FCA5A5;
    --orange-bg: rgba(245,158,11,0.15); --orange-text: #FCD34D;
    --green-bg: rgba(16,185,129,0.15); --green-text: #6EE7B7;
    --gray-bg: rgba(148,163,184,0.15); --gray-text: #CBD5E1;
    --border: #1E293B; --border-hover: #334155;
    --er-1: #34D399; --er-2: #6EE7B7; --er-3: #FCD34D; --er-4: #FDBA74; --er-5: #FCA5A5; --er-0: #94A3B8;
    --shadow: 0 4px 20px rgba(0,0,0,0.4); --shadow-lg: 0 8px 32px rgba(0,0,0,0.5);
    --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    --font-mono: "JetBrains Mono", "SF Mono", ui-monospace, monospace;
    --header-h: 130px; --sidebar-w: 280px;
  }
  :root[data-theme="light"] {
    --bg: #F8FAFC; --card: #FFFFFF; --card-hover: #F1F5F9;
    --text: #0F172A; --text-muted: #475569; --text-faint: #64748B;
    --primary: #6366F1; --primary-bg: rgba(99,102,241,0.10); --primary-text: #4338CA;
    --purple: #A855F7; --purple-bg: rgba(168,85,247,0.10); --purple-text: #6D28D9;
    --rose: #EC4899; --rose-bg: rgba(236,72,153,0.10); --rose-text: #BE185D;
    --up: #059669; --down: #DC2626; --warn: #D97706;
    --red-bg: rgba(239,68,68,0.10); --red-text: #B91C1C;
    --orange-bg: rgba(245,158,11,0.10); --orange-text: #B45309;
    --green-bg: rgba(16,185,129,0.10); --green-text: #047857;
    --gray-bg: rgba(148,163,184,0.10); --gray-text: #475569;
    --border: #E2E8F0; --border-hover: #CBD5E1;
    --er-1: #059669; --er-2: #10B981; --er-3: #D97706; --er-4: #EA580C; --er-5: #DC2626; --er-0: #64748B;
    --shadow: 0 1px 3px rgba(0,0,0,0.06); --shadow-lg: 0 8px 24px rgba(0,0,0,0.10);
  }
  * { box-sizing: border-box; }
  html { -webkit-font-smoothing: antialiased; }
  body { margin: 0; background: var(--bg); color: var(--text);
    font-family: var(--font-sans); font-size: 14px; line-height: 1.5;
    -webkit-tap-highlight-color: transparent; }
  a { color: inherit; text-decoration: none; }
  button { font-family: inherit; font-size: inherit; cursor: pointer; }
  input, select, textarea { font-family: inherit; }

  /* ========== Header ========== */
  header { position: sticky; top: 0; z-index: 100;
    background: var(--bg); backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid var(--border); }
  .container { max-width: 1440px; margin: 0 auto; padding: 14px 24px 8px; }
  .hero h1 { margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.05em; font-family: var(--font-sans); }
  .hero h1 .dot { color: var(--primary); margin: 0 4px; }
  .hero .subtitle { color: var(--text-muted); font-size: 13px; margin-top: 4px; font-weight: 400; }
  .meta-line { color: var(--text-faint); font-size: 11px; margin-top: 4px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
  .meta-line b { color: var(--text); }
  .live-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--up); display: inline-block; margin-right: 5px; animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

  /* Tabs */
  .tabs { display: flex; gap: 2px; margin-top: 10px; flex-wrap: wrap; }
  .tab { padding: 7px 14px; border-radius: 8px; font-size: 12.5px; color: var(--text-muted);
    background: transparent; border: 1px solid transparent; font-weight: 500;
    transition: all 0.15s ease; min-height: 32px; display: inline-flex; align-items: center; gap: 6px; }
  .tab:hover { color: var(--text); background: var(--card); }
  .tab.active { background: var(--primary-bg); color: var(--primary-text); border-color: var(--primary); }
  .tab-badge { background: var(--primary); color: #0A0E1A; font-size: 10px; font-weight: 700;
    padding: 1px 7px; border-radius: 9px; min-width: 18px; text-align: center; }

  /* Compact overview bar (折叠) */
  .overview-bar { display: flex; align-items: center; gap: 12px;
    padding: 8px 12px; background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    margin-top: 10px; font-size: 12.5px; color: var(--text-muted); flex-wrap: wrap; }
  .overview-bar .key { color: var(--text-faint); font-size: 11px; margin-right: 4px; }
  .overview-bar b { color: var(--text); font-family: var(--font-mono); font-weight: 600; }
  .overview-bar .toggle { margin-left: auto; padding: 4px 12px; border-radius: 6px;
    background: transparent; border: 1px solid var(--border); color: var(--text-muted);
    font-size: 11.5px; cursor: pointer; display: inline-flex; align-items: center; gap: 4px; transition: all 0.15s; }
  .overview-bar .toggle:hover { color: var(--text); border-color: var(--primary); }
  .overview-bar .toggle svg { transition: transform 0.2s; }
  .overview-bar.expanded .toggle svg { transform: rotate(180deg); }

  /* Expanded panel (KPI + insight + 二级 + charts) */
  .expanded-panel { display: none; padding: 12px 0 0; }
  .expanded-panel.show { display: block; }

  .kpi-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-bottom: 12px; }
  .kpi-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 12px 14px; transition: border-color 0.15s; min-height: 86px; }
  .kpi-card:hover { border-color: var(--primary); }
  .kpi-card .label { color: var(--text-muted); font-size: 11px; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
  .kpi-card .big { font-family: var(--font-mono); font-weight: 600; font-size: 26px;
    line-height: 1.1; letter-spacing: -0.02em; color: var(--text); }
  .kpi-card .big.green { color: var(--up); }
  .kpi-card .big.purple { color: var(--purple); }
  .kpi-card .sub { font-size: 11px; color: var(--text-faint); margin-top: 2px; }

  .insight { background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(168,85,247,0.06));
    border: 1px solid rgba(99,102,241,0.3); border-left: 3px solid var(--primary);
    border-radius: 10px; padding: 11px 14px; margin-bottom: 12px; font-size: 12.5px; }
  .insight .title { font-weight: 600; margin-bottom: 4px; }
  .insight ul { margin: 4px 0; padding-left: 18px; color: var(--text-muted); font-size: 12px; }
  .insight ul li { margin: 2px 0; }

  .stat-row { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 0;
    border-top: 1px dashed var(--border); margin-bottom: 12px; align-items: center; font-size: 12px; color: var(--text-muted); }
  .stat-row .lbl { color: var(--text-faint); font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.04em; margin-right: 4px; }
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

  .charts { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
  .chart-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 12px; }
  .chart-card .ttl { font-size: 11.5px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
  .chart-card .desc { font-size: 10.5px; color: var(--text-faint); margin-bottom: 8px; }
  .chart-card svg { width: 100%; height: 180px; display: block; }

  /* ========== Layout (sidebar + main) ========== */
  .layout { max-width: 1440px; margin: 0 auto; display: flex; align-items: flex-start; }
  .sidebar { width: var(--sidebar-w); flex-shrink: 0;
    background: var(--card); border-right: 1px solid var(--border);
    position: sticky; top: var(--header-h);
    max-height: calc(100vh - var(--header-h)); overflow-y: auto;
    padding: 16px; }
  .sidebar h4 { font-size: 11px; color: var(--text-faint);
    text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; margin: 14px 0 8px; }
  .sidebar h4:first-child { margin-top: 0; }

  .result-count { padding: 10px 14px; border-radius: 8px; background: var(--primary-bg);
    color: var(--primary-text); font-size: 14px; font-weight: 600; border: 1px solid var(--primary);
    text-align: center; margin-bottom: 12px; }
  .result-count.warn { background: var(--orange-bg); color: var(--orange-text); border-color: var(--warn); }
  .result-count.alert { background: var(--red-bg); color: var(--red-text); border-color: var(--down); }

  /* Presets */
  .presets { display: flex; flex-direction: column; gap: 6px; }
  .preset-btn { padding: 9px 12px; border-radius: 8px; border: 1px solid var(--border);
    background: var(--card-hover); color: var(--text-muted); font-size: 12.5px; font-weight: 500;
    text-align: left; transition: all 0.15s; min-height: 38px; }
  .preset-btn:hover { border-color: var(--primary); color: var(--text); }
  .preset-btn.active { background: var(--primary-bg); color: var(--primary-text); border-color: var(--primary); font-weight: 600; }

  .filters-stack { display: flex; flex-direction: column; gap: 8px; }

  .actions-stack { display: flex; flex-direction: column; gap: 6px; }

  /* Selected chips in sidebar */
  .selected-stack { display: flex; flex-direction: column; gap: 4px; }
  .selected-stack .chip { font-size: 11.5px; }

  /* Main content */
  .main { flex: 1; padding: 18px 24px 80px; min-width: 0; max-width: 100%; overflow: hidden; }

  /* ========== Custom Dropdown V5（多选 + 确定按钮）========== */
  .dd { position: relative; display: block; width: 100%; }
  .dd-btn { width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px;
    background: var(--card-hover); cursor: pointer; font-size: 13px; color: var(--text);
    display: flex; align-items: center; justify-content: space-between; gap: 6px;
    transition: all 0.15s; min-height: 42px; }
  .dd-btn:hover { border-color: var(--border-hover); }
  .dd.open .dd-btn { border-color: var(--primary); }
  .dd-btn .lbl { display: flex; align-items: center; gap: 6px; }
  .dd-btn .count { color: var(--primary); font-weight: 700; }
  .dd-btn .arrow { color: var(--text-muted); transition: transform 0.2s ease; flex-shrink: 0; }
  .dd.open .dd-btn .arrow { transform: rotate(180deg); color: var(--primary); }
  .dd-panel { display: none; position: absolute; top: calc(100% + 6px); left: 0; right: 0;
    background: var(--card); border: 1px solid var(--primary); border-radius: 10px;
    box-shadow: var(--shadow-lg); z-index: 50; max-height: 480px; overflow: hidden;
    display: none; flex-direction: column; }
  .dd.open .dd-panel { display: flex; }
  .dd-panel .head { padding: 10px 14px; border-bottom: 1px solid var(--border);
    color: var(--text-muted); font-size: 11.5px; font-weight: 600; flex-shrink: 0; }
  .dd-panel .body { overflow-y: auto; flex: 1; padding: 4px; }
  .dd-panel .footer { padding: 8px; border-top: 1px solid var(--border); display: flex; gap: 6px; flex-shrink: 0; background: var(--card-hover); }
  .dd-panel .footer button { flex: 1; min-height: 36px; padding: 8px 12px; border-radius: 7px; font-size: 12.5px; font-weight: 600; }
  .dd-panel .footer .btn-cancel { background: transparent; border: 1px solid var(--border); color: var(--text-muted); }
  .dd-panel .footer .btn-cancel:hover { color: var(--text); border-color: var(--border-hover); }
  .dd-panel .footer .btn-apply { background: var(--primary); color: white; border: none; }
  .dd-panel .footer .btn-apply:hover { background: #5557E0; }
  .dd-item { padding: 9px 12px; border-radius: 7px; cursor: pointer; font-size: 13px;
    display: flex; align-items: center; gap: 8px; user-select: none; min-height: 38px; }
  .dd-item:hover { background: var(--card-hover); }
  .dd-item.checked { background: var(--primary-bg); color: var(--primary-text); }
  .dd-item .check { width: 16px; height: 16px; border-radius: 4px; border: 1.5px solid var(--border-hover);
    flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
  .dd-item.checked .check { background: var(--primary); border-color: var(--primary); }
  .dd-item.checked .check::after { content: "✓"; color: white; font-size: 11px; font-weight: 700; }
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
  .chip { padding: 4px 10px; border-radius: 12px; font-size: 11.5px;
    display: inline-flex; align-items: center; gap: 5px; background: var(--card-hover);
    border: 1px solid var(--border); color: var(--text); }
  .chip-x { cursor: pointer; opacity: 0.5; padding: 0 2px; font-size: 11px; }
  .chip-x:hover { opacity: 1; color: var(--down); }
  .chip-impact { color: var(--text-faint); font-size: 10.5px; font-family: var(--font-mono); }
  .chip-clear { background: transparent; border: 1px solid var(--down); color: var(--down);
    cursor: pointer; padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; width: 100%; }
  .chip-relax { background: var(--primary-bg); color: var(--primary-text); border: 1px solid var(--primary);
    cursor: pointer; padding: 5px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; width: 100%; }

  .empty-banner { background: var(--card); border: 1px solid var(--warn); border-radius: 10px;
    padding: 16px; margin-bottom: 16px; }
  .empty-banner .ttl { color: var(--warn); font-weight: 600; margin-bottom: 8px; font-size: 13px; }
  .empty-banner button { display: block; width: 100%; background: var(--card-hover);
    border: 1px solid var(--border-hover); color: var(--text); padding: 8px 12px;
    border-radius: 8px; text-align: left; font-size: 12px; margin-top: 6px; }
  .empty-banner button:hover { border-color: var(--primary); }

  /* Theme switcher */
  .theme-switch { display: flex; gap: 4px; padding: 4px; border-radius: 10px; background: var(--card-hover); border: 1px solid var(--border); }
  .theme-switch button { flex: 1; padding: 6px 8px; border-radius: 7px; background: transparent;
    border: none; color: var(--text-muted); font-size: 11.5px; cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 4px; min-height: 32px; }
  .theme-switch button:hover { color: var(--text); }
  .theme-switch button.active { background: var(--primary); color: white; font-weight: 600; }

  /* btn */
  .btn { padding: 9px 14px; border: 1px solid var(--border); border-radius: 8px;
    background: var(--card-hover); color: var(--text); font-size: 13px;
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    min-height: 38px; transition: all 0.15s; width: 100%; }
  .btn:hover { background: var(--card); border-color: var(--border-hover); }
  .btn-primary { background: var(--primary); color: white; border-color: var(--primary); }
  .btn-primary:hover { background: #5557E0; }
  .btn-danger { color: var(--down); border-color: var(--border); }
  .btn-danger:hover { border-color: var(--down); }

  /* Compare board */
  .compare-board { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px; margin-bottom: 16px; }
  .ccard { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
    padding: 14px; position: relative; transition: border-color 0.15s; cursor: pointer; }
  .ccard:hover { border-color: var(--primary); }
  .ccard.is-self { border-color: var(--rose); }
  .ccard .head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .ccard .head .name { font-weight: 600; font-size: 13px; }
  .ccard .self-tag { background: var(--rose-bg); color: var(--rose-text); padding: 1px 7px;
    border-radius: 4px; font-size: 10px; font-weight: 700; border: 1px solid var(--rose); }
  .ccard .subs { color: var(--text-faint); font-size: 11px; font-family: var(--font-mono); margin-bottom: 8px; }
  .ccard .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px; }
  .ccard .cell { color: var(--text-faint); font-size: 10.5px; }
  .ccard .cell b { display: block; font-family: var(--font-mono); font-size: 15px; color: var(--text); font-weight: 600; line-height: 1.2; }
  .ccard .cell .rank { font-size: 11px; margin-left: 3px; }
  .ccard .score-row { display: flex; align-items: center; gap: 6px; font-size: 10.5px; color: var(--text-faint); }
  .ccard .score-bar { flex: 1; height: 5px; background: var(--border); border-radius: 3px; overflow: hidden; }
  .ccard .score-bar > span { display: block; height: 100%; background: var(--primary); }
  .ccard .score-num { font-family: var(--font-mono); font-weight: 600; color: var(--text); }
  .ccard .close { position: absolute; top: 6px; right: 6px; width: 22px; height: 22px; border-radius: 11px;
    background: var(--card-hover); border: none; color: var(--text-faint); cursor: pointer;
    display: flex; align-items: center; justify-content: center; font-size: 11px; }

  /* Bulk bar */
  .bulk-bar { background: var(--card); border: 1px solid var(--primary); border-radius: 10px;
    padding: 10px 14px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
    flex-wrap: wrap; }
  .bulk-bar .selected-count { color: var(--primary-text); font-weight: 600; }
  .bulk-bar .btn { width: auto; }

  /* Grid */
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 16px; }
  .grid.list-view { grid-template-columns: 1fr; gap: 8px; }
  .grid.inspire-view { grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 20px; }

  .empty { text-align: center; color: var(--text-muted); padding: 60px 0; font-size: 14px; grid-column: 1/-1; }

  /* Video Card */
  .video-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    overflow: hidden; box-shadow: var(--shadow); display: flex; flex-direction: column;
    transition: all 0.2s ease; position: relative; }
  .video-card:hover { transform: translateY(-2px); border-color: var(--border-hover); }
  .video-card.is-self { border-color: var(--rose); }
  .video-card.hot-million { border-color: rgba(239,68,68,0.5); }
  .video-card.hot-phenom { border-color: var(--purple); box-shadow: 0 0 0 1px rgba(168,85,247,0.3), var(--shadow); }
  .video-card .bulk-cb { position: absolute; left: 12px; top: 12px; z-index: 3;
    width: 26px; height: 26px; background: rgba(10,14,26,0.85); backdrop-filter: blur(6px);
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
    border-radius: 10px; font-size: 11px; font-weight: 600;
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
  .hot-chip.rising { background: rgba(239,68,68,0.85); color: white; }
  .hot-chip.strong { background: rgba(245,158,11,0.85); color: white; }
  .hot-chip.million { background: rgba(239,68,68,0.85); color: white; }
  .hot-chip.phenom { background: rgba(168,85,247,0.85); color: white; }

  .fav-btn { position: absolute; top: 10px; right: 10px; z-index: 2;
    width: 38px; height: 38px; min-width: 38px; min-height: 38px; border-radius: 19px;
    background: rgba(10,14,26,0.85); backdrop-filter: blur(8px); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center;
    color: var(--text-muted); transition: all 0.15s; }
  .fav-btn:hover { color: var(--warn); transform: scale(1.06); border-color: var(--warn); }
  .fav-btn.active { color: var(--warn); background: rgba(245,158,11,0.2); border-color: var(--warn); }
  .hide-btn { position: absolute; top: 10px; right: 56px; z-index: 2;
    width: 32px; height: 32px; border-radius: 16px;
    background: rgba(10,14,26,0.85); backdrop-filter: blur(8px); border: 1px solid var(--border);
    color: var(--text-faint); font-size: 14px; opacity: 0; transition: opacity 0.15s; display: flex;
    align-items: center; justify-content: center; }
  .video-card:hover .hide-btn { opacity: 1; }

  .card-body { padding: 14px; flex: 1; display: flex; flex-direction: column; gap: 8px; }
  .card-row1 { display: flex; align-items: center; gap: 6px; font-size: 11.5px;
    color: var(--text-muted); flex-wrap: wrap; }
  .card-row1 .channel-name { color: var(--text); font-weight: 500; }
  .card-row1 .grp { padding: 1px 7px; border-radius: 5px; background: var(--gray-bg);
    color: var(--gray-text); font-size: 10.5px; font-weight: 500; }
  .card-row1 .self { padding: 1px 7px; border-radius: 5px; background: var(--rose-bg);
    color: var(--rose-text); font-size: 10.5px; font-weight: 700; border: 1px solid var(--rose); }
  .card-row1 .vtype { padding: 1px 7px; border-radius: 5px; background: var(--card-hover);
    color: var(--text-muted); font-size: 10.5px; }

  .card-title { color: var(--text); font-size: 14.5px; font-weight: 600; line-height: 1.4;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical; display: -webkit-box; overflow: hidden;
    min-height: 40px; letter-spacing: -0.01em; }
  .card-title:hover { color: var(--primary-text); }

  .biz-signal { display: flex; align-items: baseline; gap: 8px; padding: 8px 0;
    border-top: 1px dashed var(--border); }
  .biz-signal .er-num { font-size: 24px; font-weight: 700; font-family: var(--font-mono); line-height: 1; letter-spacing: -0.02em; }
  .biz-signal .er-label { font-size: 11px; color: var(--text-faint); cursor: help;
    border-bottom: 1px dotted var(--text-faint); }
  .biz-signal .deltas { margin-left: auto; display: flex; gap: 8px; font-size: 10.5px; color: var(--text-faint); font-family: var(--font-mono); }
  .biz-signal .delta.pos { color: var(--up); }
  .biz-signal .delta.neg { color: var(--down); }

  .card-stats { display: flex; gap: 12px; align-items: center; font-size: 11.5px; color: var(--text-muted); }
  .card-stats .item { display: inline-flex; align-items: center; gap: 5px; }
  .card-stats .num { color: var(--text); font-family: var(--font-mono); font-weight: 500; font-size: 12.5px; }

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
    padding: 22px; margin-bottom: 16px; }
  .panel h3 { margin: 0 0 12px; font-size: 15px; font-weight: 600; }
  .panel table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .panel th { text-align: left; padding: 10px 12px; color: var(--text-muted);
    font-weight: 500; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em;
    border-bottom: 1px solid var(--border); }
  .panel td { padding: 11px 12px; border-bottom: 1px solid var(--border); font-family: var(--font-mono); font-size: 13px; }
  .panel td.name { font-family: var(--font-sans); font-weight: 600; font-size: 14px; }
  .panel tr:last-child td { border-bottom: none; }
  .bar { height: 6px; background: var(--border); border-radius: 3px; overflow: hidden;
    min-width: 80px; max-width: 200px; display: inline-block; vertical-align: middle; margin-left: 8px; }
  .bar > span { display: block; height: 100%; background: var(--primary); }

  .history-empty { padding: 40px 0; text-align: center; color: var(--text-muted); }
  .history-empty .big { font-size: 16px; color: var(--text); margin-bottom: 8px; font-weight: 500; }
  .progress { height: 6px; background: var(--border); border-radius: 3px; overflow: hidden;
    max-width: 320px; margin: 14px auto; }
  .progress > span { display: block; height: 100%; background: var(--primary); }

  /* Tooltip */
  [data-tip] { position: relative; }
  [data-tip]:hover::after { content: attr(data-tip); position: absolute; bottom: 100%; left: 50%;
    transform: translateX(-50%) translateY(-6px); background: var(--card-hover); color: var(--text);
    padding: 6px 10px; border-radius: 6px; font-size: 11px; white-space: nowrap;
    box-shadow: var(--shadow); z-index: 999; border: 1px solid var(--border); pointer-events: none; }

  .workflow-banner { background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(168,85,247,0.05));
    border: 1px solid rgba(99,102,241,0.3); border-radius: 12px; padding: 14px 16px; margin-bottom: 16px;
    position: relative; }
  .workflow-banner h4 { margin: 0 0 6px; font-size: 13px; font-weight: 600; }
  .workflow-banner ol { margin: 0; padding-left: 20px; color: var(--text-muted); font-size: 12px; }
  .workflow-banner .close-x { position: absolute; top: 8px; right: 8px; cursor: pointer;
    color: var(--text-faint); padding: 4px 8px; }

  .toast { position: fixed; right: 20px; bottom: 80px; z-index: 300;
    background: var(--card-hover); color: var(--text); padding: 12px 16px; border-radius: 12px;
    font-size: 13px; font-weight: 500; box-shadow: var(--shadow-lg); border: 1px solid var(--border-hover);
    transform: translateY(80px); opacity: 0; transition: all 0.25s; max-width: 420px;
    display: flex; align-items: center; gap: 12px; }
  .toast.show { transform: translateY(0); opacity: 1; }
  .toast .toast-msg { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .toast .toast-action { background: var(--primary); color: white; border: none;
    padding: 6px 12px; border-radius: 6px; font-size: 12.5px; font-weight: 600; cursor: pointer; flex-shrink: 0; }
  .toast .toast-action:hover { background: #5557E0; }
  .toast .toast-countdown { color: var(--text-faint); font-size: 11px; font-family: var(--font-mono); flex-shrink: 0; }

  /* Mobile */
  .mobile-bar { display: none; }
  .mobile-overlay { display: none; }
  .mobile-drawer { display: none; }

  @media (max-width: 1280px) {
    .kpi-grid { grid-template-columns: repeat(3, 1fr); }
    .charts { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 1024px) {
    .sidebar { display: none; }
    .main { padding: 16px 16px 100px; }
  }
  @media (max-width: 768px) {
    .container { padding: 12px 16px 6px; }
    .hero h1 { font-size: 17px; }
    .hero .subtitle { font-size: 12px; }
    .meta-line { font-size: 10.5px; gap: 8px; }
    .kpi-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
    .kpi-card { padding: 10px; min-height: 78px; }
    .kpi-card .big { font-size: 22px; }
    .charts { grid-template-columns: 1fr; }
    .grid { grid-template-columns: 1fr; gap: 12px; }
    .compare-board { grid-template-columns: 1fr 1fr; }
    .stat-row { font-size: 11.5px; padding: 8px 0; }
    .tabs { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
    .tab { flex-shrink: 0; }
    .insight { padding: 10px 12px; }
    .overview-bar { font-size: 11.5px; gap: 8px; }
    .overview-bar .key { display: none; }

    .mobile-bar { display: flex; position: fixed; bottom: 0; left: 0; right: 0;
      background: var(--bg); backdrop-filter: saturate(180%) blur(20px);
      border-top: 1px solid var(--border); padding: 8px 12px;
      padding-bottom: calc(8px + env(safe-area-inset-bottom));
      z-index: 99; gap: 6px; }
    .mobile-bar .btn { flex: 1; min-height: 44px; font-size: 12.5px; padding: 6px 8px; }
    .mobile-bar .count-badge { background: var(--primary); color: white; padding: 1px 6px;
      border-radius: 9px; font-size: 10px; font-weight: 700; margin-left: 4px; }

    .mobile-overlay { display: block; position: fixed; inset: 0; background: rgba(0,0,0,0.6);
      z-index: 200; opacity: 0; pointer-events: none; transition: opacity 0.2s; }
    .mobile-overlay.show { opacity: 1; pointer-events: auto; }
    .mobile-drawer { display: flex; flex-direction: column; position: fixed;
      bottom: 0; left: 0; right: 0; max-height: 80vh;
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
    .mobile-drawer-content .dd-panel { position: static; box-shadow: none;
      border: 1px solid var(--border); margin-top: 6px; max-height: 300px; }
    .mobile-drawer-actions { padding: 12px 16px; border-top: 1px solid var(--border);
      display: flex; gap: 8px; flex-shrink: 0; background: var(--card); }
    .mobile-drawer-actions .btn { flex: 1; min-height: 46px; font-weight: 600; }

    .toast { right: 16px; left: 16px; bottom: 80px; text-align: center; }
  }
</style>
</head>
<body>
<header>
  <div class="container">
    <div class="hero">
      <h1>YT<span class="dot">·</span>INTEL</h1>
      <div class="subtitle">北美 iPad 配件类目 · 56 频道 · 8 维度数据</div>
      <div class="meta-line">
        <span><span class="live-dot"></span>自动刷新已开</span>
        <span>数据 <b id="gen-at">—</b> <span id="gen-ago"></span></span>
        <span>频道 <b id="ch-count">—</b></span>
        <span>视频 <b id="vid-count">—</b></span>
      </div>
    </div>

    <nav class="tabs" id="tabs"></nav>

    <div class="overview-bar" id="overview-bar"></div>

    <div class="expanded-panel" id="expanded-panel">
      <div id="kpi-grid" class="kpi-grid"></div>
      <div id="insight" class="insight" style="display:none"></div>
      <div id="stat-row" class="stat-row"></div>
      <div id="charts-root" class="charts"></div>
    </div>
  </div>
</header>

<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div id="sidebar-content"></div>
  </aside>
  <main class="main" id="main">
    <div id="view-home"></div>
    <div id="view-favorites" style="display:none"></div>
    <div id="view-brand" style="display:none"></div>
    <div id="view-history" style="display:none"></div>
    <div id="view-monitor" style="display:none"></div>
    <div id="view-hidden" style="display:none"></div>
  </main>
</div>

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
const STORAGE_KEY = 'yt-tracker-v5';
const FAV_KEY = 'yt-tracker-favorites-v5';
const HIDE_KEY = 'yt-tracker-hidden-v5';
const TEARDOWN_KEY = 'yt-tracker-teardown-v5';

let DATA = null;
let HISTORY = null;
let state = loadState();
let pendingMobileState = null;
let bulkMode = false;
let bulkSelected = new Set();

function defaultFilters() {
  return { time: 'all', groups: [], channels: [], contents: [], lengths: [], hots: [], vtypes: [], brands: [] };
}
function defaultState() {
  return { tab: 'home', filters: defaultFilters(), sort: 'er', expanded_groups: [], view_mode: 'grid', preset: '', overview_expanded: false, workflow_banner_dismissed: false };
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
let _toastTimer = null;
let _toastCountdown = null;
function showToast(msg, opts={}) {
  const { actionLabel, onAction, duration = 3000 } = opts;
  const t = document.getElementById('toast');
  if (_toastTimer) { clearTimeout(_toastTimer); _toastTimer = null; }
  if (_toastCountdown) { clearInterval(_toastCountdown); _toastCountdown = null; }
  let html = `<span class="toast-msg">${escHTML(msg)}</span>`;
  if (actionLabel) {
    html += `<button class="toast-action">${escHTML(actionLabel)}</button>`;
    html += `<span class="toast-countdown">${Math.ceil(duration/1000)}s</span>`;
  }
  t.innerHTML = html;
  t.classList.add('show');
  if (actionLabel) {
    const btn = t.querySelector('.toast-action');
    btn.onclick = () => {
      if (onAction) onAction();
      t.classList.remove('show');
      if (_toastTimer) clearTimeout(_toastTimer);
      if (_toastCountdown) clearInterval(_toastCountdown);
    };
    let remain = Math.ceil(duration/1000);
    const cdEl = t.querySelector('.toast-countdown');
    _toastCountdown = setInterval(() => {
      remain -= 1;
      if (cdEl) cdEl.textContent = remain + 's';
      if (remain <= 0) clearInterval(_toastCountdown);
    }, 1000);
  }
  _toastTimer = setTimeout(() => t.classList.remove('show'), duration);
}
function withinTime(iso, key) {
  if (key === 'all') return true;
  const days = parseFloat(key);
  if (!isFinite(days) || days <= 0) return true;
  const t = new Date(iso).getTime();
  if (!isFinite(t)) return true;
  return (Date.now() - t) <= days * 86400000;
}

const ICONS = {
  play: '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
  thumb: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 22V11M2 13h5v9H4a2 2 0 01-2-2v-7zM7 11l5-9 1 1c.6.5.9 1.3.9 2v3h6a2 2 0 012 2l-2 7a2 2 0 01-2 2h-7"/></svg>',
  comment: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
  star_o: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2l2.4 7h7.6l-6.2 4.5L18.2 21 12 16.5 5.8 21l2.4-7.5L2 9h7.6z"/></svg>',
  star: '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l2.4 7h7.6l-6.2 4.5L18.2 21 12 16.5 5.8 21l2.4-7.5L2 9h7.6z"/></svg>',
  download: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v12m0 0l-5-5m5 5l5-5M4 20h16"/></svg>',
  chevron: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
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
    if (f.contents.length) { const tags = v.content_tags || []; if (!f.contents.some(c => tags.includes(c))) return false; }
    if (f.lengths.length && !f.lengths.includes(v.video_length_type)) return false;
    if (f.hots.length && !f.hots.includes(v.hot_level)) return false;
    if (f.vtypes.length && !f.vtypes.includes(v.video_type)) return false;
    if (f.brands.length) { const bms = v.brand_mentions || []; if (!f.brands.some(b => bms.includes(b))) return false; }
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

// ========== V5: Multi-Select Dropdown (tempSelected + 确定按钮) ==========
function makeDropdown({ label, options, multi, getSelected, onApply, withCount=false }) {
  const wrap = document.createElement('span');
  wrap.className = 'dd';
  wrap.innerHTML = `<button class="dd-btn"><span class="lbl"></span><span class="arrow">${ICONS.chevron}</span></button><div class="dd-panel"></div>`;
  const btn = wrap.querySelector('.dd-btn');
  const lblEl = btn.querySelector('.lbl');
  const panel = wrap.querySelector('.dd-panel');
  let temp = null; // 临时选择（多选用 array）

  function refreshBtn() {
    const sel = getSelected();
    let txt = label;
    if (multi) {
      const arr = sel || [];
      if (arr.length > 0) txt += ` <span class="count">(${arr.length})</span>`;
    } else {
      const o = options.find(o => (o.value||o) === sel);
      if (o && (o.value||o) !== 'all') txt += `: <span class="count">${o.label||o}</span>`;
    }
    lblEl.innerHTML = txt;
  }
  function renderPanel() {
    panel.innerHTML = '';
    // head
    const head = document.createElement('div');
    head.className = 'head';
    if (multi) {
      head.innerHTML = `<span>${escHTML(label)}${(temp||[]).length > 0 ? ` · ${temp.length} 个临时选` : ''}</span>`;
    } else {
      head.innerHTML = `<span>${escHTML(label)} · 选一个</span>`;
    }
    panel.appendChild(head);
    // body
    const body = document.createElement('div');
    body.className = 'body';
    options.forEach(opt => {
      const isObj = (opt && typeof opt === 'object');
      const v = isObj ? opt.value : opt;
      const lbl = isObj ? opt.label : opt;
      const checked = multi ? temp.includes(v) : (temp === v);
      const item = document.createElement('div');
      item.className = 'dd-item' + (checked ? ' checked' : '');
      item.innerHTML = (multi ? '<span class="check"></span>' : '') + `<span>${escHTML(lbl)}</span>`;
      item.onclick = (e) => {
        e.stopPropagation();
        if (multi) {
          const i = temp.indexOf(v);
          if (i >= 0) temp.splice(i, 1); else temp.push(v);
          renderPanel();
        } else {
          temp = v;
          // 单选直接 apply + close
          onApply(temp);
          wrap.classList.remove('open');
          refreshBtn();
        }
      };
      body.appendChild(item);
    });
    panel.appendChild(body);
    // footer (multi only)
    if (multi) {
      const foot = document.createElement('div');
      foot.className = 'footer';
      foot.innerHTML = `<button class="btn-cancel">取消</button><button class="btn-apply">确定 (${temp.length})</button>`;
      foot.querySelector('.btn-cancel').onclick = e => { e.stopPropagation(); close(false); };
      foot.querySelector('.btn-apply').onclick = e => { e.stopPropagation(); close(true); };
      panel.appendChild(foot);
    }
  }
  function open() {
    if (multi) temp = (getSelected() || []).slice();
    else temp = getSelected();
    wrap.classList.add('open');
    renderPanel();
  }
  function close(apply) {
    wrap.classList.remove('open');
    if (apply && multi) onApply(temp.slice());
    refreshBtn();
  }
  wrap._cancel = () => close(false);
  btn.onclick = (e) => {
    e.stopPropagation();
    document.querySelectorAll('.dd.open').forEach(d => { if (d !== wrap && d._cancel) d._cancel(); });
    if (wrap.classList.contains('open')) close(false);
    else open();
  };
  refreshBtn();
  return { el: wrap, refresh: () => { refreshBtn(); if (wrap.classList.contains('open')) renderPanel(); } };
}

function makeChannelTreeDropdown({ getGroups, getChannels, onApply }) {
  // 频道树也用 tempSelected + 确定
  const wrap = document.createElement('span');
  wrap.className = 'dd';
  wrap.innerHTML = `<button class="dd-btn"><span class="lbl"></span><span class="arrow">${ICONS.chevron}</span></button><div class="dd-panel"></div>`;
  const btn = wrap.querySelector('.dd-btn');
  const lblEl = btn.querySelector('.lbl');
  const panel = wrap.querySelector('.dd-panel');
  let tempG = [];
  let tempC = [];

  function refreshBtn() {
    const cnt = (getGroups()||[]).length + (getChannels()||[]).length;
    lblEl.innerHTML = '频道分组' + (cnt ? ` <span class="count">(${cnt})</span>` : '');
  }
  function renderPanel() {
    panel.innerHTML = '';
    const head = document.createElement('div');
    head.className = 'head';
    head.innerHTML = `<span>频道分组 · ${tempG.length + tempC.length} 个临时选 · 点 ▸ 展开看子频道</span>`;
    panel.appendChild(head);
    const body = document.createElement('div');
    body.className = 'body';
    Object.entries(CFG.group_labels).forEach(([gKey, gLabel]) => {
      const isChecked = tempG.includes(gKey);
      const isExp = state.expanded_groups.includes(gKey);
      const cnt = (CFG.channel_tree[gKey]||[]).length;
      const item = document.createElement('div');
      item.className = 'dd-item' + (isChecked ? ' checked' : '') + (isExp ? ' exp' : '');
      item.innerHTML = `<span class="check"></span><span style="font-weight:500">${escHTML(gLabel)}</span><span class="subs">${cnt}</span><span class="arrow-r">▸</span>`;
      item.onclick = (e) => {
        e.stopPropagation();
        if (e.target.classList.contains('arrow-r')) {
          const cur = state.expanded_groups.slice();
          const i = cur.indexOf(gKey);
          if (i >= 0) cur.splice(i, 1); else cur.push(gKey);
          state.expanded_groups = cur; saveState();
        } else {
          const i = tempG.indexOf(gKey);
          if (i >= 0) tempG.splice(i, 1); else tempG.push(gKey);
        }
        renderPanel();
      };
      body.appendChild(item);
      if (isExp) {
        const cw = document.createElement('div');
        cw.className = 'dd-children';
        (CFG.channel_tree[gKey]||[]).forEach(ch => {
          const cn = ch.display_name;
          const checked = tempC.includes(cn);
          const c = document.createElement('div');
          c.className = 'dd-child' + (checked ? ' checked' : '');
          c.innerHTML = `<span class="check"></span><span>${escHTML(cn)}</span>`
            + (ch.is_self ? '<span class="self">⭐ 自家</span>' : '')
            + `<span class="subs">${fmt(ch.subscriber_count)}</span>`;
          c.onclick = (e) => {
            e.stopPropagation();
            const i = tempC.indexOf(cn);
            if (i >= 0) tempC.splice(i, 1); else tempC.push(cn);
            renderPanel();
          };
          cw.appendChild(c);
        });
        body.appendChild(cw);
      }
    });
    panel.appendChild(body);
    const foot = document.createElement('div');
    foot.className = 'footer';
    foot.innerHTML = `<button class="btn-cancel">取消</button><button class="btn-apply">确定 (${tempG.length + tempC.length})</button>`;
    foot.querySelector('.btn-cancel').onclick = e => { e.stopPropagation(); close(false); };
    foot.querySelector('.btn-apply').onclick = e => { e.stopPropagation(); close(true); };
    panel.appendChild(foot);
  }
  function open() {
    tempG = (getGroups()||[]).slice();
    tempC = (getChannels()||[]).slice();
    wrap.classList.add('open');
    renderPanel();
  }
  function close(apply) {
    wrap.classList.remove('open');
    if (apply) onApply(tempG.slice(), tempC.slice());
    refreshBtn();
  }
  wrap._cancel = () => close(false);
  btn.onclick = (e) => {
    e.stopPropagation();
    document.querySelectorAll('.dd.open').forEach(d => { if (d !== wrap && d._cancel) d._cancel(); });
    if (wrap.classList.contains('open')) close(false);
    else open();
  };
  refreshBtn();
  return { el: wrap, refresh: () => { refreshBtn(); if (wrap.classList.contains('open')) renderPanel(); } };
}

document.addEventListener('click', e => {
  if (!e.target.closest('.dd')) {
    document.querySelectorAll('.dd.open').forEach(d => d._cancel && d._cancel());
  }
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelectorAll('.dd.open').forEach(d => d._cancel && d._cancel());
});

// ========== Tabs ==========
function renderTabs() {
  const favCount = getFavs().length;
  const hiddenCount = getHidden().length;
  const items = [
    { key: 'home', label: '首页' },
    { key: 'favorites', label: '拆解清单', badge: favCount > 0 ? favCount : null },
    { key: 'brand', label: '品牌对比' },
    { key: 'history', label: '历史趋势' },
    { key: 'monitor', label: '竞品监测' },
    { key: 'hidden', label: '已隐藏', badge: hiddenCount > 0 ? hiddenCount : null },
  ];
  document.getElementById('tabs').innerHTML = items.map(t =>
    `<button class="tab${t.key === state.tab ? ' active' : ''}" data-tab="${t.key}">${t.label}${t.badge != null ? `<span class="tab-badge">${t.badge}</span>` : ''}</button>`
  ).join('');
  document.querySelectorAll('.tab').forEach(b => b.onclick = () => { state.tab = b.dataset.tab; saveState(); render(); });
}

// ========== Overview Bar (折叠 / 展开) ==========
function renderOverviewBar(filtered) {
  const root = document.getElementById('overview-bar');
  const total = filtered.reduce((s,v) => s + (v.view_count||0), 0);
  const avgER = filtered.length ? filtered.reduce((s,v) => s + (v.engagement_rate||0), 0) / filtered.length : 0;
  const highER = filtered.filter(v => (v.engagement_rate||0) >= 5).length;
  const phenom = filtered.filter(v => v.hot_level === '🚀 现象级').length;

  root.classList.toggle('expanded', state.overview_expanded);
  root.innerHTML = `
    <span class="key">📊 概览</span>
    <span>视频 <b>${filtered.length}</b></span>
    <span>总播放 <b>${fmt(total)}</b></span>
    <span>ER <b>${avgER.toFixed(2)}%</b></span>
    <span>高 ER <b>${highER}</b></span>
    <span style="color:var(--purple)">现象级 <b style="color:var(--purple)">${phenom}</b></span>
    <button class="toggle">${state.overview_expanded ? '收起' : '展开详情'} ${ICONS.chevron}</button>
  `;
  root.querySelector('.toggle').onclick = () => {
    state.overview_expanded = !state.overview_expanded;
    saveState();
    render();
    setTimeout(updateHeaderHeight, 0);
  };
  document.getElementById('expanded-panel').classList.toggle('show', state.overview_expanded);
}

// ========== Header height for sticky sidebar ==========
function updateHeaderHeight() {
  const h = document.querySelector('header').offsetHeight;
  document.documentElement.style.setProperty('--header-h', h + 'px');
}

// ========== KPI ==========
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
    <div class="kpi-card" data-tip="Engagement Rate · 互动率 · (赞+评论)/播放 · >5% 优秀 / 2-5% 一般 / <2% 较差"><div class="label">平均 ER</div><div class="big ${erColor}">${avgER.toFixed(2)}<span style="font-size:14px;color:var(--text-muted);">%</span></div><div class="sub">悬停看说明</div></div>
    <div class="kpi-card"><div class="label">高 ER 内容</div><div class="big">${highER}</div><div class="sub">≥5% 互动率</div></div>
    <div class="kpi-card"><div class="label">本周新视频</div><div class="big">${week.length}</div><div class="sub">${week100k} 个 &gt;10万</div></div>
    <div class="kpi-card"><div class="label">现象级爆款</div><div class="big purple">${phenom}</div><div class="sub">&gt;500万播放</div></div>
  `;
}

// V6 智能洞察：4 层结构（事实 / 对比 / 含义 / 建议）
function generateInsights(filtered) {
  const out = [];
  const week = filtered.filter(v => withinTime(v.published_at, '7'));

  // 1) 创作类（P2）vs 总体
  const allCreate = filtered.filter(v => (v.content_tags||[]).includes('创作'));
  if (allCreate.length >= 5) {
    const allER = allCreate.reduce((s,v) => s+(v.engagement_rate||0), 0) / allCreate.length;
    const overallER = filtered.length ? filtered.reduce((s,v) => s+(v.engagement_rate||0),0) / filtered.length : 0;
    const diff = overallER ? ((allER - overallER) / overallER * 100) : 0;
    const topCh = [...new Set(allCreate.sort((a,b) => (b.engagement_rate||0)-(a.engagement_rate||0)).map(v => v.channel_name))].slice(0, 3);
    out.push({
      title: '创作类内容（P2 人群）',
      data: `ER ${allER.toFixed(2)}% · ${allCreate.length} 条视频`,
      compare: `比总体 ${diff >= 0 ? '+' : ''}${diff.toFixed(0)}%${HISTORY && HISTORY.count < 7 ? ' · 跨周对比待积累' : ''}`,
      meaning: diff >= 15 ? 'P2 创作人群活跃度高 · 内容质量好' : diff <= -15 ? 'P2 创作类供给疲软' : 'P2 创作类表现稳定',
      action: diff >= 15 ? `本周内容向创作场景倾斜 · 优先合作: ${topCh.join(' / ')}` : '保持基线投入',
    });
  }

  // 2) iPad 配件相关供给
  const ipadAcc = filtered.filter(v => (v.content_tags||[]).includes('iPad配件相关'));
  out.push({
    title: 'iPad 配件相关视频供给',
    data: `${ipadAcc.length} 条视频`,
    compare: ipadAcc.length === 0 ? '类目空白' : ipadAcc.length <= 10 ? '供给量低（<10 条）' : `供给充足`,
    meaning: ipadAcc.length <= 10 ? '类目蓝海 · 内容竞争小但需求存在' : '类目饱和度高',
    action: ipadAcc.length <= 10 ? '加大 iPad 配件评测/装机/教程内容产出 · 抢占 SEO 长尾' : '差异化切入（场景/人群/价位）',
  });

  // 3) 头部 KOL 本周动态
  const kolWeek = week.filter(v => CFG.top_kol.includes(v.channel_name));
  if (kolWeek.length) {
    const top = kolWeek.sort((a,b) => (b.view_count||0)-(a.view_count||0))[0];
    out.push({
      title: '头部 KOL 本周动态',
      data: `${kolWeek.length} 条视频 · ${[...new Set(kolWeek.map(v=>v.channel_name))].length} 个 KOL`,
      compare: `Top 1: ${top.channel_name} ${fmt(top.view_count)} 播放`,
      meaning: '风向标观察 · 头部 KOL 选题往往领先 1-2 周',
      action: top ? `跟进 ${top.channel_name} 最新内容选题 · 24h 内复用爆款 hook` : '持续监测',
    });
  }

  // 4) 竞品 A 组本周破百万
  const aHot = week.filter(v => v.channel_group === 'A_brand' && v.view_count >= 1e6);
  if (aHot.length) {
    out.push({
      title: '直接竞品 A 组本周爆款',
      data: `${aHot.length} 条破百万`,
      compare: `${aHot.slice(0,2).map(v => v.channel_name + ' ' + fmt(v.view_count)).join(' · ')}`,
      meaning: '竞品高曝光信号 · 可能在做新品/促销/品牌投放',
      action: '即刻拆解 hook + 描述 + CTA · 反向推断竞品策略',
    });
  }

  // 5) 品牌提及（自家被外部讨论的次数）
  const typecaseMentions = filtered.filter(v => (v.brand_mentions||[]).includes('Typecase')).length;
  if (typecaseMentions) {
    out.push({
      title: '自家品牌（Typecase）外部提及',
      data: `${typecaseMentions} 条视频提到 Typecase`,
      compare: `vs 头部竞品（Logitech 提及 ${filtered.filter(v=>(v.brand_mentions||[]).includes('Logitech')).length} 条）`,
      meaning: typecaseMentions > 0 ? '品牌已进入 KOL 视野' : '品牌曝光待提升',
      action: typecaseMentions > 0 ? '发联名/赠测推动更多 KOL 发声' : '加大 KOL 种草投放',
    });
  }
  return out;
}

function renderInsight(filtered) {
  const root = document.getElementById('insight');
  const insights = generateInsights(filtered);
  if (insights.length === 0) { root.style.display = 'none'; return; }
  root.style.display = 'block';
  const cards = insights.map(i => `
    <div style="background:var(--card);border:1px solid var(--border);border-left:3px solid var(--primary);border-radius:8px;padding:10px 14px;margin-top:8px">
      <div style="font-weight:600;font-size:13px;margin-bottom:4px;color:var(--text)">${escHTML(i.title)}</div>
      <div style="font-size:12px;color:var(--text-muted);line-height:1.7">
        <div><span style="color:var(--text-faint);min-width:48px;display:inline-block">数据:</span> ${escHTML(i.data)}</div>
        <div><span style="color:var(--text-faint);min-width:48px;display:inline-block">对比:</span> ${escHTML(i.compare)}</div>
        <div><span style="color:var(--text-faint);min-width:48px;display:inline-block">含义:</span> ${escHTML(i.meaning)}</div>
        <div><span style="color:var(--primary);min-width:48px;display:inline-block">建议:</span> <span style="color:var(--text)">${escHTML(i.action)}</span></div>
      </div>
    </div>`).join('');
  const note = HISTORY && HISTORY.count < 7 ? `<div style="font-size:11px;color:var(--text-faint);margin-top:6px">📊 跨周趋势对比将在 ${7 - HISTORY.count} 天后开启</div>` : '';
  root.innerHTML = `<div class="title">📊 营销情报洞察 · ${insights.length} 条</div>${cards}${note}`;
}

function renderStatRow(filtered) {
  const root = document.getElementById('stat-row');
  const hot = (l) => filtered.filter(v => v.hot_level === l).length;
  const tag = (t) => filtered.filter(v => (v.content_tags||[]).includes(t)).length;
  const high_rel = filtered.filter(v => (v.relevance_score||0) >= 80).length;
  const mid_rel = filtered.filter(v => (v.relevance_score||0) >= 60 && (v.relevance_score||0) < 80).length;
  const low_rel = filtered.filter(v => (v.relevance_score||0) < 60).length;
  let html = '';
  if (hot('🔥 上升爆款') + hot('💥 强爆款') + hot('⭐ 百万爆款') + hot('🚀 现象级') > 0) {
    html += `<span class="lbl">爆款</span>`;
    if (hot('🔥 上升爆款')) html += `<span class="pill rising">🔥 上升 ${hot('🔥 上升爆款')}</span>`;
    if (hot('💥 强爆款'))   html += `<span class="pill strong">💥 强 ${hot('💥 强爆款')}</span>`;
    if (hot('⭐ 百万爆款')) html += `<span class="pill million">⭐ 百万 ${hot('⭐ 百万爆款')}</span>`;
    if (hot('🚀 现象级'))   html += `<span class="pill phenom">🚀 现象级 ${hot('🚀 现象级')}</span>`;
  }
  html += `<span class="lbl" style="margin-left:8px">相关性</span>`;
  html += `<span class="pill high-rel">🎯 高度 ${high_rel}</span>`;
  html += `<span class="pill mid-rel">中等 ${mid_rel}</span>`;
  html += `<span class="pill low-rel">低 ${low_rel}</span>`;
  if (tag('iPad配件相关')) html += `<span class="pill tag-iPad">iPad配件 ${tag('iPad配件相关')}</span>`;
  if (tag('创作'))        html += `<span class="pill tag-creation">创作 ${tag('创作')}</span>`;
  if (tag('学生'))        html += `<span class="pill tag-student">学生 ${tag('学生')}</span>`;
  if (tag('商务'))        html += `<span class="pill tag-business">商务 ${tag('商务')}</span>`;
  root.innerHTML = html;
}

function renderCharts(filtered) {
  const root = document.getElementById('charts-root');
  if (!filtered || filtered.length === 0) { root.innerHTML = ''; return; }
  const lenOrder = CFG.length_order;
  const w1 = 320, h1 = 180, pad = 30;
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
    xlbl1 += `<text x="${x}" y="${h1 - 6}" text-anchor="middle" font-size="10" fill="#94A3B8">${l}</text>`;
  });
  const ylbl1 = `<text x="${pad - 6}" y="${pad}" text-anchor="end" font-size="10" fill="#94A3B8">${erMax.toFixed(0)}%</text><text x="${pad - 6}" y="${h1 - pad}" text-anchor="end" font-size="10" fill="#94A3B8">0%</text>`;
  const axis1 = `<line x1="${pad}" y1="${h1 - pad}" x2="${w1 - pad}" y2="${h1 - pad}" stroke="#1E293B"/><line x1="${pad}" y1="${pad}" x2="${pad}" y2="${h1 - pad}" stroke="#1E293B"/>`;

  const channels = {};
  DATA.videos.forEach(v => {
    if (!channels[v.channel_name]) channels[v.channel_name] = { name: v.channel_name, subs: v.channel_subscriber_count, ers: [] };
    channels[v.channel_name].ers.push(v.engagement_rate || 0);
  });
  const chList = Object.values(channels).map(c => ({ ...c, avgER: c.ers.reduce((s,e) => s+e, 0)/c.ers.length }));
  const w2 = 320, h2 = 180;
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
  const lbl2 = `<text x="${pad - 6}" y="${pad}" text-anchor="end" font-size="10" fill="#94A3B8">${erMax2.toFixed(0)}%</text>`;

  const groupCounts = {};
  Object.keys(CFG.group_labels).forEach(g => groupCounts[g] = 0);
  filtered.forEach(v => groupCounts[v.channel_group] = (groupCounts[v.channel_group]||0) + 1);
  const gMax = Math.max(...Object.values(groupCounts), 1);
  const w3 = 320, h3 = 180;
  const barH = 22, gap = 4;
  let bars = '';
  Object.entries(CFG.group_labels).forEach(([g, lbl], i) => {
    const cnt = groupCounts[g];
    const bw = (cnt / gMax) * (w3 - 130);
    const y = 10 + i * (barH + gap);
    bars += `<text x="6" y="${y + 14}" font-size="11" fill="#CBD5E1">${escHTML(lbl)}</text>`;
    bars += `<rect x="124" y="${y}" width="${bw.toFixed(0)}" height="${barH}" fill="#6366F1" opacity="0.6" rx="3"/>`;
    bars += `<text x="${(124 + bw + 6).toFixed(0)}" y="${y + 14}" font-size="11" fill="#94A3B8" font-family="monospace">${cnt}</text>`;
  });

  root.innerHTML = `
    <div class="chart-card"><div class="ttl">视频长度 × ER</div><div class="desc">看哪种长度容易出高 ER</div><svg viewBox="0 0 ${w1} ${h1}" preserveAspectRatio="xMidYMid meet">${axis1}${ylbl1}${xlbl1}${pts1}</svg></div>
    <div class="chart-card"><div class="ttl">频道 KOL 影响力矩阵</div><div class="desc">右上=顶级 · 玫瑰红=Typecase</div><svg viewBox="0 0 ${w2} ${h2}" preserveAspectRatio="xMidYMid meet">${axis2}${lbl2}${pts2}</svg></div>
    <div class="chart-card"><div class="ttl">类目内容供给</div><div class="desc">低=蓝海机会</div><svg viewBox="0 0 ${w3} ${h3}" preserveAspectRatio="xMidYMid meet">${bars}</svg></div>
  `;
}

// ========== Presets ==========
const PRESETS = [
  { key: '24h_rising', label: '🔥 24h 上升爆款' },
  { key: '7d_strong',  label: '💥 7 天强爆款' },
  { key: 'high_er',    label: '🎯 高 ER 优质' },
  { key: 'channel_hot',label: '📈 频道爆款' },
  { key: 'phenom',     label: '🚀 现象级' },
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

// ========== Sidebar ==========
function renderSidebar() {
  const root = document.getElementById('sidebar-content');
  root.innerHTML = '';
  if (state.tab !== 'home' && state.tab !== 'monitor') {
    root.innerHTML = '<div style="color:var(--text-faint);font-size:12px;padding:20px;text-align:center">筛选仅在「首页」「竞品监测」 Tab 生效</div>';
    const thLate = document.createElement('h4');
    thLate.textContent = '主题';
    root.appendChild(thLate);
    const twLate = document.createElement('div');
    twLate.innerHTML = renderThemeSwitch();
    root.appendChild(twLate);
    bindThemeSwitch(twLate);
    return;
  }
  const filtered = applyFilters(DATA.videos);
  const cnt = filtered.length;
  const cls = cnt === 0 ? 'alert' : cnt < 10 ? 'warn' : '';

  // result count
  const rc = document.createElement('div');
  rc.className = 'result-count ' + cls;
  rc.textContent = '显示 ' + cnt + ' 条';
  root.appendChild(rc);

  // presets
  const ph = document.createElement('h4');
  ph.textContent = '快捷预设';
  root.appendChild(ph);
  const pp = document.createElement('div');
  pp.className = 'presets';
  pp.innerHTML = PRESETS.map(p => `<button class="preset-btn${state.preset === p.key ? ' active' : ''}" data-preset="${p.key}">${p.label}</button>`).join('');
  pp.querySelectorAll('[data-preset]').forEach(b => b.onclick = () => applyPreset(b.dataset.preset));
  root.appendChild(pp);

  // filters
  const fh = document.createElement('h4');
  fh.textContent = '筛选器';
  root.appendChild(fh);
  const fs = document.createElement('div');
  fs.className = 'filters-stack';
  const setKey = (key, val) => { state.filters[key] = val; state.preset = ''; saveState(); render(); };

  fs.appendChild(makeDropdown({
    label: '时间', multi: false,
    options: [{value:'all',label:'全部'},{value:'1',label:'近 24h'},{value:'7',label:'近 7 天'},{value:'30',label:'近 30 天'},{value:'90',label:'近 90 天'}],
    getSelected: () => state.filters.time,
    onApply: v => setKey('time', v),
  }).el);

  fs.appendChild(makeChannelTreeDropdown({
    getGroups: () => state.filters.groups,
    getChannels: () => state.filters.channels,
    onApply: (g, c) => { state.filters.groups = g; state.filters.channels = c; state.preset = ''; saveState(); render(); },
  }).el);

  fs.appendChild(makeDropdown({ label: '内容类型', multi: true, options: CFG.content_tags_order, getSelected: () => state.filters.contents, onApply: v => setKey('contents', v) }).el);
  fs.appendChild(makeDropdown({ label: '时长', multi: true, options: CFG.length_order, getSelected: () => state.filters.lengths, onApply: v => setKey('lengths', v) }).el);
  fs.appendChild(makeDropdown({ label: '爆款', multi: true, options: CFG.hot_level_order, getSelected: () => state.filters.hots, onApply: v => setKey('hots', v) }).el);
  fs.appendChild(makeDropdown({ label: '视频类型', multi: true, options: CFG.video_type_order, getSelected: () => state.filters.vtypes, onApply: v => setKey('vtypes', v) }).el);
  fs.appendChild(makeDropdown({ label: '品牌提及', multi: true, options: brandMentionOptions(), getSelected: () => state.filters.brands, onApply: v => setKey('brands', v) }).el);
  fs.appendChild(makeDropdown({
    label: '排序', multi: false,
    options: [
      {value:'er',label:'ER ↓'}, {value:'views',label:'播放量 ↓'},
      {value:'comment_rate',label:'评论率 ↓'}, {value:'view_to_sub',label:'播放/订阅比 ↓'},
      {value:'recent',label:'发布时间 ↓'},
    ],
    getSelected: () => state.sort,
    onApply: v => { state.sort = v; saveState(); render(); },
  }).el);
  root.appendChild(fs);

  // actions
  const ah = document.createElement('h4');
  ah.textContent = '操作';
  root.appendChild(ah);
  const aa = document.createElement('div');
  aa.className = 'actions-stack';

  const viewBtn = document.createElement('button');
  viewBtn.className = 'btn';
  const viewLabels = { grid: '视图: 网格', list: '视图: 列表', inspire: '视图: 灵感' };
  viewBtn.textContent = viewLabels[state.view_mode || 'grid'];
  viewBtn.onclick = () => {
    const order = ['grid', 'list', 'inspire'];
    state.view_mode = order[(order.indexOf(state.view_mode || 'grid') + 1) % order.length];
    saveState(); render();
  };
  aa.appendChild(viewBtn);

  const bulkBtn = document.createElement('button');
  bulkBtn.className = 'btn' + (bulkMode ? ' btn-primary' : '');
  bulkBtn.textContent = bulkMode ? '退出批量模式' : '批量模式';
  bulkBtn.onclick = () => { bulkMode = !bulkMode; if (!bulkMode) bulkSelected.clear(); render(); };
  aa.appendChild(bulkBtn);

  const csv = document.createElement('button');
  csv.className = 'btn';
  csv.innerHTML = ICONS.download + ' 导出 CSV';
  csv.onclick = () => exportCSV();
  aa.appendChild(csv);

  const clr = document.createElement('button');
  clr.className = 'btn btn-danger';
  clr.textContent = '清空筛选';
  clr.onclick = () => { state.filters = defaultFilters(); state.preset = ''; saveState(); render(); };
  aa.appendChild(clr);

  root.appendChild(aa);

  // selected chips
  if (activeFilterCount() > 0) {
    const sh = document.createElement('h4');
    sh.textContent = '已选筛选';
    root.appendChild(sh);
    const ss = document.createElement('div');
    ss.className = 'selected-stack';

    const items = [];
    const f = state.filters;
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
    items.forEach((it, i) => {
      const delta = it.impact - cnt;
      const sign = delta > 0 ? '+' : '';
      const c = document.createElement('span');
      c.className = 'chip';
      c.innerHTML = `${escHTML(it.label)} <span class="chip-impact">(${sign}${delta})</span><span class="chip-x">✕</span>`;
      c.querySelector('.chip-x').onclick = () => {
        if (it.key === 'time') state.filters.time = 'all';
        else state.filters[it.key] = state.filters[it.key].filter(v => v !== it.value);
        state.preset = ''; saveState(); render();
      };
      ss.appendChild(c);
    });
    root.appendChild(ss);

    if (cnt < 10 && items.length >= 2) {
      const relax = document.createElement('button');
      relax.className = 'chip-relax';
      relax.style.marginTop = '6px';
      relax.textContent = '🔓 智能放宽';
      relax.onclick = () => {
        let best = null;
        items.forEach(it => { if (!best || it.impact > best.impact) best = it; });
        if (best) {
          if (best.key === 'time') state.filters.time = 'all';
          else state.filters[best.key] = state.filters[best.key].filter(v => v !== best.value);
          state.preset = ''; saveState(); render();
          showToast('放宽筛选: 已移除 ' + best.label);
        }
      };
      root.appendChild(relax);
    }
  }

  // 主题切换（永远在 sidebar 底部）
  const th = document.createElement('h4');
  th.textContent = '主题';
  root.appendChild(th);
  const tw = document.createElement('div');
  tw.innerHTML = renderThemeSwitch();
  root.appendChild(tw);
  bindThemeSwitch(tw);
}

// ========== Mobile drawer ==========
function openMobileDrawer() {
  pendingMobileState = JSON.parse(JSON.stringify({ filters: state.filters, sort: state.sort }));
  // 移动抽屉里的 dropdown
  const root = document.getElementById('mb-drawer-content');
  root.innerHTML = '';
  const setKey = (key, val) => { pendingMobileState.filters[key] = val; };

  const items = [
    { label: '时间', el: makeDropdown({ label: '时间', multi: false,
      options: [{value:'all',label:'全部'},{value:'1',label:'近 24h'},{value:'7',label:'近 7 天'},{value:'30',label:'近 30 天'},{value:'90',label:'近 90 天'}],
      getSelected: () => pendingMobileState.filters.time, onApply: v => setKey('time', v) }).el },
    { label: '频道分组', el: makeChannelTreeDropdown({
      getGroups: () => pendingMobileState.filters.groups,
      getChannels: () => pendingMobileState.filters.channels,
      onApply: (g, c) => { pendingMobileState.filters.groups = g; pendingMobileState.filters.channels = c; } }).el },
    { label: '内容类型', el: makeDropdown({ label: '内容类型', multi: true, options: CFG.content_tags_order, getSelected: () => pendingMobileState.filters.contents, onApply: v => setKey('contents', v) }).el },
    { label: '时长', el: makeDropdown({ label: '时长', multi: true, options: CFG.length_order, getSelected: () => pendingMobileState.filters.lengths, onApply: v => setKey('lengths', v) }).el },
    { label: '爆款', el: makeDropdown({ label: '爆款', multi: true, options: CFG.hot_level_order, getSelected: () => pendingMobileState.filters.hots, onApply: v => setKey('hots', v) }).el },
    { label: '视频类型', el: makeDropdown({ label: '视频类型', multi: true, options: CFG.video_type_order, getSelected: () => pendingMobileState.filters.vtypes, onApply: v => setKey('vtypes', v) }).el },
    { label: '品牌提及', el: makeDropdown({ label: '品牌提及', multi: true, options: brandMentionOptions(), getSelected: () => pendingMobileState.filters.brands, onApply: v => setKey('brands', v) }).el },
    { label: '排序', el: makeDropdown({ label: '排序', multi: false,
      options: [{value:'er',label:'ER ↓'},{value:'views',label:'播放量 ↓'},{value:'comment_rate',label:'评论率 ↓'},{value:'view_to_sub',label:'播放/订阅比 ↓'},{value:'recent',label:'发布时间 ↓'}],
      getSelected: () => pendingMobileState.sort, onApply: v => { pendingMobileState.sort = v; } }).el },
  ];
  items.forEach(it => {
    const lbl = document.createElement('div');
    lbl.className = 'label';
    lbl.textContent = it.label;
    root.appendChild(lbl);
    root.appendChild(it.el);
  });

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

function renderCompareBoard(filtered) {
  const channels = state.filters.channels;
  if (channels.length < 2) return '';
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
  const rankBy = (key) => {
    const sorted = [...stats].sort((a,b) => b[key] - a[key]);
    return name => sorted.findIndex(s => s.name === name);
  };
  const rkSubs = rankBy('subs'), rkCount = rankBy('count'), rkTot = rankBy('tot'), rkER = rankBy('aer'), rkHot = rankBy('hot');
  const medal = ri => ri === 0 ? '🥇' : ri === 1 ? '🥈' : ri === 2 ? '🥉' : '';
  const N = stats.length;
  const scored = stats.map(s => ({
    ...s,
    score: ((N - rkSubs(s.name)) + (N - rkCount(s.name)) + (N - rkER(s.name)) + (N - rkHot(s.name))) / (4 * N) * 100,
  }));

  return '<div class="compare-board">' + scored.map(s => `
    <div class="ccard ${s.isSelf ? 'is-self' : ''}" data-channel="${escHTML(s.name)}">
      <button class="close" data-close="${escHTML(s.name)}">✕</button>
      <div class="head"><span class="name">${escHTML(s.name)}</span>${s.isSelf ? '<span class="self-tag">⭐ 自家</span>' : ''}</div>
      <div class="subs">${fmt(s.subs)} 订阅</div>
      <div class="grid2">
        <div class="cell">视频<b>${s.count}<span class="rank">${medal(rkCount(s.name))}</span></b></div>
        <div class="cell">总播放<b>${fmt(s.tot)}<span class="rank">${medal(rkTot(s.name))}</span></b></div>
        <div class="cell">平均 ER<b>${s.aer.toFixed(2)}%<span class="rank">${medal(rkER(s.name))}</span></b></div>
        <div class="cell">爆款<b>${s.hot}<span class="rank">${medal(rkHot(s.name))}</span></b></div>
      </div>
      <div class="cell" style="margin-bottom:8px">高 ER<b>${s.high_er}</b></div>
      <div class="score-row"><span>综合实力</span><span class="score-bar"><span style="width:${s.score.toFixed(0)}%"></span></span><span class="score-num">${s.score.toFixed(0)}</span></div>
    </div>
  `).join('') + '</div>';
}

function renderBulkBar(visibleVideos) {
  if (!bulkMode) return '';
  return `<div class="bulk-bar">
    <span class="selected-count">已选 ${bulkSelected.size} 个</span>
    <button class="btn" id="bulk-all">全选当前页</button>
    <button class="btn" id="bulk-none">全部取消</button>
    <button class="btn btn-primary" id="bulk-fav">⭐ 加入拆解清单</button>
    <button class="btn" id="bulk-link">复制链接</button>
    <button class="btn" id="bulk-csv">${ICONS.download} 导出 CSV</button>
    <button class="btn" id="bulk-exit" style="margin-left:auto">退出</button>
  </div>`;
}
function bindBulkBar(visible) {
  const all = document.getElementById('bulk-all'); if (all) all.onclick = () => { visible.forEach(v => bulkSelected.add(v.video_id)); render(); };
  const none = document.getElementById('bulk-none'); if (none) none.onclick = () => { bulkSelected.clear(); render(); };
  const fav = document.getElementById('bulk-fav'); if (fav) fav.onclick = () => {
    const cur = new Set(getFavs()); bulkSelected.forEach(id => cur.add(id));
    setFavs(Array.from(cur)); showToast('已加入拆解清单 ' + bulkSelected.size + ' 个'); bulkSelected.clear(); bulkMode = false; render();
  };
  const link = document.getElementById('bulk-link'); if (link) link.onclick = () => {
    const sep = String.fromCharCode(10);
    const urls = Array.from(bulkSelected).map(id => DATA.videos.find(v => v.video_id === id)?.video_url).filter(Boolean).join(sep);
    navigator.clipboard?.writeText(urls).then(() => showToast('已复制 ' + bulkSelected.size + ' 个链接'));
  };
  const csv = document.getElementById('bulk-csv'); if (csv) csv.onclick = () => exportCSV(visible.filter(v => bulkSelected.has(v.video_id)), 'bulk');
  const exit = document.getElementById('bulk-exit'); if (exit) exit.onclick = () => { bulkMode = false; bulkSelected.clear(); render(); };
}

// ========== Home View ==========
function renderHomeView() {
  const root = document.getElementById('view-home');
  const filtered = applyFilters(DATA.videos);
  const sorted = applySort(filtered);

  let html = '';
  html += renderBulkBar(sorted);
  html += renderCompareBoard(filtered);

  if (sorted.length === 0) {
    const f = state.filters;
    let banner = '';
    if (activeFilterCount() > 0) {
      const sugs = [];
      ['groups','channels','contents','lengths','hots','vtypes','brands'].forEach(k => {
        f[k].forEach(val => { const cnt = countWithout(k, val); if (cnt > 0) sugs.push({ k, val, cnt }); });
      });
      if (f.time !== 'all') { const cnt = countWithout('time', null); if (cnt > 0) sugs.push({ k: 'time', val: f.time, cnt }); }
      sugs.sort((a,b) => b.cnt - a.cnt);
      banner = `<div class="empty-banner"><div class="ttl">⚠️ 无符合条件视频，建议:</div>`
        + sugs.slice(0, 3).map((s, i) => `<button data-sug="${i}">移除「${escHTML(s.k === 'time' ? '时间' : s.val)}」→ 显示 ${s.cnt} 条</button>`).join('')
        + `</div>`;
    }
    html += banner;
    html += '<div class="empty">没有符合筛选条件的视频</div>';
  } else {
    const cls = 'grid' + (state.view_mode === 'list' ? ' list-view' : state.view_mode === 'inspire' ? ' inspire-view' : '');
    html += `<div class="${cls}">` + sorted.map(renderVideoCard).join('') + '</div>';
  }
  root.innerHTML = html;
  bindCardActions(root);
  bindBulkBar(sorted);

  root.querySelectorAll('[data-sug]').forEach(b => b.onclick = () => {
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
  root.querySelectorAll('[data-close]').forEach(b => b.onclick = (e) => {
    e.stopPropagation();
    const name = b.dataset.close;
    state.filters.channels = state.filters.channels.filter(c => c !== name);
    saveState(); render();
  });
  root.querySelectorAll('.ccard[data-channel]').forEach(c => c.onclick = (e) => {
    if (e.target.dataset.close) return;
    state.filters.channels = [c.dataset.channel];
    state.filters.groups = [];
    saveState(); render();
  });
}

// ========== Favorites / Brand / History / Monitor （保留 V4 实现）==========
const TEARDOWN_DIMS = [
  { key: 'hook', label: 'Hook' }, { key: 'pain', label: 'Pain Point' },
  { key: 'arc', label: 'Story Arc' }, { key: 'visual', label: 'Visual Style' },
  { key: 'audio', label: 'Audio' }, { key: 'cta', label: 'CTA' },
];
function autoFillTeardown(v) {
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
        <div style="border-top:1px dashed var(--border);padding-top:8px;display:flex;flex-direction:column;gap:6px">
          ${TEARDOWN_DIMS.map(d => `
            <div style="font-size:11px"><span style="color:var(--text-faint);min-width:90px;display:inline-block">${d.label}:</span>
              <input type="text" data-vid="${v.video_id}" data-key="${d.key}" value="${escHTML(td[d.key]||'')}" placeholder="手填..."
                style="background:var(--card-hover);border:1px solid var(--border);color:var(--text);padding:3px 6px;border-radius:4px;width:calc(100% - 96px);font-size:11px"></div>
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
            <button class="btn btn-danger" style="margin-left:auto;padding:4px 10px;font-size:11px;min-height:28px;width:auto" data-rm-fav="${v.video_id}">移除</button>
          </div>
          <textarea data-vid="${v.video_id}" data-key="notes" placeholder="备注..." style="background:var(--card-hover);border:1px solid var(--border);color:var(--text);padding:6px;border-radius:4px;font-size:11px;resize:vertical;min-height:40px">${escHTML(td.notes||'')}</textarea>
        </div>
      </div>
    </div>`;
}
function renderFavoritesView() {
  const root = document.getElementById('view-favorites');
  const favIds = getFavs();
  const favSet = new Set(favIds);
  const favs = DATA.videos.filter(v => favSet.has(v.video_id));
  const sorted = applySort(favs);
  let html = '';
  if (!state.workflow_banner_dismissed) {
    html += `<div class="workflow-banner"><span class="close-x" id="wf-close">✕</span><h4>💡 拆解工作流</h4>
      <ol><li>首页用筛选预设找候选爆款</li><li>批量模式选 5-10 条 → 加入此清单</li><li>填 10 维（前 6 手填 + 后 4 自动）</li><li>[复制链接] → 粘贴 Claude.ai 拆 Hook+Body+CTA+公式</li><li>公式入 Obsidian 30_内容弹药库</li></ol></div>`;
  }
  html += `<div style="display:flex;gap:8px;margin-bottom:16px;align-items:center;flex-wrap:wrap">
    <span style="font-size:14px;font-weight:600">${favs.length} 条收藏</span>
    ${favs.length > 0 ? `
      <button class="btn" id="fav-md" style="width:auto">${ICONS.download} 复制 Markdown</button>
      <button class="btn" id="fav-csv" style="width:auto">${ICONS.download} 导出 CSV</button>
      <button class="btn btn-danger" id="fav-clear" style="width:auto">清空</button>` : ''}
  </div>`;
  if (favs.length === 0) html += '<div class="empty">还没有收藏视频</div>';
  else {
    const td = getTeardownData();
    html += '<div class="grid">' + sorted.map(v => renderTeardownCard(v, td[v.video_id] || {})).join('') + '</div>';
  }
  root.innerHTML = html;
  const wfClose = document.getElementById('wf-close');
  if (wfClose) wfClose.onclick = () => { state.workflow_banner_dismissed = true; saveState(); render(); };
  const md = document.getElementById('fav-md'); if (md) md.onclick = () => exportMarkdown(sorted);
  const csv = document.getElementById('fav-csv'); if (csv) csv.onclick = () => exportTeardownCSV(sorted);
  const clr = document.getElementById('fav-clear'); if (clr) clr.onclick = () => { if (confirm('清空？')) { setFavs([]); render(); } };
  bindCardActions(root);
}

function renderBrandCompareView() {
  const root = document.getElementById('view-brand');
  const brands = CFG.brand_compare_default;
  const stats = brands.map(name => {
    const vs = DATA.videos.filter(v => v.channel_name === name);
    return { name, count: vs.length, tot: vs.reduce((s,v) => s+(v.view_count||0), 0),
      aer: vs.length ? vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length : 0,
      hot: vs.filter(v => v.hot_level).length, max: vs.length ? Math.max(...vs.map(v => v.view_count||0)) : 0,
      weekCount: vs.filter(v => withinTime(v.published_at, '7')).length,
      subs: vs[0]?.channel_subscriber_count || 0, isSelf: name === CFG.self_brand };
  });
  const maxTot = Math.max(...stats.map(s => s.tot), 1);
  let html = '<div class="panel"><h3>核心竞品横向对比</h3><table><thead><tr><th>频道</th><th>订阅</th><th>视频</th><th>本周新</th><th>平均 ER</th><th>最高单条</th><th>爆款</th><th>总播放</th></tr></thead><tbody>';
  stats.forEach(s => {
    html += `<tr><td class="name">${s.isSelf ? '⭐ ' : ''}${escHTML(s.name)}</td><td>${fmt(s.subs)}</td><td>${s.count}</td><td>${s.weekCount}</td><td>${s.aer.toFixed(2)}%</td><td>${fmt(s.max)}</td><td>${s.hot}</td><td>${fmt(s.tot)}<span class="bar"><span style="width:${(s.tot/maxTot*100).toFixed(0)}%"></span></span></td></tr>`;
  });
  html += '</tbody></table></div>';
  const aChannels = (CFG.channel_tree.A_brand||[]).map(c => c.display_name);
  const aStats = aChannels.map(name => {
    const vs = DATA.videos.filter(v => v.channel_name === name);
    return { name, count: vs.length, subs: vs[0]?.channel_subscriber_count || 0,
      aer: vs.length ? vs.reduce((s,v) => s+(v.engagement_rate||0), 0) / vs.length : 0,
      hot: vs.filter(v => v.hot_level).length,
      tot: vs.reduce((s,v) => s+(v.view_count||0), 0), isSelf: name === CFG.self_brand };
  });
  aStats.sort((a,b) => b.subs - a.subs);
  html += '<div class="panel"><h3>A 组竞品全量</h3><table><thead><tr><th>频道</th><th>订阅</th><th>视频</th><th>平均 ER</th><th>爆款</th><th>总播放</th></tr></thead><tbody>';
  aStats.forEach(s => html += `<tr><td class="name">${s.isSelf ? '⭐ ' : ''}${escHTML(s.name)}</td><td>${fmt(s.subs)}</td><td>${s.count}</td><td>${s.aer.toFixed(2)}%</td><td>${s.hot}</td><td>${fmt(s.tot)}</td></tr>`);
  html += '</tbody></table></div>';
  root.innerHTML = html;
}

function renderHistoryView() {
  const root = document.getElementById('view-history');
  const cnt = HISTORY?.count || 0;
  const need = 7;
  let html = '<div class="panel"><h3>历史趋势</h3>';
  if (cnt < need) {
    html += `<div class="history-empty"><div class="big">需要积累 ${need} 天数据</div><div>已积累 ${cnt} 天 / 还需 ${need - cnt} 天</div><div class="progress"><span style="width:${(cnt/need*100).toFixed(0)}%"></span></div><div style="margin-top:14px;font-size:12px;color:var(--text-faint)">每天 9:00 自动跑完会保存当日快照</div></div>`;
  } else html += '<div>趋势图开发中</div>';
  html += '</div>';
  root.innerHTML = html;
}

function renderHiddenView() {
  const root = document.getElementById('view-hidden');
  const ids = getHidden();
  const vids = DATA.videos.filter(v => ids.includes(v.video_id));
  let html = '<div class="panel"><h3>已隐藏视频 (' + vids.length + ' 条)</h3>';
  if (vids.length === 0) {
    html += '<div class="empty">没有已隐藏视频</div>';
  } else {
    html += `<div style="margin-bottom:14px;display:flex;gap:8px"><button class="btn" id="hd-clear" style="width:auto;color:var(--down);border-color:var(--down)">全部恢复</button></div>`;
    html += '<div class="grid">' + vids.map(v => {
      return `<div class="video-card" data-vid="${v.video_id}">
        <a href="${v.video_url}" target="_blank" class="thumb-wrap">
          <img src="${v.thumbnail_url}" alt="" loading="lazy">
          <div class="duration">${v.duration||''}</div>
        </a>
        <div class="card-body">
          <div class="card-row1"><span class="channel-name">${escHTML(v.channel_name)}</span></div>
          <a class="card-title" href="${v.video_url}" target="_blank">${escHTML(v.title)}</a>
          <button class="btn btn-primary" data-unhide="${v.video_id}" style="margin-top:8px">恢复显示</button>
        </div>
      </div>`;
    }).join('') + '</div>';
  }
  html += '</div>';
  root.innerHTML = html;
  const clr = document.getElementById('hd-clear');
  if (clr) clr.onclick = () => {
    if (confirm('全部恢复（' + vids.length + ' 条）？')) { setHidden([]); render(); showToast('已全部恢复'); }
  };
  root.querySelectorAll('[data-unhide]').forEach(b => b.onclick = () => {
    const vid = b.dataset.unhide;
    setHidden(getHidden().filter(x => x !== vid));
    render();
    showToast('已恢复');
  });
}

function renderMonitorView() {
  const root = document.getElementById('view-monitor');
  const aChannels = (CFG.channel_tree.A_brand||[]).map(c => c.display_name);
  const aWeek = DATA.videos.filter(v => v.channel_group === 'A_brand' && withinTime(v.published_at, '7'));
  aWeek.sort((a,b) => new Date(b.published_at) - new Date(a.published_at));
  const stats = aChannels.map(name => ({
    name, weekVids: aWeek.filter(v => v.channel_name === name),
    weekHot: aWeek.filter(v => v.channel_name === name && (v.view_count >= 1e5 || v.hot_level)).length,
  }));
  let html = '<div class="panel"><h3>本周 A 组竞品动态</h3>';
  html += `<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));gap:10px;margin-bottom:18px">`
    + stats.map(s => `<div class="ccard ${s.name === CFG.self_brand ? 'is-self' : ''}"><div class="head"><span class="name">${escHTML(s.name)}</span></div><div style="font-size:13px;font-family:var(--font-mono);color:var(--text)">本周 <b>${s.weekVids.length}</b> 条 · 爆款 <b>${s.weekHot}</b></div></div>`).join('') + '</div>';
  html += `<h3 style="margin-top:24px">本周新视频 (${aWeek.length} 条)</h3>`;
  if (aWeek.length === 0) html += '<div class="empty">本周 A 组无新视频</div>';
  else html += '<div class="grid">' + aWeek.map(renderVideoCard).join('') + '</div>';
  html += '</div>';
  root.innerHTML = html;
  bindCardActions(root);
}

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
    const v = DATA.videos.find(x => x.video_id === vid);
    const title = v ? v.title : vid;
    const cur = getHidden();
    if (!cur.includes(vid)) { cur.push(vid); setHidden(cur); }
    render();
    showToast(`已隐藏《${title.slice(0, 24)}》`, {
      actionLabel: '撤销',
      duration: 5000,
      onAction: () => {
        setHidden(getHidden().filter(x => x !== vid));
        render();
        showToast('已恢复显示');
      }
    });
  });
  root.querySelectorAll('.bulk-cb').forEach(c => c.onclick = (e) => {
    e.stopPropagation(); e.preventDefault();
    const vid = c.closest('.video-card').dataset.vid;
    if (bulkSelected.has(vid)) bulkSelected.delete(vid); else bulkSelected.add(vid);
    render();
  });
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

function exportCSV(videos=null, suffix='filtered') {
  const data = videos || applyFilters(DATA.videos);
  const cols = ['video_id','channel_name','channel_group','title','view_count','like_count','comment_count','engagement_rate','comment_rate','duration','published_at','hot_level','video_length_type','video_type','content_tags','brand_mentions','view_to_sub_ratio','relevance_score','video_url'];
  const NL = String.fromCharCode(10);
  const rows = data.map(v => cols.map(c => {
    let val = v[c];
    if (Array.isArray(val)) val = val.join('; ');
    val = val == null ? '' : String(val);
    if (/[",]/.test(val) || val.indexOf(NL) >= 0) val = '"' + val.replace(/"/g, '""') + '"';
    return val;
  }).join(','));
  const csv = String.fromCharCode(0xFEFF) + cols.join(',') + NL + rows.join(NL);
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
  const NL = String.fromCharCode(10);
  const rows = videos.map(v => {
    const t = td[v.video_id] || {};
    return cols.map(c => {
      let val;
      if (c === 'er') val = (v.engagement_rate||0).toFixed(2);
      else if (c === 'views') val = v.view_count;
      else if (c === 'url') val = v.video_url;
      else if (c === 'progress') val = t.progress || '待拆';
      else if (c === 'notes') val = t.notes || '';
      else if (dims.includes(c)) val = t[c] || '';
      else val = v[c];
      val = val == null ? '' : String(val);
      if (/[",]/.test(val) || val.indexOf(NL) >= 0) val = '"' + val.replace(/"/g, '""') + '"';
      return val;
    }).join(',');
  });
  const csv = String.fromCharCode(0xFEFF) + cols.join(',') + NL + rows.join(NL);
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `youtube-tracker-teardown-${new Date().toISOString().slice(0,10)}.csv`;
  a.click(); URL.revokeObjectURL(url);
  showToast('已导出 ' + videos.length + ' 条');
}
function exportMarkdown(videos) {
  const NL = String.fromCharCode(10);
  const md = videos.map(v => `- [${v.title}](${v.video_url}) · ${v.channel_name} · ▶ ${fmt(v.view_count)} · ER ${(v.engagement_rate||0).toFixed(2)}%`).join(NL);
  navigator.clipboard?.writeText(md).then(() => showToast('Markdown 已复制'));
}

// ========== Master Render ==========
function render() {
  document.getElementById('view-home').style.display = state.tab === 'home' ? 'block' : 'none';
  document.getElementById('view-favorites').style.display = state.tab === 'favorites' ? 'block' : 'none';
  document.getElementById('view-brand').style.display = state.tab === 'brand' ? 'block' : 'none';
  document.getElementById('view-history').style.display = state.tab === 'history' ? 'block' : 'none';
  document.getElementById('view-monitor').style.display = state.tab === 'monitor' ? 'block' : 'none';
  document.getElementById('view-hidden').style.display = state.tab === 'hidden' ? 'block' : 'none';

  const filtered = applyFilters(DATA.videos);
  renderTabs();
  renderOverviewBar(filtered);
  renderKPI(filtered);
  renderInsight(filtered);
  renderStatRow(filtered);
  renderCharts(filtered);
  renderSidebar();

  if (state.tab === 'home') renderHomeView();
  else if (state.tab === 'favorites') renderFavoritesView();
  else if (state.tab === 'brand') renderBrandCompareView();
  else if (state.tab === 'history') renderHistoryView();
  else if (state.tab === 'monitor') renderMonitorView();
  else if (state.tab === 'hidden') renderHiddenView();

  const fcnt = activeFilterCount();
  const fcb = document.getElementById('mb-filter-count');
  if (fcnt > 0) { fcb.textContent = fcnt; fcb.style.display = 'inline-block'; } else { fcb.style.display = 'none'; }
  const favCnt = getFavs().length;
  const favb = document.getElementById('mb-fav-count');
  if (favCnt > 0) { favb.textContent = favCnt; favb.style.display = 'inline-block'; } else { favb.style.display = 'none'; }
  const sortMap = { er: 'ER↓', views: '播放↓', comment_rate: '评论率↓', view_to_sub: '播放/订阅↓', recent: '最新' };
  document.getElementById('mb-sort-label').textContent = sortMap[state.sort] || '';
  setTimeout(updateHeaderHeight, 0);
}

function updateMeta() {
  document.getElementById('gen-at').textContent = DATA.generated_at;
  document.getElementById('gen-ago').textContent = fmtAgo(DATA.generated_at);
  document.getElementById('ch-count').textContent = DATA.channel_count;
  document.getElementById('vid-count').textContent = DATA.video_count;
}

// ========== Theme Manager (深色 / 浅色 / 跟随系统) ==========
const themeManager = {
  init() {
    this.apply(this.getStored());
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (this.getStored() === 'auto') this.applyAuto();
    });
  },
  getStored() { return localStorage.getItem('theme-pref') || 'dark'; },
  apply(theme) {
    if (theme === 'auto') this.applyAuto();
    else document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme-pref', theme);
  },
  applyAuto() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  },
};
themeManager.init();

function renderThemeSwitch() {
  const cur = themeManager.getStored();
  const opts = [
    { v: 'dark', label: '🌙 深色' },
    { v: 'light', label: '☀️ 浅色' },
    { v: 'auto', label: '🖥 系统' },
  ];
  return `<div class="theme-switch">${opts.map(o => `<button class="${cur === o.v ? 'active' : ''}" data-theme="${o.v}">${o.label}</button>`).join('')}</div>`;
}
function bindThemeSwitch(root) {
  root.querySelectorAll('[data-theme]').forEach(b => b.onclick = () => {
    themeManager.apply(b.dataset.theme); render();
  });
}

async function init() {
  document.getElementById('mb-filter').onclick = openMobileDrawer;
  document.getElementById('mb-fav').onclick = () => { state.tab = 'favorites'; saveState(); render(); };
  document.getElementById('mb-sort').onclick = () => {
    const opts = ['er','views','comment_rate','view_to_sub','recent'];
    const cur = opts.indexOf(state.sort);
    state.sort = opts[(cur + 1) % opts.length];
    saveState(); render();
  };
  document.getElementById('mb-overlay').onclick = closeMobileDrawer;
  document.getElementById('mb-drawer-close').onclick = closeMobileDrawer;
  document.getElementById('mb-drawer-reset').onclick = () => {
    pendingMobileState.filters = defaultFilters(); pendingMobileState.sort = 'er';
    openMobileDrawer();  // 重新渲染
  };
  document.getElementById('mb-drawer-apply').onclick = applyMobileDrawer;

  window.addEventListener('resize', updateHeaderHeight);

  try {
    DATA = await fetchData();
    HISTORY = await fetchHistoryIndex();
    updateMeta();
    render();
  } catch (e) {
    document.getElementById('view-home').innerHTML =
      '<div class="empty">❌ 加载数据失败: ' + escHTML(e.message) +
      '<br>请用 <code>http://localhost:8765/dashboard.html</code> 或云端打开</div>';
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
