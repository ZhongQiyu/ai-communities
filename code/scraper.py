import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def parse_title(url, soup):
    if "jmir.org" in url:
        return soup.find('h1').get_text().strip()
    # 添加其他网站的解析规则
    else:
        return soup.find('title').get_text().strip() if soup.find('title') else "标题未找到"

def get_user_agent(device_type):
    user_agents = {
        'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    }
    return user_agents.get(device_type, user_agents['desktop'])

def fetch_title(url):
    device_type = 'desktop'  # 或 'mobile'
    headers = {'User-Agent': get_user_agent(device_type)}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = parse_title(url, soup)
        return title
    except Exception as e:
        print(f"无法从 {url} 爬取数据: {e}")
        return None

def crawl(urls):
    max_workers = 5  # 设置最大线程数
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交爬取任务到线程池
        future_to_url = {executor.submit(fetch_title, url): url for url in urls}

        # 处理爬取结果
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                title = future.result()  # 获取爬取结果
                if title:
                    print(f"标题：{title}，链接：{url}")
            except Exception as exc:
                print(f'{url} 生成了异常：{exc}')

# 爬取任务列表
urls = [
    'http://example.com/page1',
    'http://example.com/page2',
    'http://example.com/page3',
    # 添加更多的页面链接...
]

crawl(urls)
