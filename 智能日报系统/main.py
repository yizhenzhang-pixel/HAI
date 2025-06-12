import os
import webbrowser
import yagmail
from fetcher import fetch_by_theme
from summarizer import generate_summary
from reporter import save_to_markdown, convert_markdown_to_email_html

def send_email_with_report(html_file, to_email):
    sender_email = "a363721907@gmail.com"
    sender_password = "mluc irlq akvp uszz"  # ⚠️ 注意保护隐私

    yag = yagmail.SMTP(user=sender_email, password=sender_password)

    subject = "📩 每日智能日报"
    contents = [
        "你好，这是今天的日报，见附件。",
        html_file
    ]

    yag.send(
        to=to_email,
        subject=subject,
        contents=contents
    )
    print(f"✅ 已成功将日报作为附件发送至：{to_email}")

def main():
    try:
        selected_theme = input("请输入要抓取的主题（可输入多个关键词，如 AI 教育 金融 ）：").strip()
        if not selected_theme:
            selected_theme = "科技"
    except EOFError:
        selected_theme = "科技"

    print(f"开始抓取主题：{selected_theme}")
    keyword_list = selected_theme.split()

    print("⏳ 开始抓取新闻...")
    results = fetch_by_theme(keyword_list)
    print(f"✅ 抓取完成，获取文章数：{len(results)}")

    if not results:
        print("⚠️ 未抓到任何符合条件的新闻，请尝试其他关键词。")
        return

    print("⏳ 开始生成摘要...")
    summary_text = generate_summary(results)
    print("✅ 摘要生成完成")

    md_file, html_file = save_to_markdown(summary_text, results, theme=selected_theme)

    print("📤 正在发送邮件...")
    send_email_with_report(
        html_file,
        to_email=[
            "363721907@qq.com",
            "a363721907@gmail.com",
        ]
    )

    webbrowser.open("file://" + os.path.abspath(html_file))
    print(f"✅ 已打开日报网页：{html_file}")

if __name__ == "__main__":
    main()