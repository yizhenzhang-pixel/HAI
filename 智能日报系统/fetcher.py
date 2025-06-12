from newspaper import Article, build
import os

# 中文站点
CHINESE_SITES = {
    "澎湃新闻": "https://www.thepaper.cn",
    "凤凰网": "https://news.ifeng.com",
    "网易新闻": "https://news.163.com",
    "虎嗅": "https://www.huxiu.com",
    "界面新闻": "https://www.jiemian.com",
    "新华网": "https://www.xinhuanet.com",
    "新浪新闻": "https://news.sina.com.cn"
}

# 国际站点
INTERNATIONAL_SITES = {
    "BBC": "https://www.bbc.com",
    "CNN": "https://edition.cnn.com",
    "Reuters": "https://www.reuters.com",
    "TechCrunch": "https://techcrunch.com",
    "The Guardian": "https://www.theguardian.com",
    "The Verge": "https://www.theverge.com",
    "Forbes": "https://www.forbes.com",
    "The New York Times": "https://www.nytimes.com",
    "Bloomberg": "https://www.bloomberg.com",
    "Al Jazeera": "https://www.aljazeera.com",
    "Wired": "https://www.wired.com",
    "Medium": "https://medium.com",
    "Hacker News": "https://news.ycombinator.com",
    "VentureBeat": "https://venturebeat.com",
    "Ars Technica": "https://arstechnica.com"
}

MAX_ARTICLES_PER_SITE = 10
SUMMARY_CHAR_LIMIT = 500

def fetch_by_theme(theme_keywords):
    """
    输入关键词列表（支持中英文），返回筛选后的新闻结构。
    所有关键词都必须同时出现在文章正文中（AND逻辑）。
    返回数据结构为：[{site, title, url, text, publish_date}]
    """
    if isinstance(theme_keywords, str):
        keywords = theme_keywords.strip().split()
    else:
        keywords = theme_keywords

    results = []

    for group in [CHINESE_SITES, INTERNATIONAL_SITES]:
        for site_name, site_url in group.items():
            paper = build(site_url, memoize_articles=False)
            for article in paper.articles[:MAX_ARTICLES_PER_SITE]:
                try:
                    article.download()
                    article.parse()
                    text = article.text.strip().replace('\n', ' ')
                    if all(kw.lower() in text.lower() for kw in keywords):
                        results.append({
                            "site": site_name,
                            "title": article.title,
                            "url": article.url,
                            "text": text[:SUMMARY_CHAR_LIMIT] + "...",
                            "publish_date": str(article.publish_date) if article.publish_date else "N/A"
                        })
                except:
                    continue
    return results
