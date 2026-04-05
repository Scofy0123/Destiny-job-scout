import json
import re
import subprocess

USER_ID = "ou_9590c795acc7fe56a6a7e5bf1c9af1f8"

with open("topic_results.json", "r") as f:
    data = json.load(f)

valid = []
for item in data.get('results', []):
    salary = str(item.get('salary', ''))
    name = str(item.get('name', ''))
    if "元/天" in salary or "实习" in name:
        continue
    
    match = re.search(r'(\d+)-(\d+)K', salary)
    if match:
        min_k, max_k = int(match.group(1)), int(match.group(2))
        if max_k >= 50:
            item["_max_k"] = max_k
            item["_min_k"] = min_k
            valid.append(item)

# Sort descending
valid.sort(key=lambda x: (x.get("_max_k", 0), x.get("_min_k", 0)), reverse=True)
top5 = valid[:5]

md_lines = ["🔥 **今日高薪哨兵侦测报告 (AI 岗)**\n"]
md_lines.append(f"📡 *扫描总量：{len(data.get('results', []))}，达标存活（上限≥50K）：{len(valid)}*\n")
md_lines.append("---\n")

for i, job in enumerate(top5):
    salary = job.get('salary')
    name = job.get('name')
    company = job.get('company')
    url = job.get('url', '')
    full_url = url if url.startswith('http') else 'https://www.zhipin.com' + url
    
    md_lines.append(f"{i+1}. 💰 `{salary}` | **{name}** @ {company}")
    md_lines.append(f"   🔗 [点击这里快速投递直聊]({full_url})\n")

md_lines.append("---\n💡 *数据已全量静默入库至多维表格的新数据视图。*")

markdown_content = "\n".join(md_lines)
print(markdown_content)

# Send to Feishu Bot
# We use properly escaped quotes for the subprocess call
cmd = [
    "lark-cli", "im", "+messages-send",
    "--as", "bot",
    "--user-id", USER_ID,
    "--markdown", markdown_content
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print("\n✅ 推送成功！")
else:
    print(f"\n❌ 推送失败：{result.stderr}")
