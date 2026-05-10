"""V6 一次性重算字段（不重抓）"""
import json
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from step2_fetch_videos import (
    calc_video_type, calc_brand_mentions, calc_relevance_score,
    calc_content_tags, calc_hot_level, calc_engagement_rate,
)

DATA_FILE = ROOT / "data" / "channels_data.json"
PER_DIR = ROOT / "data" / "channels"


def reprocess(d, now_ms):
    for v in d["videos"]:
        title = v.get("title", "")
        desc = v.get("description", "")
        text = f"{title}\n{desc}"
        v["content_tags"] = calc_content_tags(text)
        v["video_type"] = calc_video_type(title)
        v["brand_mentions"] = calc_brand_mentions(text, v.get("channel_name"))
        v["relevance_score"] = calc_relevance_score(title, desc, v["content_tags"], v.get("channel_group"))
        # hot_level 用动态阈值（subs）
        er = calc_engagement_rate(v.get("view_count", 0), v.get("like_count"), v.get("comment_count"))
        v["engagement_rate"] = er
        v["hot_level"] = calc_hot_level(
            v.get("view_count", 0), er, v.get("published_at"), now_ms,
            v.get("channel_subscriber_count", 0)
        )


def main():
    now_ms = int(time.time() * 1000)
    d = json.loads(DATA_FILE.read_text())
    reprocess(d, now_ms)
    DATA_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2))
    print(f"✅ {DATA_FILE.name}: {len(d['videos'])} 条")

    for f in PER_DIR.iterdir():
        if f.suffix != ".json":
            continue
        cd = json.loads(f.read_text())
        for v in cd["videos"]:
            title = v.get("title", "")
            desc = v.get("description", "")
            text = f"{title}\n{desc}"
            v["content_tags"] = calc_content_tags(text)
            v["video_type"] = calc_video_type(title)
            v["brand_mentions"] = calc_brand_mentions(text, v.get("channel_name"))
            v["relevance_score"] = calc_relevance_score(title, desc, v["content_tags"], v.get("channel_group"))
            er = calc_engagement_rate(v.get("view_count", 0), v.get("like_count"), v.get("comment_count"))
            v["engagement_rate"] = er
            v["hot_level"] = calc_hot_level(
                v.get("view_count", 0), er, v.get("published_at"), now_ms,
                v.get("channel_subscriber_count", 0)
            )
        f.write_text(json.dumps(cd, ensure_ascii=False, indent=2))
    print(f"✅ {PER_DIR.name}/ 56 个文件")

    from collections import Counter
    hl = Counter(v["hot_level"] or "普通" for v in d["videos"])
    bm = Counter()
    for v in d["videos"]:
        for b in v["brand_mentions"]:
            bm[b] += 1
    ct = Counter()
    for v in d["videos"]:
        for t in v["content_tags"]:
            ct[t] += 1
    print(f"\n━━ V6 维度分布 ━━")
    print(f"  hot_level:    {hl.most_common()}")
    print(f"  brand_mentions（排除自家，20 品牌）: {bm.most_common(20)}")
    print(f"  content_tags（多关键词+同义词）: {ct.most_common()}")


if __name__ == "__main__":
    main()
