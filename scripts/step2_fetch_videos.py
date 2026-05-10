"""
Step 2 (V2): 抓视频 + 计算 8 个数据维度
1) engagement_rate (互动率)
2) comment_rate (评论率)
3) video_length_type (Shorts/Short/Medium/Long)
4) content_tags (多标)
5) hot_level (爆款等级)
6) view_to_sub_ratio (订阅播放比)
7) video_type (评测/开箱/对比...)
8) brand_mentions (品牌关键词)
"""
import json
import re
import time
from pathlib import Path
import yt_api

ROOT = Path(__file__).resolve().parent.parent
LIST_FILE = ROOT / "data" / "channels_list.json"
ALL_FILE = ROOT / "data" / "channels_data.json"
PER_DIR = ROOT / "data" / "channels"

VIDEOS_PER_CHANNEL = 10

# ============ 维度计算配置 ============

CONTENT_TAG_RULES = [
    ("iPad配件相关", [r"ipad keyboard", r"ipad case", r"magic keyboard", r"ipad cover", r"ipad accessor"]),
    ("创作",        [r"\bprocreate\b", r"\bdraw(ing)?\b", r"\bart(ist)?\b", r"\bdesign(er)?\b", r"\bcreator\b", r"illustrat", r"painting"]),
    ("学生",        [r"\bstudy\b", r"\bstudent\b", r"\bschool\b", r"\bhomework\b", r"\bcollege\b", r"\bexam\b", r"\bnote-?taking\b"]),
    ("商务",        [r"\bwfh\b", r"\boffice\b", r"\bproductivity\b", r"\bwork\b", r"\bbusiness\b", r"\bremote\b", r"\bworkflow\b"]),
]
# "其他Apple" 特殊：含 iPhone/Mac/Watch/AirPods 但不含 iPad
APPLE_OTHER_TERMS = [r"\biphone\b", r"\bmacbook\b", r"\bimac\b", r"\bapple watch\b", r"\bairpods\b", r"\bvision pro\b"]
HAS_IPAD = re.compile(r"\bipad\b", re.IGNORECASE)

VIDEO_TYPE_RULES = [
    ("评测",       [r"\breview\b", r"\bhands.?on\b", r"\bin-?depth look\b"]),
    ("开箱",       [r"\bunbox", r"\bunboxing\b", r"\bfirst look\b"]),
    ("对比",       [r"\bvs\.?\b", r"\bversus\b", r"\bcompar"]),
    ("装机/Setup", [r"\bsetup\b", r"\bdesk setup\b", r"\bworkstation\b", r"\bbattlestation\b"]),
    ("教程",       [r"\btutorial\b", r"\bstep[- ]by[- ]step\b", r"\bwalkthrough\b"]),
    ("教学",       [r"how to\b", r"\bguide\b", r"\btips\b", r"\btricks\b", r"\bhacks\b", r"\blearn\b"]),
    ("vlog",       [r"\bvlog\b", r"\ba day in\b", r"\bweek in my life\b", r"\bmy day\b"]),
    ("宣传片/广告",[r"\bcommercial\b", r"\bad\b\s*[—-]", r"\bspot\b", r"\bpromo\b", r"\btrailer\b"]),
    ("产品发布",   [r"\bannounce", r"\bintroducing\b", r"\blaunch\b", r"\bnew product\b", r"\breveal\b", r"\brelease\b"]),
    ("推荐/Best",  [r"\bbest\b", r"\btop \d", r"\brecommend", r"\bmust[- ]have\b"]),
]

# 频道 → 自家品牌（brand_mentions 排除）
CHANNEL_SELF_BRAND = {
    "Logitech":     "Logitech相关",
    "ESR Gear":     "ESR相关",
    "ZAGG":         "ZAGG相关",
    "Fintie":       "Fintie相关",
    "Inateck":      "Inateck相关",
    "Arteck":       "Arteck相关",
    "Doqo":         "Doqo相关",
    "Apple":        "Apple键盘相关",
    "Typecase":     "Typecase相关",
    "Anker":        "Anker相关",
    "Belkin":       "Belkin相关",
    "Satechi":      "Satechi相关",
    "Twelve South": "Twelve South相关",
    "Native Union": "Native Union相关",
    "Procreate":    "Procreate相关",
}

# 品牌关键词监测（HOU 用严格规则避免误伤）
BRAND_RULES = [
    ("Brydge相关",     [r"\bbrydge\b"]),
    ("HOU相关",        [r"\bhou keyboard\b", r"\bhou ipad\b", r"\bhou case\b"]),
    ("Logitech相关",   [r"logitech combo", r"logitech folio", r"logitech crayon", r"logitech pen"]),
    ("Apple键盘相关",  [r"magic keyboard"]),
    ("ESR相关",        [r"\besr\b"]),
    ("ZAGG相关",       [r"\bzagg\b"]),
    ("Fintie相关",     [r"\bfintie\b"]),
    ("Inateck相关",    [r"\binateck\b"]),
    ("Arteck相关",     [r"\barteck\b"]),
    ("Doqo相关",       [r"\bdoqo\b"]),
    ("Typecase相关",   [r"\btypecase\b"]),
    ("Anker相关",      [r"\banker\b"]),
    ("Belkin相关",     [r"\bbelkin\b"]),
    ("Satechi相关",    [r"\bsatechi\b"]),
    ("Twelve South相关",[r"twelve south"]),
    ("Native Union相关",[r"native union"]),
    ("Procreate相关",  [r"\bprocreate\b"]),
]


def parse_iso_duration_secs(s):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    if not m:
        return 0
    h, mi, se = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + se


def fmt_duration(secs):
    if secs <= 0:
        return ""
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def best_thumb(thumbs):
    for k in ("maxres", "standard", "high", "medium", "default"):
        if k in thumbs:
            return thumbs[k]["url"]
    return ""


def slugify(name):
    s = re.sub(r"[^\w\s-]", "", name).strip()
    s = re.sub(r"\s+", "_", s)
    return s or "channel"


# ============ 8 个维度 ============

def calc_engagement_rate(views, likes, comments):
    if not views or views <= 0:
        return 0.0
    return round((((likes or 0) + (comments or 0)) / views) * 100, 2)


def calc_comment_rate(views, comments):
    if not views or views <= 0:
        return 0.0
    return round((comments or 0) / views * 100, 3)


def calc_video_length_type(secs):
    if secs < 60:    return "Shorts"
    if secs < 300:   return "Short"
    if secs < 900:   return "Medium"
    return "Long"


def calc_content_tags(text):
    text_l = text.lower()
    tags = []
    for tag, patterns in CONTENT_TAG_RULES:
        if any(re.search(p, text_l) for p in patterns):
            tags.append(tag)
    has_ipad = bool(HAS_IPAD.search(text_l))
    if not has_ipad and any(re.search(p, text_l) for p in APPLE_OTHER_TERMS):
        tags.append("其他Apple")
    if not tags:
        tags.append("其他")
    return tags


def calc_video_type(text):
    text_l = text.lower()
    for label, patterns in VIDEO_TYPE_RULES:
        if any(re.search(p, text_l) for p in patterns):
            return label
    return "其他"


def calc_brand_mentions(text, channel_display_name=None):
    """品牌提及（排除自家频道发的）"""
    text_l = text.lower()
    self_brand = CHANNEL_SELF_BRAND.get(channel_display_name)
    out = []
    for label, patterns in BRAND_RULES:
        if label == self_brand:
            continue  # 排除自家品牌
        if any(re.search(p, text_l) for p in patterns):
            out.append(label)
    return out


# 强相关关键词（用于 relevance_score）
IPAD_ACCESSORY_PAT = re.compile(r"ipad keyboard|ipad case|magic keyboard|ipad cover|ipad accessor|smart folio|apple pencil", re.IGNORECASE)
IPAD_PAT = re.compile(r"\bipad\b", re.IGNORECASE)
OTHER_APPLE_PAT = re.compile(r"\b(iphone|macbook|imac|apple watch|airpods|vision pro)\b", re.IGNORECASE)


def calc_relevance_score(title, desc, content_tags, channel_group):
    text = (title or "") + " " + (desc or "")
    if IPAD_ACCESSORY_PAT.search(text):
        return 100
    if IPAD_PAT.search(text):
        if any(t in content_tags for t in ("创作", "学生", "商务")):
            return 80
        return 60
    if OTHER_APPLE_PAT.search(text) or channel_group == "A_brand":
        return 30
    return 20


def calc_hot_level(views, er, published_iso, now_ms):
    """爆款等级（互斥，按最高级取）"""
    pub_ms = _iso_to_ms(published_iso)
    age_h = (now_ms - pub_ms) / 3_600_000
    if views >= 5_000_000:
        return "🚀 现象级"
    if views >= 1_000_000 and age_h <= 30 * 24:
        return "⭐ 百万爆款"
    if views >= 500_000 and age_h <= 7 * 24 and er >= 5:
        return "💥 强爆款"
    if views >= 100_000 and age_h <= 24 and er >= 5:
        return "🔥 上升爆款"
    return ""


def calc_view_to_sub_ratio(views, subs):
    if not subs or subs <= 0:
        return 0.0, "频道冷启"
    ratio = round(views / subs * 100, 2)
    if ratio > 10:   tier = "频道爆款"
    elif ratio > 5:  tier = "频道高分"
    elif ratio > 1:  tier = "频道一般"
    else:            tier = "频道冷启"
    return ratio, tier


def _iso_to_ms(iso):
    iso = iso.replace("Z", "+00:00")
    from datetime import datetime
    return int(datetime.fromisoformat(iso).timestamp() * 1000)


# ============ 主流程 ============

def main():
    PER_DIR.mkdir(parents=True, exist_ok=True)
    list_data = json.loads(LIST_FILE.read_text())
    channels = list_data["channels"]
    print(f"V2 抓取 {len(channels)} 个频道的最新 {VIDEOS_PER_CHANNEL} 个视频...")

    video_to_channel = {}
    failures = []
    for c in channels:
        try:
            vids = yt_api.playlist_items(c["uploads_playlist_id"], VIDEOS_PER_CHANNEL)
            for vid in vids:
                video_to_channel[vid] = c
        except Exception as e:
            print(f"  ❌ {c['display_name']:<40} 失败: {e}")
            failures.append({"channel": c["display_name"], "reason": str(e)})
        time.sleep(0.05)
    print(f"  ✅ 共 {len(video_to_channel)} 个视频 ID")

    # 批量拿详情（含 description）
    items = yt_api.videos_batch(list(video_to_channel.keys()))
    print(f"  ✅ 拿到 {len(items)} 条视频详情")

    by_channel = {c["channel_id"]: [] for c in channels}
    all_videos = []
    now_ms = int(time.time() * 1000)

    for it in items:
        vid = it["id"]
        ch = video_to_channel.get(vid)
        if not ch:
            continue
        snip = it["snippet"]
        stats = it.get("statistics", {})
        details = it.get("contentDetails", {})

        title = snip["title"]
        desc = (snip.get("description", "") or "")[:500]  # 截断省体积
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0)) if "likeCount" in stats else None
        comments = int(stats.get("commentCount", 0)) if "commentCount" in stats else None
        duration_secs = parse_iso_duration_secs(details.get("duration", ""))
        published = snip["publishedAt"]

        text_for_match = f"{title}\n{desc}"
        er = calc_engagement_rate(views, likes, comments)
        cr = calc_comment_rate(views, comments)
        vlt = calc_video_length_type(duration_secs)
        ctags = calc_content_tags(text_for_match)
        vtype = calc_video_type(title)
        brands = calc_brand_mentions(text_for_match, ch["display_name"])
        hot = calc_hot_level(views, er, published, now_ms)
        ratio, ratio_tier = calc_view_to_sub_ratio(views, ch["subscriber_count"])
        relevance = calc_relevance_score(title, desc, ctags, ch["group"])

        record = {
            "video_id": vid,
            "title": title,
            "description": desc,
            "thumbnail_url": best_thumb(snip.get("thumbnails", {})),
            "view_count": views,
            "like_count": likes,
            "comment_count": comments,
            "duration": fmt_duration(duration_secs),
            "duration_secs": duration_secs,
            "published_at": published,
            "channel_id": ch["channel_id"],
            "channel_name": ch["display_name"],
            "channel_youtube_title": ch["youtube_title"],
            "channel_group": ch["group"],
            "channel_subscriber_count": ch["subscriber_count"],
            "video_url": f"https://www.youtube.com/watch?v={vid}",
            # ===== 8 个维度 =====
            "engagement_rate": er,
            "comment_rate": cr,
            "video_length_type": vlt,
            "content_tags": ctags,
            "video_type": vtype,
            "brand_mentions": brands,
            "hot_level": hot,
            "view_to_sub_ratio": ratio,
            "view_to_sub_tier": ratio_tier,
            "relevance_score": relevance,
        }
        by_channel[ch["channel_id"]].append(record)
        all_videos.append(record)

    # 每频道单独文件
    for c in channels:
        vids = sorted(by_channel[c["channel_id"]], key=lambda x: x["published_at"], reverse=True)
        slug = slugify(c["display_name"])
        (PER_DIR / f"{slug}.json").write_text(json.dumps({
            "channel": {
                "display_name": c["display_name"],
                "channel_id": c["channel_id"],
                "youtube_title": c["youtube_title"],
                "group": c["group"],
                "subscriber_count": c["subscriber_count"],
            },
            "videos": vids,
        }, ensure_ascii=False, indent=2))

    # 总表（默认按 ER 排序，但前端会重新排）
    all_videos.sort(key=lambda x: x["engagement_rate"], reverse=True)
    ALL_FILE.write_text(json.dumps({
        "version": "v2",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "channel_count": len(channels),
        "video_count": len(all_videos),
        "channels": channels,
        "videos": all_videos,
        "failures": failures,
    }, ensure_ascii=False, indent=2))

    print(f"\n✅ 完成。视频 {len(all_videos)} 条")

    # 维度分布速览
    from collections import Counter
    print(f"\n━━ 维度分布预览 ━━")
    print(f"  hot_level:        {Counter(v['hot_level'] or '普通' for v in all_videos).most_common()}")
    print(f"  video_length:     {Counter(v['video_length_type'] for v in all_videos).most_common()}")
    print(f"  video_type:       {Counter(v['video_type'] for v in all_videos).most_common()}")
    ctag_flat = Counter()
    for v in all_videos:
        for t in v["content_tags"]:
            ctag_flat[t] += 1
    print(f"  content_tags:     {ctag_flat.most_common()}")
    brand_flat = Counter()
    for v in all_videos:
        for b in v["brand_mentions"]:
            brand_flat[b] += 1
    print(f"  brand_mentions:   {brand_flat.most_common(15)}")

    avg_er = sum(v["engagement_rate"] for v in all_videos) / max(1, len(all_videos))
    high_er = sum(1 for v in all_videos if v["engagement_rate"] >= 5)
    print(f"\n  平均 ER:         {avg_er:.2f}%  |  ER>=5% 的视频: {high_er}")
    print(f"  数据生成: {time.strftime('%Y-%m-%dT%H:%M:%S')}")


if __name__ == "__main__":
    main()
