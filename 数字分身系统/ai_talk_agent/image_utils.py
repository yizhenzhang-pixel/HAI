import requests
import os
import platform
import subprocess

def download_image(image_url: str, save_dir: str = "images", filename: str = None) -> str | None:
    os.makedirs(save_dir, exist_ok=True)
    if not filename:
        filename = image_url.split("/")[-1].split("?")[0]
    save_path = os.path.join(save_dir, filename)

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"✅ 图像已保存：{save_path}")
            return save_path
        else:
            print(f"❌ 下载失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 下载异常：{e}")
        return None

def open_image(image_path: str):
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.run(["open", image_path])
        elif system == "Windows":
            os.startfile(image_path)
        elif system == "Linux":
            subprocess.run(["xdg-open", image_path])
        else:
            print("⚠️ 当前系统不支持自动打开图片")
        print(f"🖼️ 已尝试打开图片：{image_path}")
    except Exception as e:
        print(f"❌ 打开图片失败：{e}")