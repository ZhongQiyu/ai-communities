from scholarly import scholarly

def search_ijcai_papers(keywords):
    # 构造搜索查询
    query = f"{keywords} source:IJCAI"

    # 搜索论文
    search_query = scholarly.search_pubs(query)
    
    # 获取并显示搜索结果的摘要信息
    for i, paper in enumerate(search_query):
        print(f"Paper {i+1}: {paper.bib['title']}")
        print("Authors:", paper.bib['author'])
        print("Abstract:", paper.bib.get('abstract', 'No abstract available'))
        print("Publication year:", paper.bib.get('pub_year', 'No publication year available'))
        print("URL:", paper.bib.get('url', 'No URL available'))
        print("-" * 80)
        if i >= 9:  # 限制输出到前10篇文章
            break

def main():
    keywords = [
        "multi-agent systems",
        "agent-based modeling",
        "distributed AI",
        "cooperative agents",
        "autonomous agents"
    ]
    
    # 对每个关键词进行搜索
    for keyword in keywords:
        print(f"Searching for papers with keyword: {keyword}")
        search_ijcai_papers(keyword)
        print("=" * 100)

if __name__ == '__main__':
    main()


import requests
import os

def download_papers(base_url, start, end, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(start, end + 1):
        file_number = str(i).zfill(4)  # 填充数字，如0001, 0002,...
        file_url = f"{base_url}/{file_number}.pdf"
        response = requests.get(file_url, stream=True)

        if response.status_code == 200:
            file_path = os.path.join(output_dir, f"{file_number}.pdf")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {file_path}")
        else:
            print(f"Failed to download {file_url}")

# 配置参数
base_url = "https://www.ijcai.org/proceedings/2023"
start_number = 1
end_number = 851  # 你需要知道有多少篇论文，这里假设是1000篇
output_directory = "D:/macOS/ai-communities/atomgit/data/paper/IJCAI-23"

# 执行下载函数
download_papers(base_url, start_number, end_number, output_directory)
