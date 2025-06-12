import requests

# AI摘要接口配置
DEEPSEEK_API_KEY = "sk-pfkropedfcqdxvelnszzcqhceozpmlsodqiqsfdedcbeurpw"
DEEPSEEK_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

def generate_summary(article_list, use_ai=True):
    # 适配两种结构：dict（旧）或 list（新）
    if isinstance(article_list, dict):
        all_titles = []
        for items in article_list.values():
            if items:
                all_titles.extend(title for title, url in items if title)
    else:
        all_titles = [item["title"] for item in article_list if item.get("title")]

    if not all_titles:
        return "⚠️ 今日暂无热点内容。"

    merged_text = "\n".join(all_titles)

    if not use_ai:
        # 简易模式：本地标题拼接
        intro = f"今日共收录{len(all_titles)}条新闻标题，以下是部分重点：\n\n"
        for i, title in enumerate(all_titles[:5]):
            intro += f"{i+1}. {title}\n"
        intro += "\n（详情请参见后文）"
        return intro

    # AI 智能摘要
    prompt = f"""
你是一个新闻导览生成器。

以下是今天的新闻标题，请你总结出一段优雅、简洁、流畅的导览文字。
不要逐条复述标题，而是综合观察趋势、领域动态、共同焦点。
长度在300到500字之间，语言具有人文气息与新闻判断力。

标题列表：
{merged_text}
"""

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
        response = requests.post(DEEPSEEK_BASE_URL, headers=headers, json=payload, timeout=80)
        result = response.json()
        summary_text = result["choices"][0]["message"]["content"]
        return summary_text.strip()
    except Exception as e:
        print(f"⚠️ 智能摘要失败，原因：{e}")
        # 回退逻辑
        intro = f"今日共收录{len(all_titles)}条新闻（AI总结失败，以下为部分标题）：\n\n"
        for i, title in enumerate(all_titles[:5]):
            intro += f"{i+1}. {title}\n"
        return intro.strip()