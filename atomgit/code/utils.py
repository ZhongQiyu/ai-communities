import torch
import requests
from bs4 import BeautifulSoup
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
from concurrent.futures import ThreadPoolExecutor

class ScholarSearcher:
    def __init__(self, base_url="https://scholar.google.com/scholar"):
        self.base_url = base_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def get_paper_details(self, query):
        query += " AAMAS"
        query = query.replace(' ', '+')
        url = f"{self.base_url}?q={query}"
        page = requests.get(url, headers=self.headers)
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []

        for entry in soup.find_all("div", class_="gs_ri"):
            title = entry.find("h3", class_="gs_rt").a.text
            link = entry.find("h3", class_="gs_rt").a['href']
            author_info = entry.find("div", class_="gs_a").text
            excerpt = entry.find("div", class_="gs_rs").text if entry.find("div", class_="gs_rs") else "No excerpt available"
            # 假设会议信息位于某个特定的 HTML 元素中
            conference = soup.find("div", class_="conference").text if soup.find("div", class_="conference") else "Not available"
            # 假设年份信息位于某个特定的 HTML 元素中
            year = soup.find("span", class_="year").text if soup.find("span", class_="year") else "Not available"
            # 假设关键字信息位于某个特定的 HTML 元素中
            keywords = [kw.text for kw in soup.find_all("span", class_="keyword")] if soup.find_all("span", class_="keyword") else []
            # 假设代码仓库URL位于页面的一个链接中
            code_url = soup.find("a", text="Source Code").get('href') if soup.find("a", text="Source Code") else "Not available"
            # 假设论文的正文位于特定的HTML元素中，这里需要根据实际页面结构调整
            content = soup.find("div", class_="paper-content").text if soup.find("div", class_="paper-content") else "Content not available"
            
            result = {
                'title': title,
                'author_info': author_info,
                'excerpt': excerpt,
                'link': link,
                'conference': conference,
                'year': year,
                'keywords': keywords,
                'code_url': code_url,
                'content': content
            }
            
            # 获取更多细节
            result.update(details)
            results.append(result)

        return results

    # 使用 RAG 模型生成文本的函数
    def generate_with_ragself(self, query, model, tokenizer):
        inputs = tokenizer(query, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(input_ids=inputs["input_ids"])
        generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return generated_text

    # 定义从URLs获取元数据的函数
    def fetch_metadata(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title').get_text()
                return {'url': url, 'title': title}
            else:
                return {'url': url, 'error': 'Failed to fetch data, status code: ' + str(response.status_code)}
        except Exception as e:
            return {'url': url, 'error': 'Error occurred: ' + str(e)}

    def parse_title(self, url, soup):
        if "jmir.org" in url:
            return soup.find('h1').get_text().strip()
        # 添加其他网站的解析规则
        else:
            return soup.find('title').get_text().strip() if soup.find('title') else "标题未找到"

    def get_user_agent(self, device_type):
        user_agents = {
            'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
        }
        return user_agents.get(device_type, user_agents['desktop'])

    def fetch_title(self, url):
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

    def crawl(self, urls):
        max_workers = 5  # 设置最大线程数
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交爬取任务到线程池
            future_to_url = {executor.submit(fetch_title, url): url for url in urls}
            # 处理爬取结果
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                metadata = fetch_metadata(url)
                print(metadata)
                try:
                    title = future.result()  # 获取爬取结果
                    if title:
                        print(f"标题：{title}，链接：{url}")
                except Exception as exc:
                    print(f'{url} 生成了异常：{exc}')

# define the searcher
searcher = ScholarSearcher()

# 测试从URLs获取元数据的功能
urls = [
    "https://link.springer.com/article/10.1007/s10458-023-09601-0",
    "https://link.springer.com/article/10.1007/s10458-022-09583-5",
    "https://www.ijcai.org/proceedings/2023/0051.pdf",
    "https://link.springer.com/chapter/10.1007/978-3-031-49133-7_4",
    # 更多链接...
]
searcher.crawl(urls)

# 测试搜索和文本生成功能
search_queries = ["deep learning", "machine learning", "neural networks"]
for query in search_queries:
    print(f"Query: {query}")
    results = search_google_scholar(query)
    # retrieve the metadata of the papers
    paper = {}
    paper['title'] = result['title']
    paper['author_info'] = result['author_info']
    paper['excerpt'] = result['excerpt']
    paper['link'] = result['link']
    # 获取并存储论文的详细内容
    paper['content'] = get_paper_details(result['link'])
    papers.append(paper)
    # iterate through the papers
    for result in results:
        print(f"Title: {result['title']}")
        print("Generating text with RAG for the above title...")
        generated_text = generate_with_rag(result['title'], model, tokenizer)
        print(f"Generated text: {generated_text}")

# 存储论文的详细信息
papers = []

# 初始化 RAG 模型
model_name = "facebook/rag-token-nq"
tokenizer = RagTokenizer.from_pretrained(model_name)
retriever = RagRetriever.from_pretrained(model_name, index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained(model_name, retriever=retriever)

# 搜索词列表
search_queries = ["deep learning", "machine learning", "neural networks"]

# 检索并生成文本
for query in search_queries:
    print(f"Query: {query}")
    results = search_google_scholar(query)
    if isinstance(results, dict) and 'error' in results:
        print(results['error'])
    else:
        for result in results:
            print(f"Title: {result['title']}")
            print("Generating text with RAG for the above title...")
            generated_text = generate_with_rag(result['title'], model, tokenizer)
            print(f"Generated text: {generated_text}")
