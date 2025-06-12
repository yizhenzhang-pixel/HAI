# 数字分身系统（Digital Avatar System）

> 综合语音识别、语音合成和数字人生成的示例项目，演示如何与虚拟形象进行自然对话。

---

## 📌 项目简介

数字分身系统通过调用大语言模型生成回复，并结合 TTS、STT 与 D-ID 等接口，将文字转为语音和视频，实现与“爷爷”形象的互动。可通过命令行或 Gradio Web 页面体验。

---

## 💡 核心功能

- 支持键盘输入和 5 秒语音输入两种模式
- 利用硅基流动 API 获取模型回复（可在 `ai_talk_agent/config.py` 中配置）
- 使用 MiniMax WebSocket 接口合成语音并自动播放
- 通过 D-ID API 将语音和头像合成数字人视频，下载至 `videos/` 目录
- 提供基于 Gradio 的简单交互界面（`gradio_app.py`、`gradio_app_ui.py`）

---

## 🗂️ 目录结构

```
数字分身系统/
├── main.py                # 命令行主程序
├── gradio_app.py          # 简易 Web 版（可分享）
├── gradio_app_ui.py       # 美化后的 Web 版
├── ai_talk_agent/         # 功能模块
│   ├── config.py          # API Key 与模型参数
│   ├── model_api.py       # 调用语言模型
│   ├── tts_minimax.py     # 文本转语音
│   ├── stt_whisper.py     # 语音转文本
│   ├── did_video.py       # 生成数字人视频
│   ├── image_generation.py# 图像生成（辅助）
│   ├── image_task.py      # 图像生成任务封装
│   └── image_utils.py     # 图像下载与打开
└── videos/                # 视频输出目录
```

---

## 🚀 快速开始

1. **安装依赖**  
   需准备 Python 3.9+，安装常用库：  
   ```bash
   pip install requests websockets pydub sounddevice gradio
   ```

2. **配置 API Key**  
   在 `ai_talk_agent/config.py` 填入硅基流动、MiniMax 等所需密钥；`did_video.py` 中也需替换 D-ID API Key。

3. **运行命令行版本**  
   ```bash
   cd 数字分身系统
   python main.py
   ```  
   按提示输入文字，或在输入 `v` 后说话实现语音输入。

4. **启动 Gradio Web 界面**  
   ```bash
   python gradio_app.py       # 或 python gradio_app_ui.py
   ```  
   打开终端给出的地址即可在浏览器体验。

---

## 📜 License

本项目示例代码遵循 MIT License，更多说明见仓库根目录的 README。
