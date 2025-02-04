from playwright.sync_api import sync_playwright
from datetime import datetime
import re

def extract_number(text):
    if not text:
        return 0
    numbers = re.findall(r'\d+', text.replace(',', ''))
    return int(numbers[0]) if numbers else 0

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except:
        return None

def scrape_facebook_page(username: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page_url = f"https://www.facebook.com/{username}"
        page.goto(page_url)
        
        if "Page not found" in page.title():
            return None
        
        # Extract basic info
        page_info = {
            'username': username,
            'url': page_url,
            'name': page.query_selector('h1').inner_text(),
            'facebook_id': None,
            'profile_pic_url': page.query_selector('img').get_attribute('src'),
            'email': None,
            'website': None,
            'category': None,
            'followers_count': 0,
            'likes_count': 0,
            'creation_date': None,
        }
        
        # Navigate to About page
        about_url = f"{page_url}/about/"
        page.goto(about_url)
        
        # Extract category
        category_el = page.query_selector('div:has-text("Category")')
        if category_el:
            page_info['category'] = category_el.inner_text().split('\n')[-1].strip()
        
        # Extract contact info
        contact_el = page.query_selector('div:has-text("Contact Info")')
        if contact_el:
            for row in contact_el.query_selector_all('div[dir="auto"]'):
                text = row.inner_text()
                if 'Email' in text:
                    page_info['email'] = text.split('\n')[-1]
                elif 'Website' in text:
                    page_info['website'] = text.split('\n')[-1]
        
        # Extract followers and likes
        followers_el = page.query_selector('div:has-text(" followers")')
        page_info['followers_count'] = extract_number(followers_el.inner_text() if followers_el else None)
        
        likes_el = page.query_selector('div:has-text(" likes")')
        page_info['likes_count'] = extract_number(likes_el.inner_text() if likes_el else None)
        
        # Extract creation date
        created_el = page.query_selector('div:has-text("Created")')
        if created_el:
            date_str = created_el.inner_text().split('\n')[-1].strip()
            page_info['creation_date'] = parse_date(date_str)
        
        # Scrape posts (simplified example)
        posts = []
        posts_url = f"{page_url}/posts/"
        page.goto(posts_url)
        post_elements = page.query_selector_all('div[role="article"]')[:25]
        
        for post_el in post_elements:
            content = post_el.query_selector('div[data-ad-preview="message"]').inner_text()
            time_el = post_el.query_selector('abbr')
            timestamp = datetime.fromtimestamp(int(time_el.get_attribute('data-utime'))) if time_el else None
            posts.append({
                'content': content,
                'likes_count': extract_number(post_el.query_selector('div[aria-label="Like"]').inner_text()),
                'shares_count': extract_number(post_el.query_selector('div[aria-label="Share"]').inner_text()),
                'timestamp': timestamp,
                'comments': []
            })
        
        # Followers and following (mock data)
        followers = [{'facebook_id': '1', 'name': 'Follower 1', 'profile_pic_url': 'http://example.com/1.jpg'}]
        following = [{'facebook_id': '2', 'name': 'Following 1', 'profile_pic_url': 'http://example.com/2.jpg'}]
        
        browser.close()
        return {
            'page_info': page_info,
            'posts': posts,
            'followers': followers,
            'following': following
        }