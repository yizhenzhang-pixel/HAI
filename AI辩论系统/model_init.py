import os
import google.generativeai as genai
from utils import console

AVAILABLE_MODELS = {
    "1": "gemini-1.5-flash",
    "2": "gemini-1.5-pro-vision",
    "3": "gemini-2.5-pro-preview-05-06"
}

def select_model():
    console.print("\n[bold cyan]请选择要使用的 Gemini 模型版本：[/bold cyan]")
    for key, name in AVAILABLE_MODELS.items():
        console.print(f"  [yellow]{key}[/yellow]: {name}")
    
    choice = input("请输入模型序号（默认 3）：").strip()
    return AVAILABLE_MODELS.get(choice, "gemini-2.5-pro-preview-05-06")

def init_model(model_name=None):
    """
    初始化 Gemini 模型，支持手动或交互选择模型版本。
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print("[red]❌ 未设置 GOOGLE_API_KEY 环境变量。[/red]")
        exit()

    genai.configure(api_key=api_key)

    if not model_name:
        model_name = select_model()

    try:
        model = genai.GenerativeModel(model_name)
        model.generate_content(
            "test",
            generation_config=genai.types.GenerationConfig(max_output_tokens=5)
        )
        console.print(f"[green]✅ 模型初始化成功: {model_name}[/green]")
        return model
    except Exception as e:
        console.print(f"[red]❌ 模型初始化失败: {e}[/red]")
        exit()