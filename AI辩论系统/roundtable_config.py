from utils import console

def get_roundtable_configuration():
    config = {}
    console.print("\n[bold cyan]=== 圆桌讨论配置 ===[/bold cyan]")
    config["topic"] = console.input("请输入圆桌讨论的主题: ")

    while True:
        try:
            num_participants = int(console.input("请输入参与角色的总数量 (至少2个): "))
            if num_participants >= 2:
                break
            else:
                console.print("[bold red]参与角色数量至少为2。[/bold red]")
        except ValueError:
            console.print("[bold red]请输入有效的数字。[/bold red]")
    
    config["participants"] = []
    user_participant_index = -1 # -1 表示用户不参与

    console.print("\n[bold cyan]--- 用户参与设置 ---[/bold cyan]")
    user_participates_choice = console.input("您是否想亲自扮演其中一个角色参与讨论? (yes/no): ").strip().lower()
    
    if user_participates_choice == 'yes':
        while True:
            try:
                user_role_number = int(console.input(f"您想扮演第几个角色? (1-{num_participants}): "))
                if 1 <= user_role_number <= num_participants:
                    user_participant_index = user_role_number - 1 # 0-indexed
                    break
                else:
                    console.print(f"[bold red]请输入1到{num_participants}之间的数字。[/bold red]")
            except ValueError:
                console.print("[bold red]请输入有效的数字。[/bold red]")

    console.print("\n[bold cyan]--- 角色详细设置 ---[/bold cyan]")
    for i in range(num_participants):
        console.print(f"\n--- 配置角色 {i+1} ---")
        participant_name = console.input(f"角色 {i+1} 的名称 (例如：技术乐观主义者): ").strip()
        
        if i == user_participant_index:
            # 对于用户扮演的角色，立场可以由用户在讨论时自行把握，这里记录为用户控制
            participant_stance = "由用户在讨论中自行把握立场"
            participant_type = "user"
            console.print(f"[italic green]角色 {i+1} ({participant_name}) 将由您扮演。[/italic green]")
        else:
            participant_stance = console.input(f"角色 {i+1} ({participant_name}) 的主要立场/观点: ").strip()
            participant_type = "ai"

        config["participants"].append({
            "name": participant_name,
            "stance": participant_stance,
            "type": participant_type # 'ai' or 'user'
        })

    while True:
        try:
            config["rounds"] = int(console.input("\n请输入讨论进行的轮数 (例如：3轮，每轮每个角色发言一次): "))
            if config["rounds"] > 0:
                break
            else:
                console.print("[bold red]轮数必须大于0。[/bold red]")
        except ValueError:
            console.print("[bold red]请输入有效的数字。[/bold red]")
            
    return config