import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bertopic import BERTopic
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
def main():
    # 1. Đọc dữ liệu văn bản và embeddings
    input_file = "tweets_with_phobert_vectors.csv"
    df = pd.read_csv(input_file, encoding="utf-8-sig")
    docs = df['Text_Segmented'].tolist()
    emb_cols = df.columns.tolist()[4:]
    embeddings = df[emb_cols].values

    # 2. Chuẩn bị dữ liệu cho Gensim
    texts = [doc.split() for doc in docs]
    dictionary = Dictionary(texts)

    # 3. Đánh giá BERTopic với các giá trị min_topic_size
    results = []
    range_min_topic = range(2, 6)

    for m in range_min_topic:
        print(f"\n=== Evaluating min_topic_size={m} ===")
        topic_model = BERTopic(min_topic_size=m, language="multilingual", verbose=True)
        topics, probs = topic_model.fit_transform(docs, embeddings)

        topic_ids = [t for t in topic_model.get_topic_info().Topic if t != -1]
        topic_words = [[w for w, _ in topic_model.get_topic(tid)] for tid in topic_ids]

        coherence = CoherenceModel(
            topics=topic_words, texts=texts, dictionary=dictionary, coherence='c_v'
        ).get_coherence()

        all_words = sum(topic_words, [])
        diversity = len(set(all_words)) / len(all_words) if all_words else 0

        results.append({
            "min_topic_size": m,
            "coherence": coherence,
            "diversity": diversity
        })

    # 4. Tạo DataFrame kết quả và lưu
    results_df = pd.DataFrame(results)
    results_df.to_csv("bertopic_evaluation.csv", index=False, encoding="utf-8-sig")

    # 5. Trực quan hóa kết quả
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['min_topic_size'], results_df['coherence'], marker='o', label='Coherence')
    plt.plot(results_df['min_topic_size'], results_df['diversity'], marker='s', label='Diversity')
    plt.title("BERTopic Evaluation by min_topic_size")
    plt.xlabel("min_topic_size")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(True)
    plt.savefig("bertopic_evaluation_plot.png")
    plt.show()
if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()  # không bắt buộc, nhưng an toàn nếu đóng gói thành exe
    main()
