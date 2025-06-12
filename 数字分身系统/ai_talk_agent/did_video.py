import requests
import base64
import time
import subprocess
import os

DID_API_KEY = "YTM2MzcyMTkwN0BnbWFpbC5jb20:Yg1GH9m8lOYHE8ig-biVQ"
API_KEY = base64.b64encode(f"{DID_API_KEY}:".encode()).decode()
HEADERS = {"Authorization": f"Basic {API_KEY}"}

IMAGE_PATH = "/Users/wooton/PycharmProjects/PythonProject2/ai_talk_agent_package/grandpa.png"  # 固定头像
DOWNLOAD_DIR = "videos"  # 下载目录

def upload_image():
    with open(IMAGE_PATH, "rb") as img_file:
        res = requests.post("https://api.d-id.com/images", headers=HEADERS, files={"image": img_file})
        res.raise_for_status()
        return res.json()["url"]

def upload_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        res = requests.post("https://api.d-id.com/audios", headers=HEADERS, files={"audio": audio_file})
        res.raise_for_status()
        return res.json()["url"]

def create_video(image_url, audio_url):
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

def wait_for_video(video_id):
    while True:
        res = requests.get(f"https://api.d-id.com/talks/{video_id}", headers=HEADERS)
        res.raise_for_status()
        status = res.json()["status"]
        if status == "done":
            return res.json()["result_url"]
        elif status == "error":
            return None
        print("⏳ 正在生成视频...")
        time.sleep(30)

def download_video(video_url, filename):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    save_path = os.path.join(DOWNLOAD_DIR, filename)
    with requests.get(video_url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return save_path

def open_video(filepath):
    try:
        if os.name == "posix":
            # macOS 强制调用 VLC 播放并自动退出
            subprocess.run(["/Applications/VLC.app/Contents/MacOS/VLC", "--play-and-exit", filepath])
        elif os.name == "nt":
            os.startfile(filepath)
        else:
            print(f"请手动打开：{filepath}")
    except Exception as e:
        print("❌ 无法自动播放视频：", e)

def generate_did_video(audio_path):
    print("🎬 正在生成数字人视频（D-ID）...")
    image_url = upload_image()
    audio_url = upload_audio(audio_path)
    video_id = create_video(image_url, audio_url)
    video_url = wait_for_video(video_id)

    if video_url:
        print(f"✅ 视频生成成功：{video_url}")
        filename = f"talk_{int(time.time())}.mp4"
        local_path = download_video(video_url, filename)
        print(f"📥 已下载到本地：{local_path}")
        open_video(local_path)
    else:
        print("❌ 视频生成失败")