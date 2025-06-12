# ai_talk_agent/image_task.py

import asyncio
from .image_generation import generate_image
from .image_utils import download_image, open_image

async def handle_image_generation(prompt: str):
    """
    异步处理图像生成任务：生成图像、下载、并打开。
    """
    print("🖼️ 正在后台生成图像，请稍候...")
    try:
        image_url = await generate_image(prompt)
        if image_url:
            image_path = download_image(image_url)
            if image_path:
                open_image(image_path)
            else:
                print("⚠️ 图像下载失败")
        else:
            print("⚠️ 图像生成失败")
    except Exception as e:
        print(f"❌ 图像任务异常：{e}")