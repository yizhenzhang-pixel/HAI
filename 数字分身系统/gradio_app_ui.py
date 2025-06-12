import gradio as gr
import asyncio
import os

from ai_talk_agent.model_api import ask_model
from ai_talk_agent.tts_minimax import speak_text
from ai_talk_agent.stt_whisper import record_audio, transcribe_audio
from ai_talk_agent.did_video import generate_did_video

def chat_with_ai(user_input, mode):
    if mode == "🎙️ 语音输入":
        audio, fs = record_audio(duration=5)
        user_input = transcribe_audio(audio, fs)
    if not user_input.strip():
        return "", "", None

    reply = ask_model(user_input)

    try:
        audio_path = asyncio.run(speak_text(reply))
        video_path = generate_did_video(audio_path)
        return reply, user_input, video_path
    except Exception as e:
        return reply, user_input, None

with gr.Blocks(css="""
#title {
  font-size: 36px;
  font-weight: bold;
  color: #1E40AF;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}
#section {
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background-color: #f9fafb;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.gr-button {
  background: #2563eb !important;
  color: white !important;
  font-weight: bold;
  border-radius: 8px;
}
""") as demo:

    gr.HTML("<div id='title'>👴 爷爷的故事</div>")

    with gr.Row():
        with gr.Column(elem_id="section"):
            mode = gr.Radio(["⌨️ 文字输入", "🎙️ 语音输入"], value="⌨️ 文字输入", label="输入方式")
            user_input = gr.Textbox(label="你想说的话", placeholder="请输入或启用语音输入", lines=2)
            submit_btn = gr.Button("🚀 发送")

        with gr.Column(elem_id="section"):
            reply_text = gr.Textbox(label="🤖 爷爷的回答", lines=4)
            input_display = gr.Textbox(label="📝 语音识别结果", lines=1)
            video_display = gr.Video(label="🎬 爷爷说话中", interactive=False)

    submit_btn.click(
        fn=chat_with_ai,
        inputs=[user_input, mode],
        outputs=[reply_text, input_display, video_display]
    )

demo.launch()