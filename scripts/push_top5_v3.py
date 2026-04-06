import json
import subprocess
import os

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
PROFILE_FILE = os.path.join(CONFIG_DIR, "_my_profile.md")
RESUME_FILE = os.path.join(CONFIG_DIR, "resume.txt")
CONFIG_FILE = os.path.join(CONFIG_DIR, "_default.json")
INPUT_FILE = "topic_results_detailed.json"

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return data.get("global_settings", {})
    return {}

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
         return None
    return result.stdout.strip()

USER_ID = "ou_9590c795acc7fe56a6a7e5bf1c9af1f8"

def push_lark_message(msg_content):
    cmd = [
        "lark-cli", "im", "+messages-send",
        "--as", "bot",
        "--user-id", USER_ID,
        "--markdown", msg_content
    ]
    
    print("Pushing via Lark CLI...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ 猎场情报已通过飞书投递入舱！")
    else:
        print(f"❌ 推送失败: {result.stderr}")


def invoke_llm_judge(job_name, company, jd, profile_text):
    # 构建高维 prompt
    prompt = f"""
你现在是一位全球顶尖高阶猎头合伙人。你的客户（我）的私人职业DNA如下：
{profile_text}
================================
我现在捕获到了一个高薪岗位：
职位：{job_name} @ {company}
岗位详情（JD）：
{jd}
================================
请判断这个岗位和我的职业DNA有多契合。如果非常平庸，你可以毒舌吐槽。
如果非常契合，请：
1. 提炼为一段极度煽动性、能产生Aha Moment的【合伙人私语】。请用第二人称“你”，并在50字以内直击心智（包含FOMO情绪）。
2. 列出一条【核心杠杆】（为什么非我不可）。
3. 列出一条【潜在避坑】（毒辣一眼看出的风险点）。

请直接返回以下Markdown格式的文本，不加任何打招呼和啰嗦废话：
> **💡 合伙人私语：** [你的简短私语内容]
🔹 **你的核心杠杆**：[一条特质]
🔹 **潜在风险/避坑**：[一条风险]
"""
    # 过滤单引号和换行符避免影响bash执行
    safe_prompt = prompt.replace("'", "'\"'\"'").replace("\n", " ")
    
    print(f" -> 🤖 正在唤醒大模型 (Doubao) 进行灵魂估值: {job_name} ...")
    cmd = f"opencli doubao ask '{safe_prompt}'"
    result = run_cmd(cmd)
    
    if not result:
        return "> **💡 合伙人私语：** LLM 估值引擎连线超时或掉线，未获取到个性化分析。\\n🔹 **核心杠杆**：暂缺\\n🔹 **潜在风险**：暂缺"

    if "Role: Assistant" in result:
        # 切割掉 OpenCLI 自带的大量 system prompt 日志
        parts = result.split("Role: Assistant")
        clean_text = parts[-1]
        begin_idx = clean_text.find("💡")
        if begin_idx != -1:
            clean_text = "> **💡" + clean_text[begin_idx+1:]
        return clean_text.replace("Text:", "").strip("- >\\n' ")
        
    return result

def main():
    print("============================================================")
    print("💌 赛博猎头执行局: 大模型猎手私域推送 (V3.0 自动清洗版)")
    print("============================================================\\n")

    if not os.path.exists(INPUT_FILE):
        print("找不到下钻后的详尽数据文件。")
        return

    profile_content = ""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as pf:
            profile_content += "\\n=== 私人职业内心独白 (DNA) ===\\n" + pf.read()
    else:
        profile_content += "通用型高级人才（未填写 DNA）"
        
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, "r") as rf:
            profile_content += "\\n=== 个人历史脱敏简历 (Hard Skills) ===\\n" + rf.read()

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    results = data.get("results", [])
    if not results:
        print("没有可用的数据。")
        return

    settings = get_config()
    max_push = settings.get("max_push_limit", 5)

    sorted_results = sorted(results, key=lambda x: str(x.get("salary", "")), reverse=True)
    if max_push == -1:
        top_targets = sorted_results
    else:
        top_targets = sorted_results[:max_push]

    msg_lines = []
    msg_lines.append("# 🦅 首席情报推送：基于你个人 DNA 计算出的心动猎物池\\n")

    for idx, job in enumerate(top_targets):
        name = job.get("name", "")
        company = job.get("company", "")
        salary = job.get("salary", "")
        boss = job.get("boss", "")
        url = job.get("url", "")
        full_url = url if str(url).startswith("http") else "https://www.zhipin.com" + str(url)
        
        # 猎头估值
        jd_text = job.get("detailed_description", job.get("summary", ""))
        llm_evaluation = invoke_llm_judge(name, company, jd_text, profile_content)

        msg_lines.append(f"## 🎯 {name} @ {company} ({salary})")
        msg_lines.append(f"{llm_evaluation}")
        msg_lines.append(f"🔗 [进入猎场・立刻直聊]({full_url})\\n---")

    final_msg = "\\n".join(msg_lines)
    push_lark_message(final_msg)

if __name__ == "__main__":
    main()
