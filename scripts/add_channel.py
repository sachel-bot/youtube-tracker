"""
追加一个频道到 channels_list.json
用法: python3 add_channel.py <handle_or_query> <display_name> <group>
例:   python3 add_channel.py @typecase_official Typecase brand
"""
import json
import sys
from pathlib import Path
import yt_api

ROOT = Path(__file__).resolve().parent.parent
LIST_FILE = ROOT / "data" / "channels_list.json"

VALID_GROUPS = {
    "top_tech", "ipad_vertical", "creator_lifestyle",
    "tech_lifestyle", "brand", "tech_media", "apple_vertical"
}


def get_by_handle(handle):
    handle = handle.lstrip("@")
    data = yt_api._get("channels", {
        "forHandle": f"@{handle}",
        "part": "snippet,statistics,contentDetails",
    })
    items = data.get("items", [])
    return items[0] if items else None


def main():
    if len(sys.argv) < 4:
        print("用法: python3 add_channel.py <@handle 或 关键词> <显示名> <分组>")
        print(f"分组可选: {sorted(VALID_GROUPS)}")
        sys.exit(1)

    query, display_name, group = sys.argv[1], sys.argv[2], sys.argv[3]
    if group not in VALID_GROUPS:
        print(f"❌ 分组无效: {group}，可选: {sorted(VALID_GROUPS)}")
        sys.exit(1)

    data = json.loads(LIST_FILE.read_text())
    channels = data["channels"]

    # 重复检查
    for c in channels:
        if c["display_name"].lower() == display_name.lower():
            print(f"⚠️  '{display_name}' 已存在，跳过")
            return

    # 拿频道
    if query.startswith("@"):
        item = get_by_handle(query)
        if item is None:
            print(f"❌ handle {query} 找不到")
            sys.exit(1)
        cid = item["id"]
        title = item["snippet"]["title"]
        subs = int(item["statistics"].get("subscriberCount", 0))
        uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]
    else:
        cid, title = yt_api.search_channel(query)
        if cid is None:
            print(f"❌ 搜不到 '{query}'")
            sys.exit(1)
        stats = yt_api.channels_batch([cid])
        s = stats[cid]
        subs = s["subscriber_count"]
        uploads = s["uploads_playlist_id"]

    new = {
        "display_name": display_name,
        "search_query": query,
        "group": group,
        "channel_id": cid,
        "youtube_title": title,
        "subscriber_count": subs,
        "uploads_playlist_id": uploads,
    }
    channels.append(new)
    data["channels"] = channels
    LIST_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    print(f"✅ 已加入: {display_name}")
    print(f"   频道 ID:   {cid}")
    print(f"   YouTube:   {title}")
    print(f"   订阅数:    {subs:,}")
    print(f"   分组:      {group}")
    print(f"   总频道数:  {len(channels)}")


if __name__ == "__main__":
    main()
