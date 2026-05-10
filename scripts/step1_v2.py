"""
Step 1 (V2): 66 个频道 → channels_list.json
策略: 26 个老频道从 V1 备份复用 channel_id，40 个新频道走 search/handle
"""
import json
import time
from pathlib import Path
import yt_api

ROOT = Path(__file__).resolve().parent.parent
V1_BAK = ROOT / "data" / "channels_list.v1.bak.json"
OUT = ROOT / "data" / "channels_list.json"

# V2 完整清单 (search_query_or_@handle, display_name, group_code)
# group_code: A_brand / B_ipad_vertical / C_top_tech / D_real_use / E_lifestyle / F_3c_brand
# 老频道用 V1 的 display_name 即可被复用（reuse_map 里查）
V2_CHANNELS = [
    # ========== A 直接竞品 + 自家追踪 ==========
    ("Brydge keyboard",                     "Brydge",                          "A_brand"),
    ("HOU iPad keyboard",                   "HOU",                             "A_brand"),
    ("Logitech",                            "Logitech",                        "A_brand"),
    ("ESR Gear",                            "ESR Gear",                        "A_brand"),
    ("ZAGG Inc",                            "ZAGG",                            "A_brand"),
    ("Fintie",                              "Fintie",                          "A_brand"),
    ("Inateck",                             "Inateck",                         "A_brand"),
    ("Arteck",                              "Arteck",                          "A_brand"),
    ("Doqo iPad keyboard",                  "Doqo",                            "A_brand"),
    ("Apple",                               "Apple",                           "A_brand"),
    ("@typecase_official",                  "Typecase",                        "A_brand"),

    # ========== B iPad 垂直内容 ==========
    ("iPad Pros",                           "iPad Pros",                       "B_ipad_vertical"),
    ("9to5Toys",                            "9to5Toys",                        "B_ipad_vertical"),
    ("AppleSauce",                          "AppleSauce",                      "B_ipad_vertical"),
    ("iPaddict",                            "iPaddict",                        "B_ipad_vertical"),
    ("The Sweet Setup",                     "The Sweet Setup",                 "B_ipad_vertical"),
    ("Tom's Guide",                         "Tom's Guide",                     "B_ipad_vertical"),
    ("Gizmodo",                             "Gizmodo",                         "B_ipad_vertical"),
    ("Engadget",                            "Engadget",                        "B_ipad_vertical"),
    ("The Verge",                           "The Verge",                       "B_ipad_vertical"),
    ("9to5Mac",                             "9to5Mac",                         "B_ipad_vertical"),
    ("Christopher Lawley",                  "Christopher Lawley",              "B_ipad_vertical"),
    ("Tim Chaten",                          "Tim Chaten",                      "B_ipad_vertical"),

    # ========== C 头部数码博主 ==========
    ("MKBHD",                               "MKBHD",                           "C_top_tech"),
    ("iJustine",                            "iJustine",                        "C_top_tech"),
    ("Linus Tech Tips",                     "Linus Tech Tips",                 "C_top_tech"),
    ("Dave Lee tech",                       "Dave Lee",                        "C_top_tech"),
    ("Snazzy Labs",                         "Snazzy Labs",                     "C_top_tech"),

    # ========== D 真实使用场景 - 学生 (10) ==========
    ("Studyquill",                          "Studyquill",                      "D_real_use"),
    ("UnJaded Jade",                        "UnJaded Jade",                    "D_real_use"),
    ("Ruby Granger",                        "Ruby Granger",                    "D_real_use"),
    ("Ali Abdaal",                          "Ali Abdaal",                      "D_real_use"),
    ("Thomas Frank",                        "Thomas Frank",                    "D_real_use"),
    ("Tia Taylor study",                    "Tia Taylor",                      "D_real_use"),
    ("Studytee",                            "Studytee",                        "D_real_use"),
    ("The Cottage Fairy",                   "The Cottage Fairy",               "D_real_use"),
    ("Aileen Xu Lavendaire",                "Aileen Xu",                       "D_real_use"),
    ("Tom Solid Paperless",                 "Tom Solid",                       "D_real_use"),

    # ========== D 真实使用场景 - 艺术创作 (10) ==========
    ("Brad Colbow",                         "Brad Colbow",                     "D_real_use"),
    ("Procreate",                           "Procreate",                       "D_real_use"),
    ("Karl Heinz Kremer",                   "Karl Heinz Kremer",               "D_real_use"),
    ("Sara Dietschy",                       "Sara Dietschy",                   "D_real_use"),
    ("Peter McKinnon",                      "Peter McKinnon",                  "D_real_use"),
    ("Christine Le artist",                 "Christine Le",                    "D_real_use"),
    ("Joan Kim",                            "Joan Kim",                        "D_real_use"),
    ("Casey Neistat",                       "Casey Neistat",                   "D_real_use"),
    ("Mariana's Study Corner",              "Mariana Vieira",                  "D_real_use"),
    ("Bardot Brush",                        "Lisa Bardot (Bardot Brush)",      "D_real_use"),  # +1 由我推荐

    # ========== D 真实使用场景 - 商务 (5) ==========
    ("MacStories",                          "Federico Viticci (MacStories)",   "D_real_use"),
    ("Matt D'Avella",                       "Matt D'Avella",                   "D_real_use"),
    ("Pat Flynn Smart Passive Income",      "Pat Flynn",                       "D_real_use"),
    ("Karl Conrad iPad",                    "Karl Conrad",                     "D_real_use"),
    ("Erik Conover",                        "Erik Conover",                    "D_real_use"),

    # ========== E Lifestyle ==========
    ("Pick Up Limes",                       "Pick Up Limes",                   "E_lifestyle"),
    ("Lavendaire",                          "Lavendaire",                      "E_lifestyle"),
    ("Caroline Winkler",                    "Caroline Winkler",                "E_lifestyle"),
    ("With Jamie",                          "With Jamie",                      "E_lifestyle"),
    ("Coffee with Sam",                     "Coffee with Sam",                 "E_lifestyle"),
    ("WorkSpaceLab",                        "WorkSpaceLab",                    "E_lifestyle"),
    ("Marie Forleo",                        "Marie Forleo",                    "E_lifestyle"),
    ("Madeleine Olivia",                    "Madeleine Olivia",                "E_lifestyle"),

    # ========== F 3C 品牌 ==========
    ("Anker",                               "Anker",                           "F_3c_brand"),
    ("Belkin",                              "Belkin",                          "F_3c_brand"),
    ("Satechi",                             "Satechi",                         "F_3c_brand"),
    ("Twelve South",                        "Twelve South",                    "F_3c_brand"),
    ("Native Union",                        "Native Union",                    "F_3c_brand"),
]


def get_by_handle(handle):
    handle = handle.lstrip("@")
    data = yt_api._get("channels", {
        "forHandle": f"@{handle}",
        "part": "snippet,statistics,contentDetails",
    })
    items = data.get("items", [])
    if not items:
        return None
    item = items[0]
    return {
        "channel_id": item["id"],
        "youtube_title": item["snippet"]["title"],
        "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
        "uploads_playlist_id": item["contentDetails"]["relatedPlaylists"]["uploads"],
    }


def main():
    # 1) 从 V1 备份建复用映射: V1 display_name -> {channel_id, ...}
    v1 = json.loads(V1_BAK.read_text())
    # 旧→新名字映射（V1 用的名字 → V2 用的名字）
    rename = {
        "Marques Brownlee (MKBHD)": "MKBHD",
        "Mariana's Study Corner": "Mariana Vieira",
        "MacStories (Federico Viticci)": "Federico Viticci (MacStories)",
    }
    reuse = {}
    for c in v1["channels"]:
        key = rename.get(c["display_name"], c["display_name"])
        reuse[key] = {
            "channel_id": c["channel_id"],
            "youtube_title": c["youtube_title"],
            "subscriber_count": c["subscriber_count"],
            "uploads_playlist_id": c["uploads_playlist_id"],
        }

    # 2) 解析 V2 清单
    results = []
    issues = []
    reused_count = 0
    api_count = 0

    for query, display_name, group in V2_CHANNELS:
        if display_name in reuse:
            r = reuse[display_name]
            results.append({
                "display_name": display_name,
                "search_query": query,
                "group": group,
                **r,
                "_source": "reused_from_v1",
            })
            reused_count += 1
            continue

        # 新频道
        try:
            if query.startswith("@"):
                info = get_by_handle(query)
                api_count += 1
                if info is None:
                    print(f"  ❌ handle {query} 找不到 ({display_name})")
                    issues.append({"display_name": display_name, "query": query, "reason": "handle not found"})
                    continue
                results.append({
                    "display_name": display_name,
                    "search_query": query,
                    "group": group,
                    **info,
                    "_source": "handle",
                })
                print(f"  🆕 {display_name:<35} ← @handle {query[1:]:<25} {info['subscriber_count']:>10,} subs ({info['youtube_title']})")
            else:
                cid, title = yt_api.search_channel(query)
                api_count += 1
                if cid is None:
                    print(f"  ❌ {display_name:<35} 搜不到 (关键词: {query})")
                    issues.append({"display_name": display_name, "query": query, "reason": "no result"})
                    continue
                stats = yt_api.channels_batch([cid])
                api_count += 1
                s = stats.get(cid, {})
                subs = s.get("subscriber_count", 0)
                uploads = s.get("uploads_playlist_id", "")
                # 标记可疑
                suspect = ""
                if "Topic" in title:
                    suspect = " ⚠️Topic"
                if subs < 1000:
                    suspect += " ⚠️低订阅"
                results.append({
                    "display_name": display_name,
                    "search_query": query,
                    "group": group,
                    "channel_id": cid,
                    "youtube_title": title,
                    "subscriber_count": subs,
                    "uploads_playlist_id": uploads,
                    "_source": "search",
                })
                print(f"  🆕 {display_name:<35} ← search {query:<28} {subs:>10,} subs ({title}){suspect}")
                if suspect:
                    issues.append({"display_name": display_name, "query": query, "title": title, "subs": subs, "reason": suspect.strip()})
        except Exception as e:
            print(f"  ⚠️  {display_name:<35} API 错误: {e}")
            issues.append({"display_name": display_name, "query": query, "reason": str(e)})
        time.sleep(0.05)

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"V2 共 {len(V2_CHANNELS)} 个频道 → 拿到 {len(results)}")
    print(f"  • 复用 V1: {reused_count} 个 (省 {reused_count * 100} search 配额)")
    print(f"  • 新调 API: {api_count} 次 (~{api_count * 50} 配额)")
    if issues:
        print(f"\n⚠️  {len(issues)} 个有问题:")
        for x in issues:
            print(f"     - {x['display_name']}: {x['reason']}{' (' + x.get('title','') + ')' if x.get('title') else ''}")

    # 3) 检查重复 channel_id
    seen = {}
    dupes = []
    for r in results:
        if r["channel_id"] in seen:
            dupes.append((r["display_name"], seen[r["channel_id"]], r["channel_id"]))
        else:
            seen[r["channel_id"]] = r["display_name"]
    if dupes:
        print(f"\n⚠️  发现 ID 撞车:")
        for d in dupes:
            print(f"     {d[0]} ↔ {d[1]} (id={d[2]})")

    # 4) 写 channels_list.json
    OUT.write_text(json.dumps({
        "version": "v2",
        "channels": results,
        "issues": issues,
        "duplicates": dupes,
    }, ensure_ascii=False, indent=2))
    print(f"\n✅ 写入 {OUT}")


if __name__ == "__main__":
    main()
