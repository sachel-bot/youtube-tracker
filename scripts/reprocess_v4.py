"""
V4 一次性：用新 step2 的逻辑重算现有 channels_data.json
- video_type 10 种
- brand_mentions 排除自家
- relevance_score 新字段
不重抓 YouTube · 0 配额
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# 复用 step2 的纯函数
from step2_fetch_videos import (
    calc_video_type,
    calc_brand_mentions,
    calc_relevance_score,
    calc_content_tags,  # 需要保证 content_tags 也是新逻辑（已对）
)

DATA_FILE = ROOT / "data" / "channels_data.json"
PER_DIR = ROOT / "data" / "channels"
HISTORY_FILE = ROOT / "data" / "history" / "2026-05-11.json"


def reprocess(d):
    changed_count = 0
    for v in d["videos"]:
        title = v.get("title", "")
        desc = v.get("description", "")
        text_for_match = f"{title}\n{desc}"

        old_vt = v.get("video_type")
        old_bm = v.get("brand_mentions") or []

        # 重算
        v["content_tags"] = calc_content_tags(text_for_match)
        v["video_type"] = calc_video_type(title)
        v["brand_mentions"] = calc_brand_mentions(text_for_match, v.get("channel_name"))
        v["relevance_score"] = calc_relevance_score(title, desc, v["content_tags"], v.get("channel_group"))

        if v["video_type"] != old_vt or v["brand_mentions"] != old_bm:
            changed_count += 1
    return changed_count


def main():
    # 1) 主数据
    d = json.loads(DATA_FILE.read_text())
    cnt = reprocess(d)
    DATA_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2))
    print(f"✅ {DATA_FILE.name}: 重算 {len(d['videos'])} 条，{cnt} 条字段变化")

    # 2) 每频道
    for f in PER_DIR.iterdir():
        if not f.suffix == ".json":
            continue
        cd = json.loads(f.read_text())
        for v in cd["videos"]:
            title = v.get("title", "")
            desc = v.get("description", "")
            text_for_match = f"{title}\n{desc}"
            v["content_tags"] = calc_content_tags(text_for_match)
            v["video_type"] = calc_video_type(title)
            v["brand_mentions"] = calc_brand_mentions(text_for_match, v.get("channel_name"))
            v["relevance_score"] = calc_relevance_score(title, desc, v["content_tags"], v.get("channel_group"))
        f.write_text(json.dumps(cd, ensure_ascii=False, indent=2))
    print(f"✅ {PER_DIR.name}/ 56 个文件已重算")

    # 3) 历史快照（修今天的快照让前端进度对齐）
    if HISTORY_FILE.exists():
        h = json.loads(HISTORY_FILE.read_text())
        reprocess(h)
        HISTORY_FILE.write_text(json.dumps(h, ensure_ascii=False, indent=2))
        print(f"✅ history/{HISTORY_FILE.name} 已重算")

    # 4) 维度分布
    from collections import Counter
    vt = Counter(v["video_type"] for v in d["videos"])
    rs = Counter(("100" if v["relevance_score"] == 100 else "80" if v["relevance_score"] == 80 else "60" if v["relevance_score"] == 60 else "30" if v["relevance_score"] == 30 else "20") for v in d["videos"])
    bm_flat = Counter()
    for v in d["videos"]:
        for b in v["brand_mentions"]:
            bm_flat[b] += 1
    print(f"\n━━ 新维度分布 ━━")
    print(f"  video_type:      {vt.most_common()}")
    print(f"  relevance_score: {rs.most_common()}")
    print(f"  brand_mentions（排除自家后）: {bm_flat.most_common(15)}")


if __name__ == "__main__":
    main()
