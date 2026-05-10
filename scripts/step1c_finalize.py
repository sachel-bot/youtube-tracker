"""
Step 1c: 按用户指令最终化频道清单
- 5 个用 handle 重搜：Belkin / The Sweet Setup / iPad Pros / Tia Taylor / With Jamie
- 6 个直接删：Coffee with Sam / iPaddict / Aileen Xu / Karl Heinz Kremer / Brydge / HOU
"""
import json
from pathlib import Path
import yt_api

ROOT = Path(__file__).resolve().parent.parent
LIST = ROOT / "data" / "channels_list.json"

# 用 handle 重搜 (display_name -> handle 候选清单)
RE_SEARCH_HANDLES = {
    "Belkin":          ["@belkininc", "@belkin", "@BelkinInternational"],
    "The Sweet Setup": ["@thesweetsetup", "@TheSweetSetup"],
    "iPad Pros":       ["@iPadPros", "@ipadpros", "@iPadProsPodcast"],
    "Tia Taylor":      ["@tiataylor", "@TiaTaylor", "@TiaTaylorr"],
    "With Jamie":      ["@withjamie", "@WithJamie", "@jamiewithjamie"],
}

# 直接删除
DELETE = {
    "Coffee with Sam",
    "iPaddict",
    "Aileen Xu",
    "Karl Heinz Kremer",
    "Brydge",
    "HOU",
}


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
    data = json.loads(LIST.read_text())
    channels = data["channels"]
    print(f"开始: {len(channels)} 个频道\n")

    # 1) 用 handle 重搜
    print("━━ 阶段 1: handle 重搜 ━━")
    repaired = []
    handle_failed = []
    for c in channels:
        if c["display_name"] not in RE_SEARCH_HANDLES:
            continue
        handles = RE_SEARCH_HANDLES[c["display_name"]]
        found = None
        used_handle = None
        for h in handles:
            try:
                info = get_by_handle(h)
                if info and info["subscriber_count"] >= 1000:  # 低订阅当 fallback 失败
                    found = info
                    used_handle = h
                    break
                elif info:
                    print(f"     {h} → {info['youtube_title']} ({info['subscriber_count']:,} subs) 太低，再试")
            except Exception as e:
                print(f"     {h} 失败: {e}")
        if found:
            c["channel_id"] = found["channel_id"]
            c["youtube_title"] = found["youtube_title"]
            c["subscriber_count"] = found["subscriber_count"]
            c["uploads_playlist_id"] = found["uploads_playlist_id"]
            c["search_query"] = used_handle
            c["_source"] = "handle_repaired"
            print(f"  ✅ {c['display_name']:<20} → {used_handle:<25} ({found['youtube_title']}, {found['subscriber_count']:,} subs)")
            repaired.append(c["display_name"])
        else:
            print(f"  ❌ {c['display_name']:<20} 全部 handle 都拿不到，删")
            handle_failed.append(c["display_name"])

    # 2) 应用删除
    delete_set = DELETE | set(handle_failed)
    before = len(channels)
    channels = [c for c in channels if c["display_name"] not in delete_set]
    deleted_count = before - len(channels)

    # 3) 检查是否还有撞 ID
    seen = {}
    dupes = []
    for r in channels:
        if r["channel_id"] in seen:
            dupes.append((r["display_name"], seen[r["channel_id"]]))
        else:
            seen[r["channel_id"]] = r["display_name"]

    # 4) 写回
    data["channels"] = channels
    data["v2_finalize"] = {
        "repaired_via_handle": repaired,
        "deleted": sorted(delete_set),
        "duplicates_after": dupes,
    }
    LIST.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    print(f"\n━━ 最终统计 ━━")
    print(f"频道总数: {before} → {len(channels)} (删 {deleted_count})")
    print(f"  • handle 修复成功: {len(repaired)}")
    print(f"  • 删除: {sorted(delete_set)}")
    if dupes:
        print(f"  ⚠️  仍有撞 ID: {dupes}")
    else:
        print(f"  ✅ 无撞 ID")

    # 按分组统计
    from collections import Counter
    grp = Counter(c["group"] for c in channels)
    print(f"\n按分组:")
    for g in ["A_brand", "B_ipad_vertical", "C_top_tech", "D_real_use", "E_lifestyle", "F_3c_brand"]:
        print(f"  {g}: {grp.get(g, 0)}")


if __name__ == "__main__":
    main()
