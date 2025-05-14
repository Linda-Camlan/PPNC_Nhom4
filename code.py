import tweepy
import pandas as pd

# --- Thông tin API ---
api_key = 'PQNTyVyZedRC9fRosO4y9lveq'
api_secret = 'bgIRyxlVp6zNa1q7nb8R5Q2Kbrb4glSHozBCcaY0z65Ow4DaxT'
access_token = '1919320175117320192-JizhUdIEzKPSnxuoNagYz3qDj150uU'
access_token_secret = '0ecswESXHjuptrGs0eBpZaVpLTOZMwHBzUxZrLiYfcmIR'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHs31AEAAAAA2g10YoU1ghmoMKLLSjk%2FQb9rtWM%3DmhtDZOIgMIS0j2aNpvx9qzxXOTzbDVBpKji7Dx5qXPnoErMUth'

# --- Kết nối cả v1.1 (trending) và v2 (search tweet) ---
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)  # v1.1
client = tweepy.Client(bearer_token=bearer_token)  # v2

# --- Lấy trending topic tại Việt Nam ---
VIETNAM_WOEID = 23424984
trends_result = api.get_place_trends(VIETNAM_WOEID)
trending_keywords = [trend['name'] for trend in trends_result[0]['trends'] if trend['name'].isalpha()]

print("🔍 Từ khóa trending ở Việt Nam:", trending_keywords)

# --- Tìm các tweet mới nhất liên quan đến trending keywords ---
tweets_data = []
for keyword in trending_keywords[:5]:  # Lấy 5 từ khóa đầu thôi để tránh giới hạn
    query = f"{keyword} lang:vi -is:retweet"
    tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'lang', 'public_metrics'])

    if tweets.data:
        for tweet in tweets.data:
            tweets_data.append({
                'keyword': keyword,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'likes': tweet.public_metrics['like_count'],
                'retweets': tweet.public_metrics['retweet_count']
            })

# --- Lưu vào CSV ---
df = pd.DataFrame(tweets_data)
df.to_csv("tweets_trending_vietnamese.csv", index=False, encoding='utf-8-sig')

print(f"✅ Đã lưu {len(df)} tweet vào tweets_trending_vietnamese.csv")