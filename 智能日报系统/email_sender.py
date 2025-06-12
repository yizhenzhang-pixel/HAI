import yagmail

def send_email_with_report(html_file, to_email="your_receiver@example.com"):
    sender_email = "your_email@example.com"
    yag = yagmail.SMTP(user=sender_email, password="你的授权码")

    subject = "📩 每日智能热榜日报"
    contents = [
        "你好，这是今天的日报，见附件或内嵌HTML内容。",
        yagmail.inline(html_file),
    ]

    yag.send(to=to_email, subject=subject, contents=contents)
    print(f"✅ 已成功发送日报到：{to_email}")