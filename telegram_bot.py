import os
import json
import re
import requests
from bs4 import BeautifulSoup

# نام کاربری کانال عمومی را اینجا وارد کنید (بدون @)
CHANNEL_USERNAME = 'hattrick_channel'  # مثال: bbcPersian, CNN

def get_posts_from_public_channel(username):
    url = f"https://t.me/s/{username}"
    
    try:
        # ارسال درخواست به صفحه کانال
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # تحلیل HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پیدا کردن تمام پست‌ها
        # ساختار HTML تلگرام برای پست‌ها معمولاً در divهای با کلاس 'tgme_channel_history_post' است
        posts_divs = soup.find_all('div', class_='tgme_channel_history_post')
        
        posts = []
        
        # حلقه روی پست‌ها (فقط ۵ پست اول)
        for i, post in enumerate(posts_divs[:5]):
            # استخراج متن
            # متن اصلی معمولاً در div با کلاس 'tgme_post_message' است
            message_div = post.find('div', class_='tgme_post_message')
            if message_div:
                # حذف تگ‌های HTML از متن (مثل <br>، <a> و ...)
                text = message_div.get_text(separator=' ', strip=True)
                
                # استخراج تاریخ
                # تاریخ معمولاً در لینک <a> داخل پست است
                time_tag = post.find('a', class_='tgme_post_time')
                date_str = time_tag['title'] if time_tag else 'Unknown'
                
                # استخراج لینک پست
                post_link = f"https://t.me/{username}/{post['data-post-id']}" if 'data-post-id' in post.attrs else '#'
                
                posts.append({
                    "id": post.get('data-post-id', 'N/A'),
                    "text": text,
                    "date": date_str,
                    "link": post_link
                })
        
        return posts
    
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

def main():
    print(f"Fetching posts from @{CHANNEL_USERNAME}...")
    posts = get_posts_from_public_channel(CHANNEL_USERNAME)
    
    if posts:
        # ذخیره در فایل JSON
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)
        print(f"Success! {len(posts)} posts saved to posts.json")
    else:
        print("No posts found or error occurred.")

if __name__ == '__main__':
    main()
