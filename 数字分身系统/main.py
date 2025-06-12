import asyncio
from ai_talk_agent.model_api import ask_model
from ai_talk_agent.tts_minimax import speak_text
from ai_talk_agent.stt_whisper import record_audio, transcribe_audio
from ai_talk_agent.did_video import generate_did_video

async def main():
    print("🤖 聊聊爷爷年轻时的故事（文字输入 / 语音输入）")
    print("🎤 输入指令 `v` 开启语音输入，对话时输入 `e` 退出")

    while True:
        user_input = input("你：").strip()

        if user_input.lower() == "e":
            print("👋 再见！")
            break

        # 🎙️ 启用语音输入模式
        if user_input.lower() == "v":
            print("🎤 录音中（5 秒）...")
            audio, fs = record_audio(duration=5)
            user_input = transcribe_audio(audio, fs)
            print(f"📝 你说的是：{user_input}")

        # 🧠 调用模型生成回应
        reply = ask_model(user_input)
        print("爷爷：", reply)

        try:
            # 🗣️ 合成语音并播放，同时保存为音频文件
            audio_path = await speak_text(reply)

            # 🎬 调用 D-ID API 生成视频（异步线程方式）
            await asyncio.to_thread(generate_did_video, audio_path)

        except Exception as e:
            print(f"⚠️ 语音合成或视频生成失败：{e}")

if __name__ == "__main__":
    asyncio.run(main())