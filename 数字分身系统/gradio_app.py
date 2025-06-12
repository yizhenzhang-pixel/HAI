
import gradio as gr
import asyncio
from ai_talk_agent.model_api import ask_model
from ai_talk_agent.tts_minimax import speak_text
from ai_talk_agent.stt_whisper import record_audio, transcribe_audio

# 异步封装为同步执行器（用于 Gradio）
def chat_with_ai(user_input, mode):
    if mode == "🎙️ 语音输入":
        audio, fs = record_audio(duration=5)
        user_input = transcribe_audio(audio, fs)
    if not user_input.strip():
        return "", ""
    reply = ask_model(user_input)
    # 调用异步语音播放（非阻塞）
    asyncio.run(speak_text(reply))
    return reply, user_input

with gr.Blocks() as demo:
    gr.Markdown("## 爷爷的故事")

    mode = gr.Radio(["⌨️ 文字输入", "🎙️ 语音输入"], value="⌨️ 文字输入", label="输入方式")
    user_input = gr.Textbox(label="你想说的话", placeholder="输入内容或点击语音模式")
    submit_btn = gr.Button("发送")

    with gr.Row():
        reply_text = gr.Textbox(label="AI 回复", lines=4)
        input_display = gr.Textbox(label="识别后用户输入", lines=1)

    submit_btn.click(fn=chat_with_ai, inputs=[user_input, mode], outputs=[reply_text, input_display])

demo.launch(share=True)