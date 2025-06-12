import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from matplotlib.font_manager import FontProperties

# === 设置中文字体（请根据你电脑字体路径自行修改） ===
ch_font = FontProperties(fname="/Users/wooton/Library/Fonts/SourceHanSansSC-Regular.otf")

# === Step 1: 读取数据 ===
df = pd.read_excel("聊天分析任务_修正标签_100条.xlsx", parse_dates=["时间戳"])
df["字数"] = df["内容"].astype(str).apply(len)
df["极性"] = df["极性分数（-1~1）"]

# === Step 2: 主动发言统计 ===
talk_count = df["发送者"].value_counts()
talk_length = df.groupby("发送者")["字数"].mean()

print("\n🔢 发言条数：\n", talk_count)
print("\n✏️ 平均发言长度：\n", talk_length)

# === Step 3: 情绪走势图 ===
plt.figure(figsize=(10, 4))
df.set_index("时间戳")["极性"].rolling("10min").mean().plot()
plt.title("情绪走势（滑动窗口10分钟）", fontproperties=ch_font)
plt.ylabel("情绪极性", fontproperties=ch_font)
plt.xticks(fontproperties=ch_font)
plt.yticks(fontproperties=ch_font)
plt.grid(True)
plt.tight_layout()
plt.savefig("情绪走势.png")
print("📈 情绪走势图已生成：情绪走势.png")

# === Step 4: 情绪关键词词云 ===
def gen_wordcloud(df, emotion_class, filename):
    sub_df = df[(df["情绪分类"] == emotion_class) & (df["消息类型"] == "文字")]
    texts = " ".join(sub_df["内容"])
    words = " ".join(jieba.lcut(texts))
    if not words.strip():
        print(f"⚠️ 跳过词云生成（{emotion_class}类为空或无有效文本）")
        return
    wc = WordCloud(
        font_path="/Users/wooton/Library/Fonts/SourceHanSansSC-Regular.otf",
        background_color="white", width=800, height=400
    ).generate(words)
    wc.to_file(filename)
    print(f"☁️ 词云已生成：{filename}")

gen_wordcloud(df, "正面", "正面情绪词云.png")
gen_wordcloud(df, "负面", "负面情绪词云.png")

# === Step 5: 自动角色画像输出 ===
summary = []

if talk_count.get("我", 0) > talk_count.get("朋友", 0):
    summary.append("✅ 你是对话的主导者，发言频率更高。")
else:
    summary.append("✅ 对方在这段对话中发言更多，节奏主导权更强。")

if df[df["发送者"] == "我"]["极性"].mean() < 0:
    summary.append("😟 你整体情绪偏负面，话语中常带有抱怨、烦躁等表达。")
else:
    summary.append("🙂 你整体情绪偏积极，回应和主动表达都较平和。")

if df["情绪标签"].value_counts().get("安慰", 0) > 5:
    summary.append("🧸 对话中出现多条安慰类表达，说明存在明显的情绪支持关系。")

if df["消息类型"].value_counts().get("语音", 0) > 5:
    summary.append("🎤 使用了较多语音，显示双方有一定的交流亲密度。")

# === 输出结论报告 ===
with open("聊天分析结论报告.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(summary))

print("📄 聊天分析结论报告已生成：聊天分析结论报告.txt")