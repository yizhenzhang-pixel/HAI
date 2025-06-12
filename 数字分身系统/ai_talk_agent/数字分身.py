import requests
import time

# ✅ 请替换为你的 D-ID API Key
API_KEY = "YTM2MzcyMTkwN0BnbWFpbC5jb20:Yg1GH9m8lOYHE8ig-biVQ"
HEADERS = {
    "Authorization": f"Basic {API_KEY}"
}

# ✅ Step 1: 上传本地图片，获取 image_url
def upload_image(image_path):
    with open(image_path, "rb") as img_file:
        files = {"image": img_file}
        res = requests.post("https://api.d-id.com/images", headers=HEADERS, files=files)
        res.raise_for_status()
        return res.json()["url"]

# ✅ Step 2: 上传本地音频，获取 audio_url
def upload_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        files = {"audio": audio_file}
        res = requests.post("https://api.d-id.com/audios", headers=HEADERS, files=files)
        res.raise_for_status()
        return res.json()["url"]

# ✅ Step 3: 创建视频任务
def create_talking_video(image_url, audio_url):
    payload = {
        "source_url": image_url,
        "script": {
            "type": "audio",
            "audio_url": audio_url
        }
    }
    res = requests.post("https://api.d-id.com/talks", headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json()["id"]

# ✅ Step 4: 轮询获取结果
def wait_for_video(video_id):
    status_url = f"https://api.d-id.com/talks/{video_id}"
    while True:
        res = requests.get(status_url, headers=HEADERS)
        res.raise_for_status()
        status = res.json()["status"]
        if status == "done":
            return res.json()["result_url"]
        elif status == "error":
            raise Exception("视频生成失败")
        else:
            print("⏳ 正在生成视频中...请稍候")
            time.sleep(3)

# ✅ 主函数（只需改文件路径）
if __name__ == "__main__":
    image_path = "/Users/wooton/PycharmProjects/PythonProject2/ai_talk_agent_package/grandpa.png"
    audio_path = "/Users/wooton/PycharmProjects/PythonProject2/ai_talk_agent_package/grandpa.mp3"

    print("📤 上传头像图片...")
    image_url = upload_image(image_path)

    print("📤 上传语音音频...")
    audio_url = upload_audio(audio_path)

    print("🎬 创建视频任务...")
    video_id = create_talking_video(image_url, audio_url)

    print("⏱️ 等待视频生成...")
    result_url = wait_for_video(video_id)

    print(f"✅ 视频生成成功！点击观看：{result_url}")