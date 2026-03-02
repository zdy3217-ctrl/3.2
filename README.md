# NarratorAI Omega 🎬

全知全能的 AI 视频解说文案创作平台。

## 功能

- **文案创作** — 15种解说风格，流式生成，Ctrl+Enter 快捷触发
- **批量对比** — 同一视频最多5种风格并发生成，横向对比
- **润色改写** — 润色/精简/扩写/改写/自定义，双栏对比，支持迭代
- **爆款雷达** — AI分析最佳解说策略，推荐标题和切入角度
- **多平台适配** — 一键转换 B站/抖音/小红书/YouTube 版本
- **TTS语音合成** — 文案转语音，支持语速调节和下载
- **导出** — TXT纯文本 / SRT字幕（自动分句+时间轴）
- **收藏夹** — 收藏文案和标题，分类管理
- **历史记录** — 搜索、筛选、导出全部
- **工具箱** — 字数↔时长计算器、平台时长参考

## 技术栈

- Next.js 16 + TypeScript + Tailwind CSS 4
- 空氧API (Gemini) + 自动 Fallback
- 仙宫云 index-tts-v2 (TTS)
- localStorage 持久化

## 快速开始

```bash
cd narrator-ai
npm run dev
```

浏览器打开 http://localhost:3000

## 环境变量

编辑 `.env.local`：

```env
LLM_BASE_URL=https://api.aibh.site/v1
LLM_API_KEY=你的API Key
LLM_MODEL=gemini-3-pro
LLM_FALLBACK_MODEL=gemini-2.0-flash
TTS_API_URL=你的TTS服务地址
TTS_API_KEY=你的TTS Key（可选）
```

## 项目结构

```
src/
├── app/
│   ├── api/          # 6个API路由
│   │   ├── adapt/    # 多平台适配
│   │   ├── library/  # 模块库
│   │   ├── llm/      # LLM（流式+Fallback）
│   │   ├── radar/    # 爆款雷达
│   │   ├── rewrite/  # 润色改写
│   │   └── tts/      # 语音合成
│   ├── favorites/    # 收藏夹
│   ├── history/      # 历史记录
│   ├── library/      # 模块库浏览
│   └── settings/     # 设置（含API测试）
├── components/       # 12个组件
└── lib/              # 工具函数
```

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+Enter | 生成文案 |
| Ctrl+B | 切换侧边栏 |
| Ctrl+/ | 快捷键帮助 |
| Enter | 爆款雷达搜索 |
| Esc | 关闭弹窗 |
