"""共用：直接调 YouTube REST API（用 requests，自动走 http_proxy）"""
import os
import time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent

# API key 加载顺序: 环境变量 > .env 文件
def _load_key():
    k = os.environ.get("YT_API_KEY")
    if k:
        return k
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line.startswith("YT_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("未找到 YT_API_KEY。请在 .env 写入 YT_API_KEY=xxx 或设置环境变量。")

API_KEY = _load_key()
BASE = "https://www.googleapis.com/youtube/v3"
TIMEOUT = 30

_session = requests.Session()


def _get(path, params, retries=3):
    params = {**params, "key": API_KEY}
    last_err = None
    for attempt in range(retries):
        try:
            r = _session.get(f"{BASE}/{path}", params=params, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (403, 400):
                raise RuntimeError(f"API {r.status_code}: {r.text[:300]}")
            last_err = f"HTTP {r.status_code}: {r.text[:200]}"
        except requests.exceptions.RequestException as e:
            last_err = str(e)
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{path} failed after {retries} retries: {last_err}")


def search_channel(query):
    data = _get("search", {
        "q": query, "type": "channel", "part": "snippet", "maxResults": 1,
    })
    items = data.get("items", [])
    if not items:
        return None, None
    snip = items[0]["snippet"]
    return snip["channelId"], snip["channelTitle"]


def channels_batch(channel_ids):
    out = {}
    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i:i+50]
        data = _get("channels", {
            "id": ",".join(batch),
            "part": "snippet,statistics,contentDetails",
        })
        for item in data.get("items", []):
            out[item["id"]] = {
                "title": item["snippet"]["title"],
                "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
                "uploads_playlist_id": item["contentDetails"]["relatedPlaylists"]["uploads"],
            }
    return out


def playlist_items(playlist_id, max_items=10):
    data = _get("playlistItems", {
        "playlistId": playlist_id, "part": "contentDetails", "maxResults": max_items,
    })
    return [it["contentDetails"]["videoId"] for it in data.get("items", [])]


def videos_batch(video_ids):
    out = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        data = _get("videos", {
            "id": ",".join(batch),
            "part": "snippet,statistics,contentDetails",
        })
        out.extend(data.get("items", []))
    return out
