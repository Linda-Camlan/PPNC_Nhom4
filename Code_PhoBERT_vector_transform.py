import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# 1. Load dữ liệu
df = pd.read_csv("tweets_segmented_full.csv")
texts = df['Text_Segmented'].astype(str).tolist()

# 2. Load PhoBERT
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
model = AutoModel.from_pretrained("vinai/phobert-base")
model.eval()

# 3. Hàm chuyển văn bản thành vector (bằng mean pooling)
def get_phobert_embedding(text):
    tokens = tokenizer.encode(text, return_tensors='pt', max_length=256, truncation=True)
    with torch.no_grad():
        outputs = model(tokens)
        embeddings = outputs.last_hidden_state
        # Mean pooling
        return embeddings.mean(dim=1).squeeze().numpy()

# 4. Tính vector cho từng câu
vectors = []
for text in tqdm(texts):
    try:
        vec = get_phobert_embedding(text)
        vectors.append(vec)
    except:
        vectors.append([0]*768)  # Padding nếu lỗi

# 5. Chuyển vector thành DataFrame
vec_df = pd.DataFrame(vectors)
output_df = pd.concat([df, vec_df], axis=1)

# 6. Lưu kết quả
output_df.to_csv("tweets_with_phobert_vectors.csv", index=False)
