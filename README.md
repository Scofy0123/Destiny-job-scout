# 🎯 AI 个性化猎头系统 via BOSS直聘 (Boss-Job-Scout V3.1)

**高阶猎雷达引擎** — 一个基于 [Antigravity IDE](https://github.com/google-deepmind/antigravity) 的 AI Skill。通过全套配置化和反风控爬虫架构，穿透获取极近千字核心 JD，并利用原生大模型结合「私人职场 DNA」进行灵魂推荐。

> 💡 架构设计详见：[PRD 草案与架构](./PRD.md)
> 💡 适用场景：AI 岗位趋势追踪、薪资调研、竞品人才布局分析、基于个人 DNA 的毒辣岗位筛选。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔍 多关键词并行搜索 | 一次任务覆盖多个细分赛道（如 AI产品经理、AI Agent、大模型应用） |
| 🏙️ 城市+薪资精准筛选 | 支持按城市、薪资档位、经验、学历等多维度过滤 |
| 🛡️ 严格数值门槛洗净 | 破解网页端薪资重叠，正则硬性提取上限 K 值（如上限不足 50K 一律静默丢弃） |
| 🤖 多维表格自动入库 | 通过 `lark-cli` 自动将纯净数据增量式追加到飞书多维表格，并打上时间戳与新数据状态 |
| 🚀 Top 5 飞书消息直推 | 执行完毕后，利用飞书机器人提炼薪酬最高的 5 个岗位卡片直推个人聊天框，极速阅览 |
| 🌐 离线降级美学看板 | 若用户未安装/拒绝使用 `lark-cli`，可一键输出极具 2026 风格（毛玻璃悬浮+暗黑渐变）的本地 HTML 高薪看板 |
| ⚙️ 可配置搜索预设 | 默认配置 + 自定义配置，一键切换不同监控策略 |

## 📋 前置条件

- [Node.js](https://nodejs.org/) v18+
- [opencli](https://github.com/jackwener/opencli) 全局安装：
  ```bash
  npm install -g @jackwener/opencli
  ```
- Chrome 浏览器已安装 [opencli 浏览器插件](https://github.com/jackwener/opencli)
- Chrome 中已登录 [BOSS直聘](https://www.zhipin.com/)
- 已安装并配置 [lark-cli](https://github.com/larksuite/cli)（用于飞书表格落库与 IM 推送）
- [Antigravity IDE](https://github.com/google-deepmind/antigravity)

## 🚀 史诗级向导与安装路线 (V3.1)

在克隆下本项目后，**第一步也是唯一的一步，必须激活全局作战配置终端**：

```bash
python3 ~/.gemini/antigravity/skills/boss-job-scout/scripts/boss_scout_init.py
```
*(如果终端缺少渲染库，它会以最高优先级自愈安装 `rich` 与 `questionary`)*

通过这个具有赛博极客风格的 ANSI 互动界面的问诊：
1. **Basic 模式接入**：你可定制探测器需要的下限、城市、经验与薪资波段；
2. **Pro 模式赋能**：系统会将你的简历和性格倾向融合，打造成 `_my_profile.md` 的毒辣底座。

## 📖 常规战斗序列 (执行指令)

在完成 `Step 0` 的环境固化后，接下来的运作可完全解耦为独立管线：

```bash
# 阶段1：泛扫盲（每日自动触发池）
python3 scripts/run_boss_scout.py

# 阶段2：高频穿戴装甲（深潜抓取全量 JD，自带防封咖啡局）
python3 scripts/extract_jd.py

# 阶段3：降维打击推送（用 LLM 的毒辣逻辑解析后，推送至飞书移动端）
python3 scripts/push_top5_v3.py
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

## ⚠️ 顶级防封与反反爬机制 (Anti-Crawler V2)

BOSS直聘的反爬机制极其严苛。本 Skill 经历了生产级的重构，内置了最强安全伞以确保长期稳定运行：

| 策略 | 深度仿生学说明 |
|------|------|
| **乱序盲抽机制** | 单次会话不论配置多少个词，均采用蓄水池抽样**最多只拉取 2 个目标**，彻底阻断固定探测规律 |
| **大波浪拟人休眠** | 丢弃机械化的 5 秒间隔，全面采用 **25-55 秒长尾随机间歇**，完美模拟人类求职者页面停留时间 |
| **单页不翻页** | 强制执行 `limit=15`（第一页数据），从底层隔绝翻页造成的异常流量峰值 |
| **风控即刻熔断** | 一旦抛出 `Network Error` 或 `200404` 登录态失效，立即截断所有队列，并推送已抓取残量数据 |

> [!IMPORTANT]
> **遇到封堵或报错的急救流程（影子替身/Session Mismatch）**
> 
> 当遇到 `Network Error` 或 `xhr.onerror` 时，往往**不是账号被封**，而是 `opencli` 绑定的 Chrome Profile 与你手动登录的浏览器上下文不一致（即“影子替身”问题），或底层 XHR 通道因长时间待机被断开重连。
> 
> **正确的急救步骤：**
> 1. 请**只保留一个**安装了 `opencli` 插件的 Chrome 浏览器窗口。
> 2. 在这个拥有插件的浏览器里，新开一个 Tab，明确输入并打开 `https://www.zhipin.com/web/geek/job`（确保底层环境真正激活并已扫码登录）。
> 3. 随意点击确认页面活蹦乱跳，**切记保留此 Tab 不要关闭**。
> 4. 让 Chrome 留在前台深呼吸，在终端重新执行 `opencli boss search ...` 测试抓取即可满血复活！
## 🔗 相关项目

- [opencli](https://github.com/jackwener/opencli) — 浏览器自动化 CLI 工具
- [ai-topic-fetcher](https://github.com/Scofy0123) — 全网 AI 热点抓取器（姊妹 Skill）
- [ai-topic-to-base](https://github.com/Scofy0123) — 飞书多维表格存储（下游 Skill）

## 📄 License

MIT
