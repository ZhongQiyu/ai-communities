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
