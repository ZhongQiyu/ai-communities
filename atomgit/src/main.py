import re
import json
import requests
import pdfplumber
import networkx as nx
from github import Github
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class PDFAnalyzer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text_from_pdf()

    def extract_text_from_pdf(self):
        """从PDF中提取所有文本"""
        with pdfplumber.open(self.pdf_path) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    def extract_metadata(self):
        """从PDF文本中提取论文元数据"""
        metadata = {}

        title_match = re.search(r"\b(Title|TITLE|title)\b: (.*)", self.text)
        metadata["title"] = title_match.group(2).strip() if title_match else ""

        author_match = re.search(r"\b(Authors|AUTHORS|authors)\b: (.*)", self.text)
        metadata["authors"] = author_match.group(2).strip() if author_match else ""

        keywords_match = re.search(r"\b(Keywords|KEYWORDS|keywords)\b: (.*)", self.text)
        metadata["keywords"] = keywords_match.group(2).strip() if keywords_match else ""

        return metadata

    def fetch_data(self, keyword):
        """根据关键词从Google中检索数据"""
        # 指定搜索的URL（使用Google搜索为例）
        url = f"https://www.google.com/search?q={keyword}"
        # 设置请求头，模拟浏览器访问
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        # 解析网页内容
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            snippets = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
            # 存储结果
            results = [snippet.get_text() for snippet in snippets]
            # 将结果存为JSON文件
            with open(f"{keyword.replace(' ', '_')}_snippets.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print(f"Data for {keyword} stored.")
        else:
            print("Failed to retrieve data.")

    def find_urls(self):
        """从PDF文本中提取所有URL"""
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.text)

class PDFGitHubAnalyzer(PDFAnalyzer):
    def __init__(self, github_token, pdf_path):
        super().__init__(pdf_path)
        self.github = Github(github_token)

    def search_github(self, query):
        """在GitHub上搜索代码仓库"""
        repositories = self.github.search_repositories(query)
        for repo in repositories:
            print(repo.clone_url)

    def extract_and_search(self):
        """提取PDF文本并在GitHub上搜索相关代码"""
        # 假设从提取的文本中得到了论文标题或关键词
        title = self.extract_metadata().get("title", "")
        # 这里需要具体的逻辑来确定如何从文本中提取标题或关键词
        # 以下仅为示例，你需要根据实际情况调整
        if title:
            self.search_github(title)

    def query_external_service(title):
        # 使用论文标题从外部服务（如Semantic Scholar）检索额外信息
        headers = {"x-api-key": "your_api_key"}
        response = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}", headers=headers)

        if response.status_code == 200:
            return response.json()

        return {}

    def visualize_keywords(self, keywords, relations):
        """绘制关键词关系图"""
        G = nx.DiGraph()
        G.add_nodes_from(keywords)
        G.add_edges_from(relations)
        nx.write_gexf(G, "network_graph.gexf")
        plt.figure(figsize=(12, 8))
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', linewidths=1, font_size=15)
        plt.title('Keyword Network')
        plt.show()

# 主逻辑
if __name__ == "__main__":
    # 初始化PDF文件路径
    pdf_path = "example.pdf"  # 替换为你的PDF文件路径

    # 从PDF中提取文本；假设论文的标题或关键词在某个固定位置，或使用正则表达式自行提取
    text = extract_text_from_pdf(pdf_path)
    title = "Your paper title here extracted from the text"
    search_github(title)
    metadata = extract_metadata(text)
    if metadata.get("title"):
        additional_info = query_external_service(metadata["title"])
        metadata.update(additional_info)
    print(metadata)

    # 创建实例
    analyzer = PDFGitHubAnalyzer(github_token, pdf_path)
    analyzer.extract_and_search()

    # 使用正则表达式查找URLs
    urls = analyzer.find_urls()

    # 打印找到的所有URLs
    for url in urls:
        print(url)
    analyzer.visualize_keywords(keywords, relations)

    # 添加节点，即关键字
    keywords = ['Decision Making', 'Emotional Intelligence', 'Natural Language Generation',
                'Collaboration', 'Ethics', 'Generalization', 'Real-Time Learning',
                'Human-Agent Interaction', 'Explainability', 'Multimodal Perception']
    for keyword in keywords:
        analyzer.fetch_data(keyword)

    # 初始化GitHub客户端并搜索相关代码
    github_token = "ghp_xxxxYYYYZZZZxxxxYYYYZZZZ"  # 替换为你的真实GitHub访问令牌
    g = Github("<your_token>")

    # 添加边
    relations = [('Emotional Intelligence', 'Human-Agent Interaction'),
                 ('Natural Language Generation', 'Decision Making'),
                 ('Decision Making', 'Collaboration'),
                 ('Ethics', 'Decision Making'),
                 ('Generalization', 'Real-Time Learning'),
                 ('Real-Time Learning', 'Explainability'),
                 ('Human-Agent Interaction', 'Multimodal Perception')]

    # 创建图
    G = nx.DiGraph()
    G.add_nodes_from(keywords)
    G.add_edges_from(relations)

    # 保存为 GEXF 文件
    nx.write_gexf(G, "network_graph.gexf")

    # 绘制网络图
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', linewidths=1, font_size=15)
    plt.title('Keyword Network')
    plt.show()

    # 示例使用一个关键词
    fetch_data('Decision Making in Multi-Agent Systems')

    # 完整示例，遍历所有关键词并抓取数据
    for keyword in keywords:
        # 示例使用一个关键词
        fetch_data(keyword)
