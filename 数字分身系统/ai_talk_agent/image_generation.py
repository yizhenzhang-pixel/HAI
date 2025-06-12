import json
import requests
from .config import MINIMAX_API_KEY

IMAGE_API_URL = "https://api.minimax.chat/v1/image_generation"

async def generate_image(prompt: str) -> str | None:
    scene_prefix = "中国50-60年代的真实生活场景，黑白胶片风格，"
    full_prompt = scene_prefix + prompt

    payload = json.dumps({
        "model": "image-01",
        "prompt": full_prompt,
        "aspect_ratio": "16:9",
        "response_format": "url",
        "n": 1,
        "prompt_optimizer": True
    })
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(IMAGE_API_URL, headers=headers, data=payload, timeout=60)
        data = response.json()
        print("📩 返回数据：", json.dumps(data, ensure_ascii=False, indent=2))

        # ✅ 正确解析方式
        image_urls = data.get("data", {}).get("image_urls", [])
        if isinstance(image_urls, list) and len(image_urls) > 0:
            return image_urls[0]
        else:
            print("⚠️ 图像生成失败，image_urls 为空")
            return None

    except Exception as e:
        print(f"❌ 图像生成异常：{e}")
        return None