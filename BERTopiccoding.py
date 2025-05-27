import pandas as pd
from bertopic import BERTopic
from sklearn.decomposition import PCA
import numpy as np

# Bước 1: Đọc dữ liệu đã có embedding
df = pd.read_csv("tweets_with_phobert_vectors.csv", encoding="utf-8-sig")

# Bước 2: Lấy danh sách văn bản và embedding
docs = df['Text_Segmented'].tolist()
embedding_columns = df.columns[4:]  # Bỏ 3 cột đầu là: Keyword, Text_Clean, Created_At
embeddings = df[embedding_columns].values.tolist()
embeddings = np.array(embeddings)

# (Tùy chọn) Giảm chiều embedding xuống 50 chiều nếu thấy chậm
# from sklearn.decomposition import PCA
# pca = PCA(n_components=50)
# embeddings = pca.fit_transform(embeddings)

# Bước 3: Tạo mô hình BERTopic (dùng embedding từ PhoBERT)
topic_model = BERTopic(min_topic_size=5 ,language="multilingual", verbose=True) #
topics, probs = topic_model.fit_transform(docs, embeddings)
topic_model.save("bertopic_phobert_model")
print("\n✅ Đã lưu mô hình BERTopic vào thư mục: bertopic_phobert_model")


# Bước 4: In ra 5 chủ đề phổ biến nhất
print("\n📌 Top 5 chủ đề được phát hiện:")
print(topic_model.get_topic_info().head())
print(topic_model.get_topic(3))
doc_info = topic_model.get_document_info(docs)
doc_info.to_csv("document_topic_info.csv", index=False, encoding='utf-8-sig')
print("\n✅ Đã lưu chi tiết văn bản và chủ đề vào file: document_topic_info.csv")
# Bước 5: Lưu kết quả ra file CSV mới
df['Topic'] = topics
df.to_csv("tweets_with_topics.csv", index=False, encoding='utf-8-sig')
print("\n✅ Đã lưu kết quả phân chủ đề vào file: tweets_with_topics.csv")

# (Tùy chọn) Trực quan hóa
#topic_model.visualize_topics().show()

