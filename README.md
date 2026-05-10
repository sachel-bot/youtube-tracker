# 📺 YouTube 北美 iPad 配件内容情报

> Typecase + 竞品 + 类目监控 · 跨战役复用

监控 56 个 YouTube 频道（iPad 配件竞品 / 头部数码博主 / iPad 真实使用场景 / Lifestyle / 3C 品牌学习），自动抓取最新视频、计算 8 个数据维度、生成每日刷新的可视化看板。

## 维度

1. engagement_rate（互动率）
2. comment_rate（评论率）
3. video_length_type（Shorts/Short/Medium/Long）
4. content_tags（iPad配件相关 / 创作 / 学生 / 商务 / 其他Apple）
5. hot_level（🔥 上升 / 💥 强 / 🎯 百万 / 🚀 现象级）
6. view_to_sub_ratio（频道爆款率）
7. video_type（评测 / 开箱 / 对比 / 装机 / 教学 / vlog）
8. brand_mentions（Brydge / HOU / Logitech / Apple键盘 等品牌关键词）

## 频道分组

- **A** 竞品 + 自家追踪 (9): Logitech, ESR, ZAGG, Fintie, Inateck, Arteck, Doqo, Apple, Typecase
- **B** iPad 垂直内容 + 媒体 (9): 9to5Toys, AppleSauce, Tom's Guide, Gizmodo, Engadget, The Verge, 9to5Mac, Christopher Lawley, Tim Chaten
- **C** 头部数码 (5): MKBHD, iJustine, Linus Tech Tips, Dave Lee, Snazzy Labs
- **D** iPad 真实使用场景 (22): 学生 / 艺术创作 / 商务
- **E** Lifestyle 高复购 (6): Pick Up Limes, Lavendaire, etc.
- **F** 3C 品牌学习 (5): Anker, Belkin, Satechi, Twelve South, Native Union

## 本地启动

```bash
# 装依赖
pip3 install requests 'urllib3<2'

# 设 API key
echo "YT_API_KEY=你的_youtube_api_v3_key" > .env

# 抓数据
python3 scripts/step1_v2.py        # 首次：搜频道 ID（~4000 配额）
python3 scripts/step1c_finalize.py # 修复 + 删除问题频道
python3 scripts/step2_fetch_videos.py  # 抓视频 + 算维度（~80 配额）
python3 scripts/step4_build_dashboard.py  # 生成 dashboard.html
```

## 自动刷新

- macOS launchd 配置在 `~/Library/LaunchAgents/com.youtube-tracker.{refresh,server}.plist`
- 每天 9:00 自动跑 refresh.sh，本地 server 8765 端口常驻

## 配额成本

- 首次（搜 56 频道 + 抓视频）: ~4000 单位
- 之后每天: ~80 单位（远低于 10000/天免费额度）

## 数据文件

- `data/channels_list.json` - 频道清单
- `data/channels_data.json` - 总数据（含 8 维度）
- `data/channels/{name}.json` - 每频道单独
- `dashboard.html` - 可视化看板（fetch 模式）
