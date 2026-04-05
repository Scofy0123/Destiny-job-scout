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

### opencli BOSS 完整命令清单

```
opencli boss search <query>        搜索职位（核心命令）
opencli boss joblist               我发布的职位列表
opencli boss recommend             推荐候选人
opencli boss resume <uid>          查看候选人简历
opencli boss detail <security-id>  职位详情
opencli boss chatlist              聊天列表
opencli boss chatmsg <uid>         查看聊天记录
opencli boss greet <uid>           向候选人发招呼
opencli boss batchgreet            批量发招呼
opencli boss send <uid> <text>     发送消息
opencli boss invite <uid>          发面试邀请
opencli boss exchange <uid>        交换联系方式
opencli boss mark <uid>            给候选人打标签
opencli boss stats                 职位数据统计
```

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

### Step 0: 确定配置

如果用户未指定配置，列出所有可用配置并带出简介：

```
请选择搜索配置：
1. 🔹 **默认配置** — [description]
2. 🔹 **[自定义配置A]** — [description]
3. ➕ 新建配置
```

读取配置文件路径：`~/.gemini/antigravity/skills/boss-job-scout/configs/`

### Step 1: 串行抓取

对配置中每个 `enabled: true` 的 channel，**严格串行**执行，每个搜索之间插入 **7 秒随机延迟**：

```bash
opencli boss search "<query>" --limit 15 <extra_args> --format json > <workspace>/temp_boss_<key>.json
sleep $(( RANDOM % 4 + 5 ))   # 5-8 秒随机延迟
```

> ⚠️ **反爬关键规则（必须严格遵守）：**
> 1. **永远不要超过 `limit=15`**：BOSS 直聘使用无限滚动加载，`limit > 15` 会触发伪翻页请求，必被反爬拦截
> 2. **严格串行执行**：禁止并发多个 `opencli boss` 命令
> 3. **每次搜索间隔 ≥ 5 秒**：模拟人类操作节奏
> 4. **单次会话不超过 7 个搜索**：超过容易触发 Session 级冷却
> 5. **遇到 Network Error 立即停止**：不要盲目重试，提示用户去 Chrome 中手动通过 BOSS 的安全验证

### Step 2: AI 过滤与提炼

对抓取到的原始数据进行过滤：
- **排除**：薪资包含"元/天"的（日结实习）、岗位名包含"实习"的
- **排除**：薪资不包含"K"的异常数据
- **去重**：以 `url` 字段为 key 去重

为每条有效岗位生成：
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

### Step 4: 回复用户

汇报：
- 共搜索了几个关键词
- 原始数据多少条，过滤后有效数据多少条
- 展示 Top 10 高薪岗位摘要表格
- 提示可以调用 `ai-topic-to-base` 存入飞书多维表格

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
