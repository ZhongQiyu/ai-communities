import json
import requests
import networkx as nx
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

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
