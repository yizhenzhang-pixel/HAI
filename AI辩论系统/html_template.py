from utils import clean_string
import re

def generate_html_content(topic, history, debate_config): # <-- 添加 debate_config 参数
    """根据辩论历史生成带有新样式的 HTML 内容字符串"""
    # 使用更新后的 CSS 样式
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>辩论记录: {topic}</title>
    <style>
        @font-face {{
            font-family: 'SourceHanSans'; /* 定义字体名称 */
            src: url('file:///Users/wooton/Library/Fonts/SourceHanSansSC-Regular.otf'); /* 指定本地字体文件路径 */
        }}

        body {{
            font-family: 'SourceHanSans', "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.7; /* 稍微调整行高 */
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 40px auto; /* 减少上下边距 */
            background-color: #ffffff;
            padding: 30px 40px; /* 减少内边距 */
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-radius: 8px;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 40px; /* 减少标题下方间距 */
            font-weight: bold;
            font-size: 1.8em;
        }}
        .turn {{
            margin-bottom: 20px; /* 减少发言之间的间距 */
            padding-bottom: 15px; /* 减少发言底部留白 */
            border-bottom: 1px solid #f0f0f0;
        }}
        .turn:last-child {{
             border-bottom: none;
        }}
        .speaker {{
            font-weight: 600;
            color: black;
            display: block;
            margin-bottom: 8px; /* 减少发言者和文本之间的间距 */
            font-size: 1.1em;
        }}
        .speaker .icon {{
             margin-right: 8px; /* 减少图标间距 */
             font-size: 1.15em;
             vertical-align: -1px;
        }}
        .text {{
            margin-top: 5px; /* 减少文本上边距 */
            color: #444;
            white-space: pre-wrap; /* 保留换行和空格 */
            line-height: 1.7; /* 调整正文行高 */
        }}
        .stage {{
            font-style: normal;
            color: black;
            margin: 45px 0 25px 0; /* 调整阶段标题的上下间距 */
            text-align: center;
            font-size: 1.4em;
            font-weight: 600;
            padding-bottom: 10px;
            border-bottom: 2px solid #ddd;
            width: fit-content;
            margin-left: auto;
            margin-right: auto;
        }}
        .stage .icon {{
            margin-right: 10px;
            font-size: 1.05em;
            vertical-align: middle;
        }}
        b, strong {{ /* 确保加粗效果明显 */
            font-weight: bold;
            color: #111; /* 可以让加粗颜色深一点 */
        }}
    </style>
</head>
<body>
    <div class="container"> <!-- 添加容器 -->
        <h1>辩论记录: {topic}</h1>
"""
    # --- HTML 内容生成逻辑 ---
    current_stage = ""
    stage_icons = {
        "介绍": "📜",
        "开篇立论": "🎤",
        "驳论": "⚔️",
        "总结陈词": "🏁",
        "评判": "🏆"
    }

    for turn in history:
        # 去掉发言者名字中的 "(模拟)"
        speaker = turn['speaker'].replace(" (模拟)", "")
        raw_text = turn['text']

        # 处理 Markdown 加粗标记为 HTML <b> 标签
        # 先处理双星号，再处理单星号
        processed_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', raw_text)
        processed_text = re.sub(r'\*(.*?)\*', r'<b>\1</b>', processed_text)

        # 处理换行符
        text_html = processed_text.replace('\n', '<br>')

        turn_type = turn.get('type', 'speech')
        stage_indicator = ""
        recorded_stage = turn.get('stage')

        # --- Stage detection logic remains the same ---
        if recorded_stage:
             if "驳论" in recorded_stage: stage_indicator = "驳论"
             else: stage_indicator = recorded_stage
        elif "裁判介绍" in turn['speaker']: stage_indicator = "介绍" # Use original speaker name for detection
        elif "裁判评判" in turn['speaker']: stage_indicator = "评判" # Use original speaker name for detection
        elif turn_type == "speech" and not current_stage:
            if any(debater['full_name'] == turn['speaker'] for debater in debate_config.get('debaters',[])):
                 stage_indicator = "开篇立论"

        if stage_indicator and stage_indicator != current_stage:
            current_stage = stage_indicator
            icon = stage_icons.get(current_stage, "📄")
            html += f'<div class="stage"><span class="icon">{icon}</span>{current_stage}</div>\n'

        if turn_type == "speech":
            # --- Icon logic remains the same, using original speaker name from turn['speaker'] ---
            speaker_icon = "🧑‍⚖️" # Default judge
            if debate_config and 'debaters' in debate_config:
                pro_team_debaters = debate_config['debaters'].get('pro', [])
                con_team_debaters = debate_config['debaters'].get('con', [])

                # 检查发言者是否为 'pro' 队的第一位辩手
                if pro_team_debaters and turn['speaker'] == pro_team_debaters[0]['full_name']:
                    speaker_icon = "💡"  # 'pro' 队第一位辩手的图标
                # 否则，检查发言者是否为 'con' 队的第一位辩手
                elif con_team_debaters and turn['speaker'] == con_team_debaters[0]['full_name']:
                    speaker_icon = "🚀"  # 'con' 队第一位辩手的图标
            
            # 如果发言者是裁判，确保设置裁判图标（这会覆盖之前的辩手图标）
            if debate_config and 'judge' in debate_config and turn['speaker'] == debate_config['judge']['full_name']:
                 speaker_icon = "🧑‍⚖️"

            # 使用处理过的 speaker 和 text_html
            html += f"""
    <div class="turn">
        <span class="speaker"><span class="icon">{speaker_icon}</span>{speaker}:</span>
        <div class="text">{text_html}</div>
    </div>
"""
    html += """
    </div> <!-- 结束容器 -->
</body>
</html>
    """
    # 确保在函数末尾返回 html 字符串
    return html


def generate_roundtable_html_content(topic, history, config):
    participants_html = "<ul>"
    for p_idx, p_config in enumerate(config.get("participants", [])):
        participants_html += f"<li><b>角色 {p_idx + 1}: {p_config.get('name', '未知角色')}</b> ({p_config.get('stance', '未定义立场')}) - {'用户扮演' if p_config.get('type') == 'user' else 'AI驱动'}</li>"
    participants_html += "</ul>"

    history_html = ""
    current_round = 0
    for entry in history:
        if entry.get("round") != current_round:
            current_round = entry.get("round")
            history_html += f"<h3>第 {current_round} 轮讨论</h3>"
        
        speaker = entry.get('speaker', '未知发言者')
        # stance = entry.get('stance', '') # 立场信息已在参与者列表中显示
        role_type = entry.get('role_type', '')
        content = entry.get('content', '').replace('\n', '<br>') # 替换换行符以便HTML正确显示

        history_html += f"""
        <div class="history-entry">
            <p><strong>{speaker} ({'用户' if role_type == 'user' else 'AI'}):</strong></p>
            <p>{content}</p>
        </div>
        """

    html_output = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>圆桌讨论记录: {topic}</title>
    <style>
        body {{ font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f4f7f6; color: #333; line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 30px auto; padding: 25px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 15px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }}
        h2 {{ color: #3498db; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px;}}
        h3 {{ color: #2980b9; margin-top: 25px; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ background-color: #ecf0f1; margin-bottom: 8px; padding: 10px; border-radius: 4px; border-left: 4px solid #3498db; }}
        li b {{ color: #2c3e50; }}
        .history-entry {{ 
            margin-bottom: 20px; 
            padding: 15px; 
            border: 1px solid #e0e0e0; 
            border-left: 5px solid #1abc9c; /* AI发言用一种颜色 */
            background-color: #ffffff; 
            border-radius: 5px; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .history-entry.user-entry {{
            border-left-color: #f39c12; /* 用户发言用另一种颜色 */
        }}
        .history-entry strong {{ 
            display: block; 
            margin-bottom: 8px; 
            color: #2c3e50; 
            font-weight: 600;
        }}
        .history-entry p:last-child {{ margin-bottom: 0; }}
        footer {{ text-align: center; margin-top: 30px; font-size: 0.9em; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>圆桌讨论主题: {topic}</h1>

        <h2>参与者及核心观点</h2>
        {participants_html}

        <h2>讨论记录</h2>
        {history_html}
        
        <footer>
            <p>AI 智能交互系统 - 圆桌讨论记录</p>
        </footer>
    </div>
</body>
</html>
    """
    return html_output