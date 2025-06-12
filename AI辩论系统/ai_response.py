import textwrap
from utils import clean_string, console

def generate_ai_response(speaker_name, stage, config, history, model):
    """构建 prompt 并调用 Gemini 生成发言"""
    role_info = ""
    speaker_data = None
    team = None

    for side, team_list in config['debaters'].items():
        for debater in team_list:
            if clean_string(debater['full_name']) == clean_string(speaker_name):
                speaker_data = debater
                role_info = debater['stance']
                team = side
                break

    if not speaker_data and clean_string(config['judge']['full_name']) == clean_string(speaker_name):
        speaker_data = config['judge']
        role_info = config['judge']['role']

    if not role_info:
        return "[无法识别角色信息]"

    prompt = f"你是 {speaker_name}，当前阶段：{stage}\n立场/任务：{role_info}\n"
    prompt += f"辩题是：“{config['topic']}”\n"

    if team:
        prompt += f"\n你的队伍：{team}方\n"
        opp = 'con' if team == 'pro' else 'pro'
        prompt += f"我方队友：\n"
        for d in config['debaters'][team]:
            if d['full_name'] != speaker_name:
                prompt += f"- {d['full_name']}: {d['stance']}\n"
        prompt += f"对方辩手：\n"
        for d in config['debaters'][opp]:
            prompt += f"- {d['full_name']}: {d['stance']}\n"

    if history:
        recent = [t for t in history if t['type'] == 'speech'][-6:]
        prompt += "\n最近发言摘要：\n"
        for t in recent:
            short = textwrap.shorten(t['text'], width=1000, placeholder="...")
            prompt += f"- {t['speaker']} ({t['stage']}): {short}\n"

    prompt += f"\n请根据当前阶段，输出你的发言，不要写任何前缀，例如“我认为”、“作为XXX”。"

    try:
        response = model.generate_content(prompt)
        return clean_string(response.text)
    except Exception as e:
        return f"[生成失败: {e}]"
