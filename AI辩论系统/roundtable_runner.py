from utils import console
# 假设您的模型交互逻辑封装在 model.generate() 或类似方法中
# 例如: from model_init import YourModelClass (如果模型有特定方法)

def run_roundtable_discussion(config, model):
    history = []
    topic = config["topic"]
    participants = config["participants"]
    num_rounds = config["rounds"]

    console.print(f"\n[bold blue]圆桌讨论开始！主题：{topic}[/bold blue]")
    console.print(f"参与者:")
    for p_idx, p in enumerate(participants):
        console.print(f"- 角色 {p_idx+1}: {p['name']} (核心观点: {p['stance']}) [{'用户扮演' if p['type'] == 'user' else 'AI驱动'}]")

    current_discussion_text = f"讨论主题: {topic}\n"
    if len(participants) > 0:
        current_discussion_text += "参与者及其核心观点:\n"
        for p_idx, p in enumerate(participants):
            current_discussion_text += f"- {p['name']}: {p['stance']}\n"
    current_discussion_text += "\n讨论记录:\n"


    for round_num in range(1, num_rounds + 1):
        console.print(f"\n[bold yellow]--- 第 {round_num} 轮讨论 ---[/bold yellow]")
        for participant_index, participant in enumerate(participants):
            participant_name = participant["name"]
            participant_stance = participant["stance"]
            participant_type = participant["type"]

            console.print(f"\n轮到 [bold cyan]{participant_name}[/bold cyan] 发言...")

            if participant_type == "user":
                user_input = console.input(f"请输入您的发言 ({participant_name}): ").strip()
                statement = user_input
            else: # AI participant
                # 构建更丰富的上下文给AI
                prompt_context = f"你正在参与一场关于“{topic}”的圆桌讨论。\n"
                prompt_context += f"你的角色是“{participant_name}”，你的核心观点是“{participant_stance}”。\n"
                prompt_context += "其他参与者及观点:\n"
                for p_idx, p_other in enumerate(participants):
                    if p_idx != participant_index: # 不显示当前AI自己的信息在“其他参与者”部分
                        prompt_context += f"- {p_other['name']}: {p_other['stance']}\n"
                
                prompt_context += f"\n到目前为止的讨论内容如下：\n{current_discussion_text}\n---\n"
                prompt_context += f"现在轮到你 ({participant_name}) 发言。请严格基于你的角色和核心观点，对当前讨论的内容进行回应、补充、提出新的见解或问题。请直接陈述你的发言内容，不要包含角色扮演的额外说明 (例如不要说 '作为xx，我认为...')。\n你的发言："
                
                # 实际调用模型生成回应
                console.print("[italic gray](AI 正在思考...)[/italic gray]")
                # 确保 model 对象有正确的方法，并且能正确处理 prompt
                # 尝试使用 generate_content，并获取 .text 属性
                try:
                    response = model.generate_content(prompt_context)
                    statement = response.text
                except AttributeError:
                    # 如果直接 .text 失败，尝试不加 .text (某些库可能直接返回字符串)
                    # 或者您需要根据您所用库的文档调整此处
                    console.print("[bold red]警告: model.generate_content(prompt_context).text 失败，尝试直接获取响应。请检查模型API文档。[/bold red]")
                    statement = model.generate_content(prompt_context) # 再次尝试，或者根据API调整
                except Exception as e:
                    console.print(f"[bold red]模型调用时发生错误: {e}[/bold red]")
                    statement = f"模型调用失败: {e}"


            console.print(f"[bold magenta]{participant_name}:[/bold magenta] {statement}")
            
            history_entry = {
                "speaker": participant_name,
                "stance": participant_stance, 
                "role_type": participant_type, # 'ai' or 'user'
                "content": statement,
                "round": round_num
            }
            history.append(history_entry)
            current_discussion_text += f"{participant_name}: {statement}\n" # 更新讨论上下文
            
    return history