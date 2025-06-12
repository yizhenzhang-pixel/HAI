
import markdown2
import datetime
import os
import base64
import requests
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

DEEPSEEK_API_KEY = "sk-pfkropedfcqdxvelnszzcqhceozpmlsodqiqsfdedcbeurpw"
DEEPSEEK_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

def generate_summary_text(results):
    titles = [item["title"] for item in results if item.get("title")]
    if not titles:
        return "⚠️ 今日暂无新闻内容可用。"

    prompt = "以下是今天的新闻标题，请写一段优雅、通俗的导览摘要（300-500字）：\n" + "\n".join(titles)
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {"role": "system", "content": "你是一个优秀的中文新闻导览写手。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    try:
        response = requests.post(DEEPSEEK_BASE_URL, headers=headers, json=payload, timeout=60)
        return response.json()["choices"][0]["message"]["content"].strip()
    except:
        return "⚠️ 智能摘要生成失败，请稍后再试。"

def generate_wordcloud(results, save_path):
    full_text = " ".join([item.get("text", "") for item in results if item.get("text")])
    words = list(jieba.cut(full_text))
    stopwords = set(["的", "是", "在", "了", "和", "也", "与", "就", "都", "为", "上", "对", "一个", "我们", "这", "进行"])
    words = [w for w in words if w not in stopwords and len(w) > 1]
    freq = Counter(words)
    wordcloud = WordCloud(
        font_path="/System/Library/Fonts/STHeiti Medium.ttc",
        background_color="white",
        width=800,
        height=400
    ).generate_from_frequencies(freq)
    wordcloud.to_file(save_path)

def generate_base64_image(img_path):
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{encoded}" alt="词云图" style="max-width:100%; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.1);" />'

def save_to_markdown(summary_text, results, theme="AI"):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join("reports", today)
    os.makedirs(folder, exist_ok=True)

    md_path = os.path.join(folder, f"{theme}日报.md")
    html_path = os.path.join(folder, f"{theme}日报.html")
    wordcloud_path = os.path.join(folder, "词云图.png")

    generate_wordcloud(results, wordcloud_path)
    img_tag = generate_base64_image(wordcloud_path)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 📈 {today} 智能日报（{theme}主题）\n\n")
        f.write(f"## 🧭 总览摘要\n\n> {summary_text.strip()}\n\n")
        f.write("## ☁️ 热词词云\n\n<!--WORDCLOUD_PLACEHOLDER-->")
        f.write("## 📰 新闻列表\n\n")
        for i, item in enumerate(results, 1):
            f.write(f"{i}. [{item.get('title')}]({item.get('url')})\n")

    convert_markdown_to_html(md_path, html_path, img_tag)
    return md_path, html_path

def convert_markdown_to_html(md_path, html_path, img_tag):
    html_content = markdown2.markdown_path(md_path, extras=["fenced-code-blocks", "toc"])
    html_content = html_content.replace("<!--WORDCLOUD_PLACEHOLDER-->", f'<div class="wordcloud-container">{img_tag}</div>')
    page = f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>智能日报</title>
  <style>
    body {{
      font-family: "Helvetica Neue", sans-serif;
      background: #f4f6f8;
      padding: 30px 0;
      margin: 0;
    }}
    .container {{
      background: white;
      max-width: 720px;
      margin: auto;
      padding: 32px;
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.05);
    }}
    h1, h2, h3 {{
      color: #111;
      padding-bottom: 6px;
      border-bottom: 1px solid #eaecef;
    }}
    a {{
      color: #0366d6;
      text-decoration: none;
    }}
    blockquote {{
      background: #f1f3f5;
      padding: 12px 18px;
      margin: 12px 0;
      border-left: 4px solid #91a7ff;
      color: #444;
      border-radius: 8px;
    }}
    ul {{
      list-style: none;
      padding-left: 0;
    }}
    ul li::before {{
      content: "📌 ";
    }}
    .wordcloud-container {{
      margin: 20px auto;
      text-align: center;
      background: #eef2f7;
      padding: 20px;
      border-radius: 10px;
    }}
  </style>
</head>
<body>
  <div class="container">
    {html_content}
  </div>
</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(page)

def convert_markdown_to_email_html(md_path):
    html_text = markdown2.markdown_path(md_path)
    return f"<div style='font-family: Helvetica, sans-serif;'>{html_text}</div>"
