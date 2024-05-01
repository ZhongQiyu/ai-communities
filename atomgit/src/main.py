<<<<<<< HEAD
import re
import json
import requests
import pdfplumber
import networkx as nx
from github import Github
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class PDFGitHubExtractor:
    def __init__(self, github_token, pdf_path):
        self.github = Github(github_token)  # 初始化GitHub客户端
        self.pdf_path = pdf_path            # 设置PDF文件路径

    def extract_text_from_pdf(self):
        """从PDF中提取所有文本"""
        with pdfplumber.open(self.pdf_path) as pdf:
            all_text = ''
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text
        return all_text

    def search_github(self, query):
        """根据查询在GitHub上搜索仓库，并打印克隆URL"""
        repositories = self.github.search_repositories(query)
        for repo in repositories:
            print(repo.clone_url)

    def extract_and_search(self):
        """提取PDF文本并使用其中的标题或关键词在GitHub上搜索相关代码"""
        extracted_text = self.extract_text_from_pdf()
        # 假设从提取的文本中得到了论文标题或关键词
        # 这里需要具体的逻辑来确定如何从文本中提取标题或关键词
        # 以下仅为示例，你需要根据实际情况调整
        title = "Your paper title here extracted from the text"
        self.search_github(title)

# 创建实例
extractor = PDFGitHubExtractor(github_token, pdf_path)
extractor.extract_and_search()

# 初始化PDF文件路径
pdf_path = '/Users/yourusername/Desktop/my_paper.pdf'  # 替换为你的PDF文件路径
# pdf_path = '<path_to_your_pdf_file.pdf>'

# 从PDF中提取文本；假设论文的标题或关键词在某个固定位置，或使用正则表达式自行提取
title = "Your paper title here extracted from the text"
extracted_text = extract_text_from_pdf(pdf_path)

# 使用正则表达式查找URLs
urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', all_text)

# 打印找到的所有URLs
for url in urls:
    print(url)

# 初始化GitHub客户端
github_token = "ghp_xxxxYYYYZZZZxxxxYYYYZZZZ"  # 替换为你的真实GitHub访问令牌
g = Github("<your_token>")
# g = Github("ghp_xxxxYYYYZZZZxxxxYYYYZZZZ")

# 在GitHub上搜索相关代码
search_github(title)



=======
import json
import requests
import networkx as nx
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

>>>>>>> 7f14b110f41c20247774a14142ca13d301c233d6
# 创建图
G = nx.DiGraph()

# 添加节点和边
keywords = ['Decision Making', 'Emotional Intelligence', 'Natural Language Generation',
            'Collaboration', 'Ethics', 'Generalization', 'Real-Time Learning',
            'Human-Agent Interaction', 'Explainability', 'Multimodal Perception']

relations = [('Emotional Intelligence', 'Human-Agent Interaction'),
             ('Natural Language Generation', 'Decision Making'),
             ('Decision Making', 'Collaboration'),
             ('Ethics', 'Decision Making'),
             ('Generalization', 'Real-Time Learning'),
             ('Real-Time Learning', 'Explainability'),
             ('Human-Agent Interaction', 'Multimodal Perception')]

G.add_nodes_from(keywords)
G.add_edges_from(relations)

# 保存为 GEXF 文件
nx.write_gexf(G, "network_graph.gexf")

def fetch_data(keyword):
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
        results = []
        for snippet in snippets:
            text = snippet.get_text()
            results.append(text)
        # 将结果存为JSON文件
        with open(f"{keyword.replace(' ', '_')}_snippets.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Data for {keyword} stored.")
    else:
        print("Failed to retrieve data.")

# 示例使用一个关键词
fetch_data('Decision Making in Multi-Agent Systems')

# 遍历所有关键词并抓取数据
for keyword in keywords:
    # 示例使用一个关键词
    fetch_data(keyword)

# 创建一个空的有向图
G = nx.DiGraph()

# 添加节点（关键词）
keywords = ['Decision Making', 'Emotional Intelligence', 'Natural Language Generation',
            'Collaboration', 'Ethics', 'Generalization', 'Real-Time Learning',
            'Human-Agent Interaction', 'Explainability', 'Multimodal Perception']

for keyword in keywords:
    G.add_node(keyword)

# 添加边（关键词之间的关系）
relations = [('Emotional Intelligence', 'Human-Agent Interaction'),
             ('Natural Language Generation', 'Decision Making'),
             ('Decision Making', 'Collaboration'),
             ('Ethics', 'Decision Making'),
             ('Generalization', 'Real-Time Learning'),
             ('Real-Time Learning', 'Explainability'),
             ('Human-Agent Interaction', 'Multimodal Perception')]

for src, dst in relations:
    G.add_edge(src, dst)

# 绘制网络图
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', linewidths=1, font_size=15)
plt.title('Keyword Network')
plt.show()
