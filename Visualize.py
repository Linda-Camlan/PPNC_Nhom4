import pandas as pd
from bertopic import BERTopic
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# 1. Load mô hình và dữ liệu
# =============================

# Load mô hình BERTopic đã lưu
topic_model = BERTopic.load("bertopic_phobert_model")

# Đọc file info
df = pd.read_csv("document_topic_info.csv", encoding="utf-8-sig")

# Đổi tên cột cho gọn
df.rename(columns={"Topic": "topic", "Name": "topic_name"}, inplace=True)

# =============================
# 2. Biểu đồ phân bố topic
# =============================

# Loại bỏ outlier (-1)
df_filtered = df[df["topic"] != -1]

# Đếm số văn bản mỗi topic
topic_counts = df_filtered["topic_name"].value_counts().sort_values(ascending=True)

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
sns.barplot(x=topic_counts.values, y=topic_counts.index, palette="viridis")
plt.xlabel("Số lượng văn bản")
plt.ylabel("Chủ đề (topic)")
plt.title("📊 Phân bố số lượng văn bản theo từng chủ đề")
plt.tight_layout()
plt.show()

# =============================
# 3. In mẫu văn bản mỗi topic
# =============================
print("\n================= 📝 MẪU VĂN BẢN MỖI TOPIC =================")

for topic in df_filtered["topic"].unique():
    row = df_filtered[df_filtered["topic"] == topic].iloc[0]
    print(f"\n🟩 Topic {topic} - {row['topic_name']}")
    print(f"📄 {row['Document'][:200]}...")  # In 200 ký tự đầu

# =============================
# 4. Biểu đồ từ khóa đại diện
# =============================

print("\n📌 Đang tạo biểu đồ từ khóa đại diện mỗi topic...")

# Hiển thị interactive plot (plotly)
topic_model.visualize_barchart(top_n_topics=10).show()

# (Tùy chọn) Lưu HTML
topic_model.visualize_barchart(top_n_topics=10).write_html("barchart_keywords.html")
topic_model.visualize_topics().write_html("topic_map.html")
