---
name: boss-job-scout
version: 1.0.0
description: "BOSS直聘岗位监控雷达。通过 opencli 抓取 BOSS 直聘高薪岗位数据，支持多关键词并行搜索、薪资过滤、结构化 JSON 输出。当用户需要监控招聘市场、追踪特定岗位趋势、做薪资调研时使用。"
metadata:
  requires:
    bins: ["opencli"]
  cliHelp: "This is an agentic workflow skill, no custom CLI."
---

# boss-job-scout 工作流

> **前置条件：**
> - 全局安装 `opencli`（`npm install -g @jackwener/opencli`）
> - 全局安装飞书命令行工具 `lark-cli`（用于同步表格和推送消息）
> - Chrome 浏览器已安装 opencli 插件
> - Chrome 中已登录 [BOSS直聘](https://www.zhipin.com/)

## 核心能力

通过 `opencli boss search` 抓取 BOSS 直聘的岗位数据，支持：

| 能力 | 说明 |
|------|------|
| 关键词搜索 | 按岗位名/技能关键词搜索 |
| 城市筛选 | `--city 上海/北京/杭州/深圳/...` |
| 薪资过滤 | `--salary 50K以上/30-50K/20-30K/...` |
| 经验/学历 | `--experience 3-5年` / `--degree 本科` |
| 行业筛选 | `--industry 互联网` |

### opencli BOSS 核心命令与进阶能力

```bash
opencli boss search <query>        # 搜索职位（本执行核心命令）
```

> **渐进式披露：**
> 如果用户需要对找到的候选人继续执行“打招呼”、“主动沟通”、“发面试邀请”等动作，请**先阅读以下参考指引**获取完整的高阶命令，切勿在常规监控任务中自作主张。
> 📖 [高阶动作操作指引](file://~/.gemini/antigravity/skills/boss-job-scout/references/opencli-boss-advanced-commands.md)

## 配置系统

配置文件存储在本 Skill 目录下的 `configs/` 文件夹中。

```
boss-job-scout/
├── SKILL.md
└── configs/
    └── _default.json    # 默认配置（可改不可删）
```

每个配置文件格式：

```json
{
  "name": "配置名称",
  "description": "配置简介",
  "topic": "监控主题",
  "channels": {
    "channel_key": {
      "enabled": true,
      "command": "opencli boss search",
      "query": "搜索关键词",
      "limit": 15,
      "threshold": { "field": "salary", "condition": "过滤规则" },
      "extra_args": "--city 上海 --salary 50K以上",
      "output_columns": ["name","salary","company","area","experience","degree","skills","url"]
    }
  }
}
```

## 执行流程

### Step 0: 必须进行环境检查

在开始任何操作前，**必须首先通过 `lark-cli --version` 等命令检查用户本地是否已经安装了飞书 CLI（`lark-cli`）**。
- 如果没有安装，请**立刻停止执行**，提醒用户缺少关键环境依赖。
- 同时在回复中，直接使用以下原话引导用户授权安装：“检测到未安装 `lark-cli`，请将这条指令直接发给我，让我来帮你全自动安装：\n`帮我装一下所有的东西：https://github.com/larksuite/cli/blob/main/README.zh.md`”

### Step 1: 确定配置

如果用户未指定配置，列出所有可用配置并带出简介：

```
请选择搜索配置：
1. 🔹 **默认配置** — [description]
2. 🔹 **[自定义配置A]** — [description]
3. ➕ 新建配置
```

读取配置文件路径：`~/.gemini/antigravity/skills/boss-job-scout/configs/`

### Step 1: 仿生学乱序抽查 (Anti-Crawler V2)

从配置中获取所有 `enabled: true` 的 channel，**绝对不能全量抓取**！必须执行**大波浪少食多餐策略**：每次运行必须随机打乱这些 channel，并**只抽取最多 2 个目标**进行抓取。且在两次搜索之间插入 **25到55秒 的大波浪拟人休眠**。在休眠期间，向用户发出前台唤醒警告。

你可以直接调用预置爬虫管控核心：
```bash
python3 ~/.gemini/antigravity/skills/boss-job-scout/scripts/run_boss_scout.py
```

> ⚠️ **大厂级反爬铁律（违反即刻封号）：**
> 1. **乱序微批次**：单次运行最大遍历数量 ≤ 2 个词！拒绝机械拉网。
> 2. **深呼吸长休眠**：禁止 5 秒的小儿科休眠。间隔必须随机落在 `25~55` 秒区间。
> 3. **永远不要超过 `limit=15`**：杜绝跨页动作。
> 4. **遇到 Network Error 或 200404 立即停止**：直接报错上抛并要求用户重登 Boss 直聘并走手工图灵机测试（图片验证码滑块）。

### Step 2: AI 过滤与提炼

对抓取到的原始数据，必须进行**两道过滤**：

1. **数值硬过滤（硬性拦截）**：
   - 使用正则 `(\d+)-(\d+)K` 提取 `salary` 字符串中的上限数值（Max K）。
   - **严格验证规则**：如果提取出的上限数值 `< 50`，则判定为无效数据，直接丢弃（即保留 30-60K，但必须剔除 20-40K、15-20K 等上限未触达 50K 的数据）。
   - **排除异常**：薪资包含"元/天"的（日结实习）、薪资没有"K"的、以及岗位名包含"实习"的，全部剔除。
   - **去重**：以 `url` 字段为唯一标识去重。

2. **AI 信息提炼**：
为每条存活下来的有效高薪岗位生成：
- **一句话评价**：基于岗位名、薪资、公司、技能要求综合评价该岗位的市场竞争力和前景
- **技能热词提取**：从 skills 字段中提取关键技术趋势

### Step 3: 输出结构化 JSON

输出到工作区 `<workspace>/topic_results.json`：

```json
{
  "mode": "platform",
  "platform": "boss",
  "config_name": "默认配置",
  "scan_date": "2026-04-05",
  "results": [
    {
      "title": "AI产品经理",
      "author": "某大型互联网公司",
      "heat": "50-80K·16薪",
      "url": "https://www.zhipin.com/job_detail/xxx.html",
      "query": "AI产品经理",
      "summary": "头部AI公司的产品负责人岗，要求C端+AI双重背景",
      "shootability": "适合做薪资对比类内容，16薪是亮点"
    }
  ]
}
```

### Step 4: 路由输出（分流处理）

Agent 根据 `Step 0` 的环境检查结果，采取不同的输出策略：

#### 分支 A：用户已授权使用 lark-cli（默认方案）
1. **表格自动入库**：你可以安全地调用配套脚本自动把脱水 JSON 的增量数据插入基座表：
   ```bash
   python3 ~/.gemini/antigravity/skills/boss-job-scout/scripts/upload_to_base.py
   ```
2. **Top 5 消息直推**：调用预置脚本引擎，将最高薪数据直捣黄龙推送到私聊：
   ```bash
   python3 ~/.gemini/antigravity/skills/boss-job-scout/scripts/push_top5.py
   ```

#### 分支 B：离线降级方案（用户未安装且拒绝授权）
如果用户回复“跳过”，则启用纯本地沉淀方案：
1. **终端降级输出**：不要停止运行，直接以极具视觉冲击力的 Markdown 列表在当前聊天窗口打印 Top 5 高薪简报。
2. **2026 美学大屏生成**：在执行脚本前，**务必先检查脚本文件是否存在并确认 Python 3 环境可用**。确认无误后，调用本技能目录下的生成脚本：
   ```bash
   python3 ~/.gemini/antigravity/skills/boss-job-scout/scripts/generate_html.py
   ```
   该脚本会提取过滤后的高薪数据，在当前工作区生成一个包含深色模式、毛玻璃特效（Glassmorphism）、动态卡片悬浮、双主题无缝切换的最新 HTML 本地看板 `boss_topic_board.html`。
3. 把全量数据存一份脱水版到本地 `topic_results_filtered.json` 供备查。

> **✅ 强制防呆与自我校验机制 (Verification Guard & Fail-Safe)：**
> 任何依赖项调用（生成 HTML 或 lark-cli 推送），Agent **必须**检视执行后的 stdout / stderr 或返回值！
> 1. 如果顺利成功，继续往后执行。
> 2. **如果出现任何错误、异常或命令不存在**：切勿替用户作主张忽略报错！除了向用户透出错误日志外，必须**第一时间主动向用户请示**接下来的对策（比如：“推送失败，是否尝试离线降级方案？”或“脚本运行报错，需要我怎么处理？”）。

### Step 5: 回复用户

向用户总结汇报：
- 共搜索了哪几个关键词。
- 原始数据多少条，经过硬性过滤后存活的最新有效数据多少条。
- 如果是分支 A 且验证成功：提示数据已自动入库视图，并且卡片简报已推送到飞书聊天。
- 如果是分支 B 且验证成功：提示数据已生成为本地具有最新交互特效的 HTML 数据大屏，并**温柔提示**：“如果希望下次全自动连通落库，随时叫我帮你安装 lark-cli 哦”。

## 配置管理

### 新建配置

引导用户选择：
1. 监控关键词（可多个）
2. 目标城市
3. 薪资范围
4. 经验/学历要求（可选）
5. 配置命名

### 修改/删除配置

- `_default.json` 可修改内容，不可删除文件
- 其他配置可自由修改和删除

## 错误处理

| 错误 | 原因 | 处理 |
|------|------|------|
| `Network Error` (首页就失败) | BOSS Session 被冷却 | 停止执行，提示用户在 Chrome 中打开 zhipin.com 手动通过验证码，等待 5-10 分钟 |
| `Network Error` (翻页时失败) | 触发了翻页反爬 | 不翻页，使用更多细分关键词替代 |
| 数据量不足 | 关键词太窄或城市限制 | 建议拆分为更多细分关键词，或放宽城市/薪资条件 |

## 已知限制

1. BOSS 直聘反爬较激进，单次 Session 内搜索次数有上限（建议 ≤ 7 次）
2. `limit` 最大为 15（单页），不支持翻页
3. 需要 Chrome 保持 BOSS 直聘的登录状态
4. 密集请求后可能触发图片验证码，需人工干预
