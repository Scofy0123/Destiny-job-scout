# 🎯 boss-job-scout

**BOSS直聘岗位监控雷达** — 一个基于 [Antigravity IDE](https://github.com/google-deepmind/antigravity) 的 AI Skill，通过 [opencli](https://github.com/jackwener/opencli) 自动抓取 BOSS直聘高薪岗位数据，实现招聘市场的智能巡查。

> 💡 适用场景：AI 岗位趋势追踪、薪资调研、竞品人才布局分析、求职市场情报收集

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔍 多关键词并行搜索 | 一次任务覆盖多个细分赛道（如 AI产品经理、AI Agent、大模型应用） |
| 🏙️ 城市+薪资精准筛选 | 支持按城市、薪资档位、经验、学历等多维度过滤 |
| 🤖 AI 智能提炼 | 自动过滤实习/日结岗位，生成岗位竞争力评价和技能热词分析 |
| 📊 结构化 JSON 输出 | 标准化格式输出，可直接对接飞书多维表格等下游系统 |
| ⚙️ 可配置搜索预设 | 默认配置 + 自定义配置，一键切换不同监控策略 |

## 📋 前置条件

- [Node.js](https://nodejs.org/) v18+
- [opencli](https://github.com/jackwener/opencli) 全局安装：
  ```bash
  npm install -g @jackwener/opencli
  ```
- Chrome 浏览器已安装 [opencli 浏览器插件](https://github.com/jackwener/opencli)
- Chrome 中已登录 [BOSS直聘](https://www.zhipin.com/)
- [Antigravity IDE](https://github.com/google-deepmind/antigravity)

## 🚀 安装

### 方式一：克隆到 Antigravity Skills 目录

```bash
git clone https://github.com/Scofy0123/boss-job-scout.git ~/.gemini/antigravity/skills/boss-job-scout
```

### 方式二：手动复制

将 `SKILL.md` 和 `configs/` 文件夹复制到 `~/.gemini/antigravity/skills/boss-job-scout/` 目录下。

## 📖 使用方法

在 Antigravity IDE 中对 AI 说：

```
运行 boss-job-scout
```

或者更具体地：

```
运行 boss-job-scout，用默认配置帮我搜一下上海的AI高薪岗位
```

### 示例对话

```
👤 用户：帮我看看上海最近有什么 AI Agent 相关的高薪岗位
🤖 Agent：检测到 boss-job-scout 配置，使用默认配置为您搜索...
         ✅ AI产品经理: 15条
         ✅ AI Agent: 15条
         ...
         过滤后共 46 条有效岗位，以下是 Top 10：
         | 岗位 | 薪资 | 公司 |
         |------|------|------|
         | 首席AI产品官 | 100-150K·16薪 | 某上市人力资源公司 |
         | ...   | ... | ... |
```

## ⚙️ 配置系统

### 默认配置

默认配置覆盖 7 个细分关键词赛道：

| 赛道 | 关键词 | 城市 | 薪资 |
|------|--------|------|------|
| AI产品经理 | `AI产品经理` | 上海 | 50K以上 |
| AI产品总监 | `AI产品总监` | 上海 | 50K以上 |
| AI Agent | `AI Agent` | 上海 | 50K以上 |
| 大模型应用 | `大模型应用` | 上海 | 50K以上 |
| LLM产品 | `LLM产品` | 上海 | 50K以上 |
| AI Native | `AI Native` | 上海 | 50K以上 |
| AI转型 | `AI转型` | 上海 | 50K以上 |

### 自定义配置

在 Antigravity 中对 AI 说：

```
帮我新建一个 boss-job-scout 配置
```

Agent 会引导你选择关键词、城市、薪资等参数，并保存为命名配置。

配置文件存储在 `configs/` 目录下，格式为 JSON。`_default.json` 可修改但不可删除。

## ⚠️ 已知限制与反爬须知

BOSS直聘的反爬机制较为激进。本 Skill 已内置以下安全策略以确保稳定运行：

| 策略 | 说明 |
|------|------|
| **单页不翻页** | `limit` 最大为 15，对应 BOSS 搜索结果第一屏 |
| **串行执行** | 禁止并发多个搜索，每次间隔 5-8 秒 |
| **单次上限** | 单次会话建议不超过 7 个搜索 |
| **错误即停** | 遇到 Network Error 立即停止，不盲目重试 |

如果触发了 BOSS 的安全验证（图片验证码），需要：
1. 在装有 opencli 插件的 Chrome 中打开 [zhipin.com](https://www.zhipin.com/)
2. 手动通过验证码
3. 等待 5-10 分钟后重试

## 🔗 相关项目

- [opencli](https://github.com/jackwener/opencli) — 浏览器自动化 CLI 工具
- [ai-topic-fetcher](https://github.com/Scofy0123) — 全网 AI 热点抓取器（姊妹 Skill）
- [ai-topic-to-base](https://github.com/Scofy0123) — 飞书多维表格存储（下游 Skill）

## 📄 License

MIT
