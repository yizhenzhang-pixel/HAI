import time
from utils import record_turn, clean_string, console
from ai_response import generate_ai_response

TURN_DELAY_SECONDS = 1

def run_debate(debate_config, model):
    """运行完整的辩论流程"""
    history = []
    topic = debate_config['topic']
    console.print(f"\n========== [bold green]辩论开始: {topic}[/bold green] ==========")

    # --- 裁判介绍 ---
    judge_name = debate_config['judge']['full_name']
    record_turn(history, "系统", f"轮到: {judge_name} (介绍)", "介绍", turn_type="system")
    intro = generate_ai_response(judge_name, "介绍", debate_config, history, model)
    record_turn(history, judge_name, intro, "介绍")
    console.print(intro)
    time.sleep(TURN_DELAY_SECONDS)

    pro_team = debate_config['debaters']['pro']
    con_team = debate_config['debaters']['con']
    rounds = 2

    # --- 开篇立论 ---
    for team in [pro_team, con_team]:
        for debater in team:
            handle_turn(debater, "开篇立论", debate_config, history, model)

    # --- 驳论多轮 ---
    for _ in range(rounds):
        for team in [pro_team, con_team]:
            for debater in team:
                handle_turn(debater, "驳论", debate_config, history, model)

    # --- 总结陈词 ---
    for team in [con_team, pro_team]:  # 反方先总结
        if team:
            handle_turn(team[-1], "总结陈词", debate_config, history, model)

    # --- 裁判评判 ---
    record_turn(history, "系统", f"轮到: {judge_name} (评判)", "评判", turn_type="system")
    judgement = generate_ai_response(judge_name, "评判", debate_config, history, model)
    record_turn(history, judge_name, judgement, "评判")
    console.print(judgement)

    console.print("\n========== [bold red]辩论结束[/bold red] ==========")
    return history

def handle_turn(debater, stage, config, history, model):
    name = debater['full_name']
    team = debater['team']
    is_user = debater.get('is_user', False)

    record_turn(history, "系统", f"轮到: {name} ({stage})", stage, turn_type="system")
    console.print(f"[bold magenta]>>> {stage} - {team}方: {name}[/bold magenta]")

    if is_user:
        console.print("[bold yellow]请您输入发言内容 (输入 'EOF' 结束):[/bold yellow]")
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'EOF':
                    break
                lines.append(line)
            except EOFError:
                break
        text = "\n".join(lines) or "[用户跳过发言]"
    else:
        text = generate_ai_response(name, stage, config, history, model)

    record_turn(history, name, text, stage)
    console.print(text)
    time.sleep(TURN_DELAY_SECONDS)
