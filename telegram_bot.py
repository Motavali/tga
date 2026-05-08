import os
import json
import requests
from bs4 import BeautifulSoup

# نام کانال عمومی را اینجا وارد کنید (بدون @)
# مثال: 'bbcPersian'
CHANNEL_USERNAME = 'HATTRICK_CHANNEL' 

def get_posts():
    url = f"https://t.me/s/{CHANNEL_USERNAME}"
    print(f"Trying to fetch: {url}")
    
    try:
        # درخواست به تلگرام
        response = requests.get(url, timeout=10)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: Failed to fetch page. Status code: {response.status_code}")
            return []

        # تحلیل HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پیدا کردن پست‌ها
        # ساختار HTML تلگرام ممکن است تغییر کند، اما معمولاً کلاس 'tgme_channel_history_post' ثابت است
        posts = soup.find_all('div', class_='tgme_channel_history_post')
        
        print(f"Found {len(posts)} posts in HTML.")
        
        result = []
        # پردازش ۵ پست اول
        for post in posts[:5]:
            # استخراج متن
            message_div = post.find('div', class_='tgme_post_message')
            if message_div:
                text = message_div.get_text(separator=' ', strip=True)
                
                # استخراج تاریخ
                time_tag = post.find('a', class_='tgme_post_time')
                date_str = time_tag['title'] if time_tag else 'N/A'
                
                # استخراج لینک
                post_id = post.get('data-post-id', 'N/A')
                link = f"https://t.me/{CHANNEL_USERNAME}/{post_id}" if post_id != 'N/A' else '#'
                
                result.append({
                    "id": post_id,
                    "text": text,
                    "date": date_str,
                    "link": link
                })
            else:
                print("Skipping post: No message div found.")
        
        return result

    except Exception as e:
        print(f"Critical Error: {e}")
        return []

def main():
    print("Starting script...")
    posts = get_posts()
    
    if posts:
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(posts)} posts to posts.json")
    else:
        print("No posts saved.")

if __name__ == '__main__':
    main()
