import json
import time
import random
import subprocess
import os

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
CONFIG_FILE = os.path.join(CONFIG_DIR, "_default.json")
INPUT_FILE = "topic_results.json"
OUTPUT_FILE = "topic_results_detailed.json"

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return data.get("global_settings", {})
    return {}

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing: {cmd}\\nStderr: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except:
        return None

def main():
    settings = get_config()
    max_extract = settings.get("max_deep_scrape_limit", -1)

    print("============================================================")
    print("🕷️ 极光雷达: 深度下钻 (Deep Scrape Pipeline) 启动")
    if max_extract == -1:
        print("-> 目标: 提取本日 所有 初筛匹配岗位的纯文本长篇 JD 供大模型分析")
    else:
        print(f"-> 目标: 提取薪资排名前 {max_extract} 岗位的纯文本长篇 JD 供大模型分析")
    print("============================================================\\n")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到初始数据 {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    results = data.get("results", [])
    if not results:
        print("未发现洗过的高薪猎物，结束提取。")
        return

    # 按薪资从高到低排序 (粗略排序即可，这里使用长度或字符串，也可以让调用方决定，目前 topic_results 中已较粗略洗净)
    sorted_results = sorted(results, key=lambda x: str(x.get("salary", "")), reverse=True)
    if max_extract == -1:
        top_targets = sorted_results
    else:
        top_targets = sorted_results[:max_extract]

    detailed_results = []

    for i, target in enumerate(top_targets):
        sec_id = target.get("security_id")
        name = target.get("name")
        company = target.get("company")
        salary = target.get("salary")
        
        print(f"[{i+1}/{len(top_targets)}] 潜水下探: {name} @ {company} ({salary})")

        if not sec_id:
            print(" -> 无安全ID，跳过。")
            detailed_results.append(target)
            continue

        cmd = f"opencli boss detail '{sec_id}' --format json"
        detailed_data = run_cmd(cmd)
        
        if detailed_data and isinstance(detailed_data, list) and len(detailed_data) > 0:
            print(" -> 猎物剖析完毕，成功拽出底层隐秘 JD。")
            # 融合原始数据与详情数据
            detail_info = detailed_data[0]
            target["detailed_description"] = detail_info.get("description", "")
            target["detailed_welfare"] = detail_info.get("welfare", "")
            target["boss_title"] = detail_info.get("boss_title", "")
        else:
            print(" -> 详情提取失败或被封阻。")
            target["detailed_description"] = "无详细描述"

        detailed_results.append(target)

        if i < len(top_targets) - 1:
            # 每抓取 5 个目标，强制进入“长波浪休眠” (模拟人类去倒咖啡或回消息，休眠 1~2 分钟)
            if (i + 1) % 5 == 0:
                coffee_break = random.randint(60, 120)
                print(f" -> [☕ 咖啡防封机制] 已连续作战 5 次，强制深度休眠 {coffee_break} 秒伪装真实人类行为...")
                time.sleep(coffee_break)
            else:
                delay = random.randint(25, 45)
                print(f" -> [大波浪避险机制] 常规氧气潜伏 {delay} 秒以切断频率波痕...")
                time.sleep(delay)

    data["results"] = detailed_results
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\\n✅ 下钻提取全过程完毕，共 {len(top_targets)} 份带有灵魂 JD 的情报已被封装入库。")

if __name__ == "__main__":
    main()
