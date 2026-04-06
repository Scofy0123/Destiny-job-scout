import os
import shutil

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
TEMPLATE_FILE = os.path.join(CONFIG_DIR, "_user_profile_template.md")
PROFILE_FILE = os.path.join(CONFIG_DIR, "_my_profile.md")

def main():
    print("============================================================")
    print("🧠 赛博猎头配置向导 (User Persona Initialization)")
    print("============================================================\n")
    
    if os.path.exists(PROFILE_FILE):
        print("✅ 检测到你的专属职业画像档案 (`_my_profile.md`) 已经存在。")
        print(f"📁 路径: {PROFILE_FILE}")
        print("💡 提示：找工作的心境发生变化时，随时可以用编辑器打开修改。\n")
        return

    print("⚠️ 尚未检测到私人画像文件！")
    print("正在为你初始化专属职业档案模板...")
    
    try:
        shutil.copy2(TEMPLATE_FILE, PROFILE_FILE)
        print("✅ 初始化成功！")
        print(f"我们已经在以下路径为你生成了模板文件：\n-> {PROFILE_FILE}\n")
        print("🚨 【必须操作】：请立即使用 IDE 或文本编辑器打开上述文件！")
        print("并用最赤裸、最真实的话回答里面的 6 个灵魂提问。系统将把这些信息灌给大模型评委。")
        print("\n填完后再次重启爬虫任务即可体验私人内推服务！")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")

if __name__ == "__main__":
    main()
