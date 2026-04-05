import json
import subprocess
import time
import sys

BASE_TOKEN = "Ll50bGx3saIBWEs4T0lca0mjniz"
TABLE_ID = "tbly2p4ZLmj6styh"
FIRST_FIELD_ID = "fldr4jDDp0"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing: {cmd}\nStderr: {result.stderr}")
        return None
    try:
        j = json.loads(result.stdout)
        if not j.get('ok'):
           print(f"Lark API Error: {j}") 
        return j
    except:
        return result.stdout

print("Fields are already set up.")
# Wait just to be safe
time.sleep(1)

with open("topic_results.json", "r") as f:
    data = json.load(f)

scan_date = data.get("scan_date", "Unknown Date")
sorted_results = sorted(data.get("results", []), key=lambda x: (x.get("search_keyword", ""), x.get("salary", "")))

print(f"Preparing to insert {len(sorted_results)} records...")
for idx, item in enumerate(sorted_results):
    url = item.get("url", "")
    full_url = url if url.startswith("http") else "https://www.zhipin.com" + url
    record_json = {
        "岗位名称": str(item.get("name", "Unknown")),
        "薪资": str(item.get("salary", "Unknown")),
        "公司": str(item.get("company", "Unknown")),
        "关键词": str(item.get("_query", "Unknown")),
        "抓取日期": str(scan_date),
        "抓取状态": "新数据",
        "标签/要求": str(item.get("summary", "Unknown")),
        "详情链接": full_url
    }
    
    fields_str = json.dumps(record_json, ensure_ascii=False).replace("'", "'\\''")
    cmd = f"lark-cli base +record-upsert --base-token {BASE_TOKEN} --table-id {TABLE_ID} --json '{fields_str}'"
    res = run_cmd(cmd)
    if (idx + 1) % 10 == 0:
        print(f"Inserted {idx+1}/{len(sorted_results)}")

print("All Done!")
