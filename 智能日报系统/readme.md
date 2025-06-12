# 智能日报系统（Smart Daily Report System）

> 从多个新闻站点抓取热点，结合 AI 模型生成摘要，自动输出可视化日报并邮件发送。

---

## 📌 项目简介

本系统提供一套半自动化流程：依据主题关键词爬取中英新闻网站，利用大语言模型提炼摘要，生成带有词云的 Markdown/HTML 报告，并可通过邮箱分发或 FastAPI 接口使用。适合个人或团队了解每日资讯动态。

---

## 💡 核心功能

- 按关键词抓取国内外新闻（`fetcher.py`）
- 调用 DeepSeek 等模型生成 300~500 字导览摘要（`summarizer.py`）
- 生成带词云的 Markdown/HTML 报告（`reporter.py`）
- 通过 Yagmail 发送日报邮件（`email_sender.py` 或 `main.py` 内置）
- 提供 FastAPI 服务端，可由前端调用（`app.py`）
- `python-crontab.py` 示例定时脚本，支持每日自动执行

---

## 🗂️ 目录结构

```
智能日报系统/
├── main.py            # 终端版入口
├── fetcher.py         # 新闻抓取逻辑
├── summarizer.py      # AI 摘要生成
├── reporter.py        # Markdown/HTML 输出
├── email_sender.py    # 简化的邮件发送
├── app.py             # FastAPI 服务端示例
├── theme_map.py       # 主题与函数映射
├── python-crontab.py  # cron 定时示例
└── reports/           # 日报输出目录（运行后生成）
```

---

## 🚀 快速开始

1. **安装依赖**
   建议 Python 3.9+，安装库：`pip install requests newspaper3k markdown2 wordcloud yagmail fastapi uvicorn`

2. **配置密钥与邮箱**
   在脚本中填入新闻 API、AI 模型和邮箱的密钥或授权码。

3. **运行终端版**

   ```bash
   cd 智能日报系统
   python main.py
   ```
   根据提示输入主题关键词，可自动打开生成的 HTML 报告并发送邮件。

4. **启动 Web 服务（可选）**

   ```bash
   python app.py
   ```
   访问 `http://127.0.0.1:8000` 调用接口生成日报。

5. **定时任务（可选）**
   配置 `python-crontab.py`，即可在每天固定时间自动发送日报。

---

## 📜 License

代码遵循 MIT License，详见仓库根目录。
