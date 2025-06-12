from config import get_debate_configuration # 保留对原始辩论配置的导入
from roundtable_config import get_roundtable_configuration # 新增：导入圆桌讨论配置函数
from model_init import init_model
from debate_runner import run_debate # 保留对原始辩论运行器的导入
from roundtable_runner import run_roundtable_discussion # 新增：导入圆桌讨论运行函数
from export import export_to_html # export_to_pdf
from html_template import generate_html_content, generate_roundtable_html_content # 导入新的函数
from utils import sanitize_filename, console

def main():
    try:
        console.print("[bold cyan]欢迎使用 AI 智能交互系统！[/bold cyan]")
        console.print("请选择交互模式：")
        console.print("1. 对抗性辩论")
        console.print("2. 圆桌讨论")
        
        mode_choice = ""
        while mode_choice not in ["1", "2"]:
            mode_choice = console.input("[bold yellow]请输入模式编号 (1 或 2): [/bold yellow]")

        model = init_model() # 模型初始化可以提前

        if mode_choice == "1":
            console.print("\n[bold green]--- 对抗性辩论模式 ---[/bold green]")
            debate_config = get_debate_configuration()
            if debate_config:
                history = run_debate(debate_config, model)
                if history:
                    console.print(f"\n[bold green]辩论结束，原始记录如下：[/bold green]")
                    for entry in history: # 假设 history 结构与之前一致
                        speaker = entry.get('speaker', '未知发言者')
                        role = entry.get('role', '')
                        content = entry.get('content', '')
                        console.print(f"[bold magenta]{speaker} ({role}):[/bold magenta] {content}")
                    
                    #HTML导出
                    base_filename = sanitize_filename(debate_config["topic"])
                    html_filename = f"{base_filename}_debate_log.html"
                    html_content = generate_html_content(debate_config["topic"], history, debate_config)
                    export_to_html(html_content, html_filename)
        
        elif mode_choice == "2":
            console.print("\n[bold green]--- 圆桌讨论模式 ---[/bold green]")
            roundtable_config = get_roundtable_configuration()
            if roundtable_config:
                history = run_roundtable_discussion(roundtable_config, model)
                if history:
                    console.print(f"\n[bold green]圆桌讨论结束，讨论记录如下：[/bold green]")
                    for entry in history:
                        speaker = entry.get('speaker', '未知发言者')
                        # stance = entry.get('stance', '') # 或者叫 perspective
                        role_type = entry.get('role_type', '') 
                        content = entry.get('content', '')
                        console.print(f"[bold magenta]{speaker} ({'用户' if role_type == 'user' else 'AI'}):[/bold magenta] {content}")
                    
                    # 为圆桌讨论导出HTML
                    topic = roundtable_config.get("topic", "roundtable_discussion")
                    base_filename = sanitize_filename(topic)
                    html_filename = f"{base_filename}_roundtable_log.html"
                    
                    console.print(f"\n[bold blue]正在生成圆桌讨论的 HTML 报告: {html_filename}[/bold blue]")
                    html_content = generate_roundtable_html_content(topic, history, roundtable_config) 
                    export_to_html(html_content, html_filename)
                    console.print(f"[bold green]✔ HTML 报告已保存至 {html_filename}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]❌ 程序运行时发生意外错误: {e}[/bold red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
