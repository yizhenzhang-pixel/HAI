from rich.console import Console
from rich.prompt import Prompt
from utils import clean_string

console = Console()

def get_debate_configuration():
    """通过交互式输入获取辩论设置"""
    console.print("\n--- [bold cyan]设置辩论参数[/bold cyan] ---")

    topic = Prompt.ask("请输入辩论主题", default="强大的AI模型应该开源吗？")
    topic = clean_string(topic)

    while True:
        try:
            num_debaters = int(Prompt.ask("请输入每方队伍的辩手数量", default="1"))
            if num_debaters > 0:
                break
            console.print("[yellow]辩手数量必须大于 0。[/yellow]")
        except ValueError:
            console.print("[red]请输入有效的数字。[/red]")

    user_participates = Prompt.ask("您想亲自参与辩论吗? (yes/no)", choices=["yes", "no"], default="no") == 'yes'
    user_info = None
    user_team = None

    if user_participates:
        name = Prompt.ask("请输入您的名字")
        team = Prompt.ask("您想加入哪一方？ (pro/con)", choices=["pro", "con"], default="pro")
        stance = Prompt.ask("请输入您的核心立场")
        user_info = {
            "full_name": clean_string(name),
            "stance": clean_string(stance),
            "is_user": True,
            "team": team
        }
        user_team = team

    default_names = {
        "pro": ["杨立昆", "吴恩达", "艾伦·纽厄尔", "克劳德·香农"],
        "con": ["辛顿", "马斯克", "布隆", "谢尔盖·布林"]
    }
    default_stances = {
        "pro": "支持AI开源",
        "con": "反对AI开源"
    }

    debaters = {"pro": [], "con": []}
    for side in ["pro", "con"]:
        count = num_debaters - (1 if user_participates and user_team == side else 0)
        if user_participates and user_team == side:
            debaters[side].append(user_info)

        for i in range(count):
            name = Prompt.ask(f"请输入 {side.upper()} 方 AI 辩手 {i+1} 的名字", default=default_names[side][i] if i < len(default_names[side]) else f"{side}_AI_{i+1}")
            stance = Prompt.ask(f"请输入 AI 辩手 {name} 的立场", default=default_stances[side])
            debaters[side].append({
                "full_name": clean_string(name),
                "stance": clean_string(stance),
                "is_user": False,
                "team": side
            })

    judge_name = Prompt.ask("请输入裁判的名字", default="本吉奥")
    judge_role = Prompt.ask("请输入裁判的角色", default="关注逻辑与公平性")

    judge = {
        "full_name": clean_string(judge_name),
        "role": clean_string(judge_role)
    }

    return {
        "topic": topic,
        "debaters": debaters,
        "judge": judge,
        "user_participates": user_participates,
        "user_debater_info": user_info,
        "num_debaters_per_team": num_debaters
    }
