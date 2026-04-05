import json
import os
import re
from datetime import datetime

RESULTS_JSON = "topic_results.json"
OUTPUT_HTML = "boss_topic_board.html"

def generate_html():
    if not os.path.exists(RESULTS_JSON):
        print(f"Error: {RESULTS_JSON} not found.")
        return

    with open(RESULTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Re-apply strict filter just in case
    valid_jobs = []
    for item in data.get('results', []):
        salary = str(item.get('salary', ''))
        name = str(item.get('name', ''))
        if "元/天" in salary or "实习" in name:
            continue
        
        match = re.search(r'(\d+)-(\d+)K', salary)
        if match:
            item["_max_k"] = int(match.group(2))
            item["_min_k"] = int(match.group(1))
            if item["_max_k"] >= 50:
                valid_jobs.append(item)

    # Sort
    valid_jobs.sort(key=lambda x: (x.get("_max_k", 0), x.get("_min_k", 0)), reverse=True)

    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    scan_date = data.get("scan_date", today_str)

    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BOSS Job Scout Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0c10;
            --surface-color: rgba(31, 33, 40, 0.65);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --accent-glow: #38bdf8;
            --accent-pink: #f472b6;
            --glass-blur: blur(16px);
        }}

        body {{
            background: radial-gradient(circle at top right, #1e1b4b, var(--bg-color) 40%),
                        radial-gradient(circle at bottom left, #082f49, var(--bg-color) 40%);
            background-color: var(--bg-color);
            background-attachment: fixed;
            color: var(--text-primary);
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}

        header {{
            text-align: center;
            margin-bottom: 4rem;
            animation: fadeDown 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }}

        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 4rem;
            font-weight: 800;
            letter-spacing: -2px;
            margin: 0 0 1rem 0;
            background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.125rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }}

        .badge {{
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent-glow);
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.875rem;
            font-weight: 600;
            border: 1px solid rgba(56, 189, 248, 0.2);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.1);
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}

        .card {{
            background: var(--surface-color);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 2rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            animation: fadeUp 0.6s backwards;
        }}
        
        /* Set animation delays for stagger */
        .card:nth-child(1) {{ animation-delay: 0.1s; }}
        .card:nth-child(2) {{ animation-delay: 0.2s; }}
        .card:nth-child(3) {{ animation-delay: 0.3s; }}
        .card:nth-child(4) {{ animation-delay: 0.4s; }}
        .card:nth-child(5) {{ animation-delay: 0.5s; }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }}

        .card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 
                        0 0 0 1px rgba(255,255,255,0.1) inset;
            background: rgba(40, 43, 50, 0.7);
        }}

        .card:hover::before {{
            transform: translateX(100%);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}

        .salary {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: transparent;
            background: linear-gradient(135deg, #34d399, #10b981);
            -webkit-background-clip: text;
            margin: 0;
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
        }}
        
        .card:nth-child(1) .salary {{ background: linear-gradient(135deg, #ffed4a, #fbbf24); -webkit-background-clip: text; }}
        .card:nth-child(2) .salary {{ background: linear-gradient(135deg, #f472b6, #e81cff); -webkit-background-clip: text; }}
        .card:nth-child(3) .salary {{ background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; }}

        .job-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
            line-height: 1.4;
        }}

        .company {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .company::before {{
            content: '';
            display: inline-block;
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--accent-glow);
        }}

        .skills {{
            margin-top: 1.5rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .skill-tag {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #cbd5e1;
            font-size: 0.75rem;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            transition: all 0.2s;
        }}

        .card:hover .skill-tag {{
            background: rgba(255, 255, 255, 0.1);
        }}

        .action-link {{
            display: inline-block;
            margin-top: 2rem;
            width: 100%;
            text-align: center;
            padding: 0.8rem;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        .action-link:hover {{
            background: var(--text-primary);
            color: var(--bg-color);
            box-shadow: 0 0 20px rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }}

        @keyframes fadeDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .glow-orb {{
            position: fixed;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(56,189,248,0.15) 0%, transparent 70%);
            top: -200px;
            left: -200px;
            pointer-events: none;
            z-index: -1;
            filter: blur(40px);
        }}
    </style>
</head>
<body>
    <div class="glow-orb"></div>
    <div class="container">
        <header>
            <h1>High-Value Targets</h1>
            <div class="subtitle">
                <span>{scan_date}</span>
                <span class="badge">Valid Jobs: {len(valid_jobs)}</span>
            </div>
        </header>

        <div class="grid">
"""

    for i, job in enumerate(valid_jobs):
        salary = job.get('salary', 'N/A')
        name = job.get('name', 'N/A')
        company = job.get('company', 'N/A')
        url = job.get('url', '#')
        full_url = url if url.startswith('http') else 'https://www.zhipin.com' + url
        skills_raw = job.get('skills', '')
        skills = skills_raw.split(',') if skills_raw else []
        
        # Determine specific badge for top 3
        rank_html = ""
        if i == 0: rank_html = "<span style='font-size: 1.5rem;'>👑</span>"
        elif i == 1: rank_html = "<span style='font-size: 1.5rem;'>🚀</span>"
        elif i == 2: rank_html = "<span style='font-size: 1.5rem;'>🔥</span>"

        skills_html = "".join([f"<span class='skill-tag'>{s.strip()}</span>" for s in skills[:4] if s.strip()])
        if len(skills) > 4: skills_html += f"<span class='skill-tag'>+{len(skills)-4}</span>"

        card_html = f"""
            <div class="card">
                <div class="card-header">
                    <p class="salary">{salary}</p>
                    {rank_html}
                </div>
                <h3 class="job-title">{name}</h3>
                <div class="company">{company}</div>
                <div class="skills">
                    {skills_html}
                </div>
                <a href="{full_url}" target="_blank" class="action-link">View Position</a>
            </div>
"""
        html_content += card_html

    html_content += """
        </div>
    </div>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Generated 2026 Interactive Dashboard: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_html()
