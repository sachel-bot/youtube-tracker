"""
Step 1b: 修复 Sam Kohl 撞 ID 和 ZAGG 搜到 Topic 频道的问题
"""
import json
from pathlib import Path
import requests
import yt_api

ROOT = Path(__file__).resolve().parent.parent
LIST_FILE = ROOT / "data" / "channels_list.json"


def get_by_handle(handle):
    """用 channels.list?forHandle 拿频道（带重试）"""
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
    data = json.loads(LIST_FILE.read_text())
    channels = data["channels"]

    # 1) Sam Kohl: 试 handle @samkohl
    print("修复 Sam Kohl...")
    found = get_by_handle("samkohl")
    if found is None:
        print(f"  @samkohl 不存在；试 @SamKohl ...")
        found = get_by_handle("SamKohl")
    if found is None:
        print(f"  ❌ 没找到 Sam Kohl 个人频道，从列表中移除")
        channels = [c for c in channels if c["display_name"] != "Sam Kohl"]
    else:
        print(f"  ✅ Sam Kohl → {found['channel_id']}  ({found['youtube_title']}, {found['subscriber_count']:,} subs)")
        for c in channels:
            if c["display_name"] == "Sam Kohl":
                c.update(found)
                c["search_query"] = "@samkohl"

    # 2) ZAGG: 试搜 "ZAGG Inc" / "ZAGG official"
    print("\n修复 ZAGG...")
    new_id = None
    for q in ["ZAGG Inc", "ZAGG official", "ZAGGdaily"]:
        cid, title = yt_api.search_channel(q)
        print(f"  关键词 '{q}' → {cid}  ({title})")
        if cid and "Topic" not in (title or ""):
            stats = yt_api.channels_batch([cid])
            s = stats[cid]
            for c in channels:
                if c["display_name"] == "ZAGG":
                    c["channel_id"] = cid
                    c["youtube_title"] = title
                    c["search_query"] = q
                    c["subscriber_count"] = s["subscriber_count"]
                    c["uploads_playlist_id"] = s["uploads_playlist_id"]
            new_id = cid
            print(f"  ✅ ZAGG 修复 → {cid}")
            break
    if new_id is None:
        print(f"  ⚠️  ZAGG 官方频道找不到，保留 Topic 频道（仅作占位）")

    # 写回
    data["channels"] = channels
    LIST_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    # 检查 ID 重复
    seen = {}
    for c in channels:
        if c["channel_id"] in seen:
            print(f"\n⚠️  ID 仍重复: {c['display_name']} 与 {seen[c['channel_id']]}")
        seen[c["channel_id"]] = c["display_name"]

    print(f"\n✅ 当前频道总数: {len(channels)}")


if __name__ == "__main__":
    main()
