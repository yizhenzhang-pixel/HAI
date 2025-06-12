import asyncio
import websockets
import json
import ssl
from io import BytesIO
from pydub import AudioSegment
import datetime
import subprocess

from .config import MINIMAX_API_KEY, T2A_WS_URL, VOICE_ID, EMOTION

async def speak_text(text):
    """通过 MiniMax WebSocket 合成语音并保存为 mp3，同时返回音频路径"""

    async def establish_connection():
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}"
        }

        ws = await websockets.connect(
            T2A_WS_URL,
            ssl=ssl_context,
            extra_headers=headers
        )

        res = json.loads(await ws.recv())
        if res.get("event") == "connected_success":
            return ws
        return None

    async def start_task(ws):
        start_msg = {
            "event": "task_start",
            "model": "speech-02-hd",
            "voice_setting": {
                "voice_id": VOICE_ID,
                "speed": 1,
                "vol": 1,
                "pitch": 0,
                "emotion": EMOTION
            },
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
                "channel": 1
            }
        }
        await ws.send(json.dumps(start_msg))
        res = json.loads(await ws.recv())
        return res.get("event") == "task_started"

    async def continue_task(ws):
        await ws.send(json.dumps({
            "event": "task_continue",
            "text": text
        }))

        audio_chunks = []
        while True:
            response = json.loads(await ws.recv())
            if "data" in response and "audio" in response["data"]:
                audio_chunks.append(response["data"]["audio"])
            if response.get("is_final"):
                break
        return "".join(audio_chunks)

    async def close_connection(ws):
        await ws.send(json.dumps({"event": "task_finish"}))
        await ws.close()

    # === 主流程 ===
    ws = await establish_connection()
    if not ws:
        print("❌ MiniMax 连接失败")
        return None

    try:
        if not await start_task(ws):
            print("❌ 启动任务失败")
            return None

        hex_audio = await continue_task(ws)
        audio_bytes = bytes.fromhex(hex_audio)

        try:
            audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_reply_{timestamp}.mp3"
            audio.export(filename, format="mp3")

            # ✅ 播放
            subprocess.run(["afplay", filename])

            # ✅ 返回路径
            return filename

        except Exception as e:
            print("❌ 语音保存或播放失败：", e)
            return None

    finally:
        await close_connection(ws)