import os
import json
import requests
from bs4 import BeautifulSoup

# لینک مستقیم پست تلگرام را اینجا وارد کنید
# مثال: 'https://t.me/s/HATTRICK_CHANNEL/24608'
POST_URL = 'https://t.me/s/HATTRICK_CHANNEL/24608'

def get_post_data(url):
    print(f"Fetching data from: {url}")
    
    try:
        # تنظیم هدر برای شبیه‌سازی مرورگر
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # درخواست به صفحه پست
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # تحلیل HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج متن پست
        # متن پست معمولاً در div با کلاس 'tgme_post_message' است
        message_div = soup.find('div', class_='tgme_post_message')
        
        if message_div:
            # حذف تگ‌های HTML و دریافت متن خالص
            text = message_div.get_text(separator=' ', strip=True)
            
            # استخراج تاریخ
            # تاریخ معمولاً در لینک <a> با کلاس 'tgme_post_time' است
            time_tag = soup.find('a', class_='tgme_post_time')
            date_str = time_tag['title'] if time_tag else 'Unknown Date'
            
            # استخراج لینک پست (همان لینک ورودی)
            post_link = url
            
            # استخراج شناسه پست از URL
            # فرمت URL: https://t.me/s/channel/post_id
            post_id = url.strip('/').split('/')[-1]
            
            return {
                "id": post_id,
                "text": text,
                "date": date_str,
                "link": post_link
            }
        else:
            print("Error: Could not find the post message div.")
            return None
            
    except Exception as e:
        print(f"Error fetching post: {e}")
        return None

def main():
    print("Starting Telegram Post Scraper...")
    
    # دریافت اطلاعات پست
    post_data = get_post_data(POST_URL)
    
    if post_data:
        # ذخیره در فایل JSON
        # اگر می‌خواهید لیستی از پست‌ها داشته باشید، می‌توانید این دیکشنری را در یک لیست قرار دهید
        posts_list = [post_data]
        
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts_list, f, ensure_ascii=False, indent=4)
            
        print(f"Success! Post ID {post_data['id']} saved to posts.json")
        print(f"Text preview: {post_data['text'][:50]}...")
    else:
        print("Failed to fetch post data.")

if __name__ == '__main__':
    main()            if message_div:
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
