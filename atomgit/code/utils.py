import requests
from bs4 import BeautifulSoup
import torch
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

def search_google_scholar(query):
    query += " AAMAS"  # 限定在 AAMAS 会议上
    query = query.replace(' ', '+')
    url = f"https://scholar.google.com/scholar?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    results = []
    for entry in soup.find_all("div", class_="gs_ri"):
        title = entry.find("h3", class_="gs_rt").a.text
        link = entry.find("h3", class_="gs_rt").a['href']
        author_info = entry.find("div", class_="gs_a").text
        excerpt = entry.find("div", class_="gs_rs").text if entry.find("div", class_="gs_rs") else "No excerpt available"
        result = {
            'title': title,
            'author_info': author_info,
            'excerpt': excerpt,
            'link': link,
            # 'conference': '',
            # 'year': '',
            # 'keywords': '',
            # 'date': '',
            # 'code_url': '',
        }
        # 获取更多细节
        details = get_paper_details(link)
        result.update(details)
        results.append(result)
    return results

def get_paper_details(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
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

    # 返回包含这些信息的字典
    return {
        "conference": conference,
        "year": year,
        "keywords": keywords,
        "code_url": code_url
    }

# 使用 RAG 模型生成文本的函数
def generate_with_rag(query, model, tokenizer):
    inputs = tokenizer(query, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(input_ids=inputs["input_ids"])
    generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return generated_text

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
    for result in results:
        print(f"Title: {result['title']}")
        print("Generating text with RAG for the above title...")
        generated_text = generate_with_rag(result['title'], model, tokenizer)
        print(f"Generated text: {generated_text}")

# 存储论文的详细信息
papers = []

for result in results:
    paper = {}
    paper['title'] = result['title']
    paper['author_info'] = result['author_info']
    paper['excerpt'] = result['excerpt']
    paper['link'] = result['link']
    
    # 获取并存储论文的详细内容
    paper['content'] = get_paper_details(result['link'])
    
    papers.append(paper)
