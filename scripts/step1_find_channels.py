"""
Step 1: 搜 50 个频道名 → 拿 Channel ID + 订阅数 + uploads playlist
输出: data/channels_list.json
"""
import json
import time
from pathlib import Path
import yt_api

ROOT = Path(__file__).resolve().parent.parent
OUT_FILE = ROOT / "data" / "channels_list.json"

# (搜索关键词, 显示名, 分组标签)
# 分组: top_tech / ipad_vertical / creator_lifestyle / tech_lifestyle / brand / tech_media / apple_vertical
CHANNELS = [
    ("MKBHD",                       "Marques Brownlee (MKBHD)",      "top_tech"),
    ("iJustine",                    "iJustine",                       "top_tech"),
    ("Linus Tech Tips",             "Linus Tech Tips",                "top_tech"),
    ("Sara Dietschy",               "Sara Dietschy",                  "top_tech"),
    ("Peter McKinnon",              "Peter McKinnon",                 "top_tech"),
    ("Casey Neistat",               "Casey Neistat",                  "top_tech"),
    ("Tested",                      "Tested",                         "top_tech"),

    ("Christopher Lawley",          "Christopher Lawley",             "ipad_vertical"),
    ("MacStories",                  "MacStories (Federico Viticci)",  "ipad_vertical"),
    ("Ali Abdaal",                  "Ali Abdaal",                     "ipad_vertical"),
    ("Matt D'Avella",               "Matt D'Avella",                  "ipad_vertical"),
    ("Thomas Frank",                "Thomas Frank",                   "ipad_vertical"),

    ("Mariana's Study Corner",      "Mariana's Study Corner",         "creator_lifestyle"),
    ("The Studyholic",              "The Studyholic",                 "creator_lifestyle"),
    ("UnJaded Jade",                "UnJaded Jade",                   "creator_lifestyle"),
    ("Ruby Granger",                "Ruby Granger",                   "creator_lifestyle"),
    ("Justine Leconte officiel",    "Justine Leconte",                "creator_lifestyle"),
    ("Jenn Im",                     "Jenn Im",                        "creator_lifestyle"),
    ("Pick Up Limes",               "Pick Up Limes",                  "creator_lifestyle"),
    ("Lavendaire",                  "Lavendaire",                     "creator_lifestyle"),

    ("Tina Huang",                  "Tina Huang",                     "tech_lifestyle"),
    ("Erik Conover",                "Erik Conover",                   "tech_lifestyle"),
    ("Cleo Abram",                  "Cleo Abram",                     "tech_lifestyle"),
    ("Mrwhosetheboss",              "Mrwhosetheboss",                 "tech_lifestyle"),
    ("Andrew Kan",                  "Andrew Kan",                     "tech_lifestyle"),

    ("Apple",                       "Apple",                          "brand"),
    ("Logitech",                    "Logitech",                       "brand"),
    ("ESR Gear",                    "ESR Gear",                       "brand"),
    ("ZAGG",                        "ZAGG",                           "brand"),
    ("OtterBox",                    "OtterBox",                       "brand"),
    ("Speck Products",              "Speck Products",                 "brand"),
    ("Urban Armor Gear",            "UAG (Urban Armor Gear)",         "brand"),
    ("Targus",                      "Targus",                         "brand"),

    ("The Verge",                   "The Verge",                      "tech_media"),
    ("Engadget",                    "Engadget",                       "tech_media"),
    ("CNET",                        "CNET",                           "tech_media"),
    ("WIRED",                       "Wired",                          "tech_media"),
    ("TechRadar",                   "TechRadar",                      "tech_media"),
    ("Tom's Guide",                 "Tom's Guide",                    "tech_media"),
    ("9to5Mac",                     "9to5Mac",                        "tech_media"),
    ("AppleInsider",                "AppleInsider",                   "tech_media"),
    ("MacRumors",                   "MacRumors",                      "tech_media"),
    ("iMore",                       "iMore",                          "tech_media"),

    ("Snazzy Labs",                 "Snazzy Labs",                    "apple_vertical"),
    ("Max Tech",                    "Max Tech",                       "apple_vertical"),
    ("AppleTrack",                  "AppleTrack",                     "apple_vertical"),
    ("Luke Miani",                  "Luke Miani",                     "apple_vertical"),
    ("Sam Kohl",                    "Sam Kohl",                       "apple_vertical"),
    ("Front Page Tech",             "Jon Prosser (Front Page Tech)",  "apple_vertical"),
    ("Rene Ritchie",                "Rene Ritchie",                   "apple_vertical"),
]


def main():
    results = []
    not_found = []

    print(f"开始搜 {len(CHANNELS)} 个频道...\n")
    for query, display_name, group in CHANNELS:
        try:
            cid, real_title = yt_api.search_channel(query)
            if cid is None:
                print(f"  ❌ 没搜到: {display_name}  (关键词: {query})")
                not_found.append({"display_name": display_name, "query": query, "reason": "no result"})
                continue
            print(f"  ✅ {display_name:<40} → {cid}  ({real_title})")
            results.append({
                "display_name": display_name,
                "search_query": query,
                "group": group,
                "channel_id": cid,
                "youtube_title": real_title,
            })
        except Exception as e:
            print(f"  ⚠️  API 错误 [{display_name}]: {e}")
            not_found.append({"display_name": display_name, "query": query, "reason": str(e)})
        time.sleep(0.05)

    print(f"\n搜到 {len(results)}/{len(CHANNELS)}，开始拿订阅数 + uploads playlist...")
    cid_list = [r["channel_id"] for r in results]
    stats = yt_api.channels_batch(cid_list)
    for r in results:
        s = stats.get(r["channel_id"], {})
        r["subscriber_count"] = s.get("subscriber_count", 0)
        r["uploads_playlist_id"] = s.get("uploads_playlist_id")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"channels": results, "not_found": not_found}, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成。写入 {OUT_FILE}")
    print(f"   成功: {len(results)}  失败: {len(not_found)}")
    if not_found:
        print(f"   失败列表: {[x['display_name'] for x in not_found]}")


if __name__ == "__main__":
    main()
