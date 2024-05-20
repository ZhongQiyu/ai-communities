import requests
import pandas as pd

# Google Custom Search API配置
API_KEY = 'your_google_api_key'
CX = 'your_custom_search_engine_id'

def search_github_repositories(query):
    """在Google上搜索与查询相关的GitHub代码仓库"""
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}+site:github.com"
    response = requests.get(url)
    results = response.json()
    repositories = []
    if 'items' in results:
        for item in results['items']:
            repositories.append({'title': item['title'], 'link': item['link']})
    return repositories

# 读取论文数据
file_path = 'D:/ai-communities/atomgit/data/paper/IJCAI2023_Accepted_Papers(2).xlsx'
papers_df = pd.read_excel(file_path)

# 添加一个新的列来存储关联的GitHub仓库链接
papers_df['github_repos'] = None

# 遍历每篇论文的标题并进行搜索
for index, row in papers_df.iterrows():
    title = row['title']
    search_results = search_github_repositories(title)
    if search_results:
        papers_df.at[index, 'github_repos'] = search_results

# 保存结果到新的Excel文件
output_file = 'D:/ai-communities/atomgit/data/paper/IJCAI2023_Accepted_Papers_with_GitHub.xlsx'
papers_df.to_excel(output_file, index=False)

print("搜索完成，结果已保存到新的Excel文件。")
