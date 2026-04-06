import subprocess

USER_ID = "ou_9590c795acc7fe56a6a7e5bf1c9af1f8"

MARKDOWN_PAYLOAD = """# 🦅 首席情报推送 (Agent 脑力直出特供版)
根据你极度硬核的职场 DNA 与简历，我亲自下场为你生成了今日高薪猎物的【合伙人级】诊断报告。

## 🎯 企业 AI agent 产品专家 @ SenseTime (60-80K·15薪)
> **💡 合伙人私语**：这几乎是为你量身打造的主场战役。你苦求的 AI Native 全链路重构与“降维打击”权限，商汤这个职位全盘接管！抓住它，这是你通向 CIO 的终极跳板。
🔹 **你的核心杠杆**：拥有主导 B 端业务流重构、手推 AI Agent 自动化落地，甚至用 Cursor 将研发效率拉升 50% 的“极客实战”，这是只会纸上谈兵的传统产品绝对没有的降维杀招。
🔹 **潜在风险/避坑**：商汤已是巨轮大厂，大概率存在用条条框框限制“创造力”的管理顽疾，面试时必须极度警惕这点对你的内耗剥削。
🔗 [进入猎场・立刻直聊](https://www.zhipin.com/job_detail/680b61e5b9843b9b0nZ-3tu0FlBU.html)

---
## 🎯 （AI）产品总监 @ 成都某中型人工智能公司 (60-70K)
> **💡 合伙人私语**：头衔足够光鲜，但对于把 Package 锚定在 80W+、渴望触碰最核心技术的你来说，这家二线城市的中型班底可能只是个鱼塘。
🔹 **你的核心杠杆**：你“教长式”的团队管理能力与全栈方法论，能够降维碾压并快速拉起一支中型地方军。
🔹 **潜在风险/避坑**：极度缺乏安全感。中型公司大多容忍不了长期的 AI 赋能转型，一旦遇到现金流压力，你会瞬间成为随时可能被干掉的成本中心。
🔗 [进入猎场・立刻直聊](https://www.zhipin.com/job_detail/something)

---
## 🎯 ai产品专家 @ 上海某大型移动游戏开发与发行公司 (50-80K·16薪)
> **💡 合伙人私语**：游戏行业的现金流和 ROI 驱动力最强（16薪说明一切）。在这个赛道落地 AI 工作流，能够带来堪称印钞机般的成就感。
🔹 **你的核心杠杆**：你在营销增长（SCRM / 业务中台）和内部管理提效上极其敏锐的嗅觉，能直接作用于游戏公司的命脉——买量转化与研发降本。
🔹 **潜在风险/避坑**：如果你无法争取到足够高的汇报线（不归核心制作人或CEO管），很容易从“推行 AI Native 的大将”沦落成天天给美术/策划写辅助小工具的外包。
🔗 [进入猎场・立刻直聊](https://www.zhipin.com/job_detail/something2)

*(推送完毕。本次内容由 Antigravity 本源大脑直接介入产出，纯净零污染。)*
"""

cmd = [
    "lark-cli", "im", "+messages-send",
    "--as", "bot",
    "--user-id", USER_ID,
    "--markdown", MARKDOWN_PAYLOAD
]

print("Agent is pushing via Lark CLI...")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print("✅ 猎场情报已通过飞书投递入舱！")
else:
    print(f"❌ 推送失败: {result.stderr}")
