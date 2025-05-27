import py_vncorenlp
import pandas as pd
import re
# Tải file stopwords từ GitHub
import requests

stopword_url = "https://raw.githubusercontent.com/stopwords/vietnamese-stopwords/master/vietnamese-stopwords.txt"
stopwords = requests.get(stopword_url).text.splitlines()
stopwords = [word.strip() for word in stopwords if word.strip() != ""]

# Khởi tạo VnCoreNLP với đầy đủ annotators
rdrsegmenter = py_vncorenlp.VnCoreNLP(
    annotators=["wseg", "pos", "ner"],
    save_dir='E:/crawldatausingx/dowload/VnCoreNLP-1.2/VnCoreNLP-1.2'
)

# Đọc dữ liệu từ CSV
df = pd.read_csv("E:/crawldatausingx/tweets_segmented_full.csv")


# Làm sạch văn bản
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Zà-ỹÀ-Ỹ0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
  # Bỏ stopword
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return ' '.join(words)

# Áp dụng làm sạch
df['Text_Clean'] = df['Text_Clean'].apply(clean_text)
df = df.drop_duplicates(subset="Text_Clean", keep="first")
df['Created_At'] = pd.to_datetime(df['Created_At'], errors='coerce')
df = df.dropna(subset=['Created_At', 'Text_Clean'])
df = df[df['Text_Clean'].str.len() > 10]
df = df.reset_index(drop=True)




# Áp dụng phân tích NLP cho mỗi dòng
df['Text_Segmented'] = df['Text_Clean'].apply(lambda x: ' '.join(rdrsegmenter.word_segment(x)))
# Lưu file kết quả
df_final = df[['Keyword', 'Text_Clean', 'Text_Segmented', 'Created_At']]
df_final.to_csv("E:/crawldatausingx/tweets_segmented_full.csv", index=False, encoding='utf-8-sig')

print("✅ Đã xử lý xong phân tích từ vựng, từ loại và thực thể. File lưu tại tweets_segmented_full.csv")
