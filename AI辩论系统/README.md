
# AI辩论系统（AI Debate System）

> 一个基于 Python 脚本运行的智能辩论生成系统，支持模拟辩论与圆桌讨论两种模式，调用大语言模型自动生成多轮发言，并导出结构化 HTML 报告。

---

## 📌 项目简介

AI辩论系统通过多角色配置与模型交互，实现自动化的观点碰撞过程。你只需预设辩题与角色，即可自动生成完整的辩论流程、内容记录与美化输出，适用于：

- 模拟AI间的批判性思维对话  
- 教育场景中展示语言模型如何生成推理与反驳  
- 个人使用者快速生成结构化讨论文本

---

## 💡 核心功能

- 支持“正式辩论”和“圆桌讨论”两种发言机制  
- 可自定义轮数、角色身份、模型调用结构  
- 自动生成发言并导出 HTML 格式可视化页面  
- 支持 Gemini 等模型切换，接口集中管理  

---

## 🗂️ 目录结构

```
AI辩论系统/
├── main.py                 # 主程序入口，支持命令行交互
├── config.py               # 辩题配置（辩论模式）
├── roundtable_config.py    # 辩题配置（圆桌模式）
├── debate_runner.py        # 控制正式辩论流程
├── roundtable_runner.py    # 控制圆桌讨论流程
├── ai_response.py          # 模型回复函数
├── model_init.py           # 模型加载与接口配置
├── export.py               # 输出 HTML 文件
├── html_template.py        # HTML 模板封装
├── utils.py                # 辅助工具函数
└── output/                 # 自动生成的输出文件目录（需自行创建）
```

---

## 🚀 使用说明

### 1. 安装依赖

建议创建虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install openai google-generativeai
```

如需使用 Gemini，请配置你的 API Key，并在 `model_init.py` 中指定默认模型。

---

### 2. 运行主程序

#### 正式辩论模式：

```bash
python main.py
```

系统将提示选择模式、读取辩题并自动生成辩论内容。


## ✨ 输出样例（HTML 格式）

程序运行结束后，会在当前目录下生成一个 `.html` 文件，内容包括：

- 辩题信息、辩手配置、发言轮次  
- 每轮发言清晰分栏，角色对话可视化  
- 美观、可浏览、可复制的结构化输出页面

---

## 🧩 自定义指南

你可修改以下配置以定制辩论内容：

- `config.py`：辩题、角色、轮次等基础设定  
- `model_init.py`：更换模型（如从 Gemini 切换到 OpenAI）  
- `html_template.py`：修改输出样式或添加关键词高亮规则

---

## 📌 注意事项

- 当前版本不包含前端网页系统，所有功能通过 Python 命令行调用  
- 输出结果为静态 HTML 文件，供后续浏览与展示  
- 模型调用频次较高，请留意 API 限额与计费策略

---

## 📜 License

MIT License
