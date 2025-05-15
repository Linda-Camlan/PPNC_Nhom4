
import tweepy
import pandas as pd
import csv
import time

# --- API v2 ---
client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAMgy1QEAAAAAKt0CUxTQ94EJEUNas%2B7QeN3qtNg%3DmZ2u7UQVjT726vY0ifvs8tQkOMplvLERtipPwuNhHx22whqqPI")

# --- Từ khóa thay thế trending ---
keywords = ["Chính trị", "đạo đức"]

csv_file = "hot_vi_tweets.csv"
with open(csv_file, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Keyword", "Text", "Created_At", "Likes", "Retweets"])

for keyword in keywords:
    query = f'"{keyword}" lang:vi -is:retweet'
    print(f"📥 Đang tìm kiếm: {keyword}")

    while True:
        try:
            tweets = client.search_recent_tweets(
                query=query,
                max_results=50,
                tweet_fields=['created_at', 'lang', 'public_metrics']
            )
            break  # nếu thành công thì thoát vòng while
        except tweepy.TooManyRequests as e:
            print("⚠️ Quá nhiều yêu cầu! Đang tạm dừng 60 giây...")
            time.sleep(60)
        except Exception as e:
            print(f"❌ Lỗi khác: {e}")
            break

    if tweets and tweets.data:
        with open(csv_file, mode='a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for tweet in tweets.data:
                writer.writerow([
                    keyword,
                    tweet.text.replace('\n', ' '),
                    tweet.created_at,
                    tweet.public_metrics['like_count'],
                    tweet.public_metrics['retweet_count']
                ])
    else:
        print(f"⚠️ Không tìm thấy tweet nào với từ khóa '{keyword}'")

print("✅ Hoàn tất. Dữ liệu đã được lưu vào file:", csv_file)