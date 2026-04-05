import json
import os
import re
import time
import random
import subprocess
from datetime import datetime

CONFIG_FILE = os.path.expanduser("~/.gemini/antigravity/skills/boss-job-scout/configs/_default.json")
OUTPUT_FILE = "topic_results.json"
MAX_BATCH_SIZE = 2  # 每次最多盲搜词汇数量以避免防爬
JITTER_MIN = 30
JITTER_MAX = 55

def run_scout():
    print(f"Loading config from {CONFIG_FILE}...")
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        
    channels = config.get("channels", {})
    scan_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 抽取所有开启状态的词汇
    channel_keys = [k for k, v in channels.items() if v.get("enabled")]
    
    # [ANTI-CRAWLER: 乱序执行与截断]
    # 打乱顺序，并且单次会话无论多少个词开启，强制只抓最多2个词
    random.shuffle(channel_keys)
    selected_keys = channel_keys[:MAX_BATCH_SIZE]
    
    print("=" * 60)
    print("🔥 BOSS 直聘深度仿生潜行模式已激活 (Anti-Crawler V2.0)")
    print(f"-> 发现 {len(channel_keys)} 个监控项，本次随机抽取 {len(selected_keys)} 个目标：{selected_keys}")
    print("=" * 60)
    print("\n")
    
    all_results = []
    
    for i, key in enumerate(selected_keys):
        channel = channels[key]
        query = channel.get("query")
        limit = channel.get("limit", 15)
        
        print(f"[{i+1}/{len(selected_keys)}] 猎象动作: '{query}' (limit: {limit})")
        cmd = f"opencli boss search '{query}' --limit {limit} --city 上海 --salary 50K以上 --format json"
        
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if process.returncode != 0 or "Network Error" in process.stdout or "Network Error" in process.stderr:
            print(f"❌ 被防御网侦测到了! 执行中断保护！错误日志:")
            print("STDOUT:", process.stdout)
            print("STDERR:", process.stderr)
            break
            
        try:
            json_str = process.stdout.strip()
            start_idx = json_str.find('[')
            end_idx = json_str.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = json_str[start_idx:end_idx+1]
                data = json.loads(json_str)
                print(f" -> 隐秘撤离成功，本词共卷走 {len(data)} 份原始战利品。")
                
                for item in data:
                    item["_query"] = query
                
                all_results.extend(data)
            else:
                print(f" -> 解析失败。API拦截了格式，输出：{process.stdout[:100]}")
        except Exception as e:
            print("❌ 解析JSON崩溃:", e)
            print("STDOUT Dump:", process.stdout)
            
        # [ANTI-CRAWLER: 狂暴大波浪抖动睡眠]
        if i < len(selected_keys) - 1:
            delay = random.randint(JITTER_MIN, JITTER_MAX)
            print(f" -> [仿生休眠启动] 为避免检测，程序强制休眠深呼吸 {delay} 秒，请勿关闭窗口...\n")
            time.sleep(delay)

    print(f"\n✅ 巡查下潜结束。本次累计回传毛数据: {len(all_results)}.")
    print("清洗机介入过滤... (剔除所有包含实习、日结、上限<50K的信息).")
    
    valid_jobs = []
    seen_urls = set()
    
    for job in all_results:
        url = job.get("url", "")
        if url in seen_urls:
            continue
            
        name = str(job.get("name", ""))
        salary = str(job.get("salary", ""))
        
        if "实习" in name or "元/天" in salary or "K" not in salary.upper():
            continue
            
        match = re.search(r'(\d+)-(\d+)K', salary, re.IGNORECASE)
        if match:
            min_k = int(match.group(1))
            max_k = int(match.group(2))
            
            if max_k >= 50:
                job["_max_k"] = max_k
                job["_min_k"] = min_k
                skills = job.get("skills", "")
                skill_list = [s.strip() for s in skills.split(",") if s.strip()]
                job["summary"] = f"【系统评估】匹配查询 '{job.get('_query')}'。需掌握 {', '.join(skill_list[:3])} 等。"
                valid_jobs.append(job)
                seen_urls.add(url)
                
    valid_jobs.sort(key=lambda x: (x.get("_max_k", 0), x.get("_min_k", 0)), reverse=True)
    
    print(f"✅ 清洗完毕！硬通货纯净数据：{len(valid_jobs)} 单待交接。")
    
    output_data = {
        "mode": "platform",
        "platform": "boss",
        "config_name": config.get("name", "Default"),
        "scan_date": scan_date,
        "results": valid_jobs
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ 成果已沉淀至 {OUTPUT_FILE}。等候指令！")

if __name__ == "__main__":
    run_scout()
