import os
import sys
import json
import time
import subprocess

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
CONFIG_FILE = os.path.join(CONFIG_DIR, "_default.json")
PROFILE_FILE = os.path.join(CONFIG_DIR, "_my_profile.md")
RESUME_FILE = os.path.join(CONFIG_DIR, "resume.txt")
REQ_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requirements.txt")

# ==========================================
# 依赖热加载 (静默安装高级终端UI库)
# ==========================================
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import track
    import questionary
except ImportError:
    print("🚀 初次启动：正在装备顶配全息化交互组件 (Rich & Questionary)...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "--user", "--break-system-packages", 
        "-r", REQ_FILE, "-q"
    ])
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import track
    import questionary

console = Console()

EXPERIENCE_ENUMS = ["不限", "应届", "1年以内", "1-3年", "3-5年", "5-10年", "10年以上"]
DEGREE_ENUMS = ["不限", "大专", "本科", "硕士", "博士"]
SALARY_ENUMS = ["50K以上", "30-50K", "20-30K", "15-20K", "10-15K", "5-10K", "3-5K", "3K以下"]

def render_title():
    console.print()
    title_text = "[bold cyan]🦅 Boss Job Scout V3.1 初始化战情中心[/bold cyan]\\n[dim]这是一个具备 AI Native 强耦合理解力的高阶猎头平台引擎。[/dim]"
    console.print(Panel(title_text, border_style="cyan", expand=False))
    console.print("要安全、稳定且极其毒辣地为您物色最顶级职位，我们需要做一点简单的授权设定。\\n", style="italic gray62")

def setup_basic_mode():
    console.print(Panel("[bold bright_blue]📡 第一阶段：基础狩猎雷达网络配置 (Basic Mode)[/bold bright_blue]\\n在此环节，系统通过静默高频扫描，捕捉各渠道的高薪猎物，并自动汇集成云端数据库表格。", border_style="blue"))
    time.sleep(1)
    
    # Text Input
    city = questionary.text("1. 城市基站 (你想锁定哪座城市? 例: 上海, 杭州)", default="北京").ask()
    
    # Select Menus
    experience = questionary.select("2. 经验壁垒 (你需要几年的职场门槛?)", choices=EXPERIENCE_ENUMS).ask()
    degree = questionary.select("3. 学历门槛 (你需要什么学历下限?)", choices=DEGREE_ENUMS).ask()
    salary_range = questionary.select("4. 狙击薪资区间 (你期望的底线入场券?)", choices=SALARY_ENUMS).ask()
    
    queries_input = questionary.text("5. 雷达探测词汇 (用逗号隔开多个查询口令，例: AI产品经理,CIO,AI Agent)", default="AI产品经理, AI Agent, AI Native").ask()
    
    if experience == "不限": experience = ""
    if degree == "不限": degree = ""
    queries = [q.strip() for q in queries_input.split(",") if q.strip()]

    with console.status("[bold green]正在重构底层防封爬虫逻辑与雷达配置文件...") as status:
        config_data = {
            "name": "BOSS岗位监控",
            "description": f"监控 {city} 地区高薪AI岗位",
            "topic": f"{city}AI高薪岗位追踪",
            "global_settings": {
                "city": city,
                "experience": experience,
                "degree": degree,
                "opencli_salary": salary_range,
                "min_salary_k": 50 if "50K" in salary_range else 30, # 动态兜底估算
                "max_deep_scrape_limit": -1,
                "max_push_limit": 5
            },
            "channels": {}
        }
        
        for idx, query in enumerate(queries):
            slug = f"boss_track_0{idx+1}" 
            config_data["channels"][slug] = {
                "enabled": True,
                "command": "opencli boss search",
                "query": query,
                "limit": 15
            }
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
            
        time.sleep(1.5)
    console.print(f"✅ [bold green]{CONFIG_FILE} (雷达底座) 覆写完成！[/bold green]\\n")

def setup_pro_mode():
    console.print(Panel("[bold dark_orange]🤖 第二阶段：超体法官心智注入 (Pro Mode)[/bold dark_orange]\\n这里是系统的最高阶杀招。将您的 [bold]脱敏实战经验[/bold] 与 [bold]职场反差拷问[/bold] 注入机器，\\n它将成为您的私人猎聘合伙人，在飞书里为您生成刀刀见血的直推私语。", border_style="dark_orange"))
    
    time.sleep(1)
    
    if os.path.exists(PROFILE_FILE):
        ans = questionary.confirm(f"检测到您已经填写过 {PROFILE_FILE}，是否需要重新进行灵魂拷问?").ask()
        if ans:
            run_old_setup()
    else:
        run_old_setup()
        
    if os.path.exists(RESUME_FILE):
        console.print(f"\\n✅ 检测到你的 Hard Skills 简历墙已在 [italic]{RESUME_FILE}[/italic] 存放就绪。", style="green")
    else:
        console.print(f"\\n❌ 警告：未检测到 [italic]{RESUME_FILE}[/italic]。请稍后务必将你的脱敏纯文本简历拷贝到该文件中。", style="bold red")

def run_old_setup():
    setup_path = os.path.join(os.path.dirname(__file__), "setup_profile.py")
    if os.path.exists(setup_path):
        os.system(f"python3 {setup_path}")
    else:
        console.print("⚠️ 未找到 setup_profile.py 向导文件。", style="yellow")

def main():
    try:
        render_title()
        setup_basic_mode()
        setup_pro_mode()
        
        console.print()
        end_text = "[bold green]配置全部锁定！这台高维战争机器现在正式隶属于你。[/bold green]\\n\\n[dim]接下来的常规启动战术：[/dim]\\n1. 执行 [bold cyan]python3 scripts/run_destinyscout.py[/bold cyan] (每日初筛引擎)\\n2. 执行 [bold cyan]python3 scripts/extract_jd.py[/bold cyan] (深潜突击队)\\n3. 执行 [bold cyan]python3 scripts/push_top5_v3.py[/bold cyan] (大模型灵魂推送)"
        console.print(Panel(end_text, border_style="green"))
    except KeyboardInterrupt:
        console.print("\\n\\n[bold red]向导已强制退出。您随时可以重新运行它。[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()
