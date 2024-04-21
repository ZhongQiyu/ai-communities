import requests
from bs4 import BeautifulSoup

def search_google_scholar(query):
    base_url = "https://scholar.google.com/scholar"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", class_="gs_r gs_or gs_scl")
        for result in results:
            title = result.find("h3", class_="gs_rt").text
            pdf_link = result.find("a", class_="gs_or_mor").get("href")
            print("Title:", title)
            print("PDF Link:", pdf_link)
            print()
    else:
        print("Error:", response.status_code)

query = "your search keywords"  # 替换为你想要搜索的关键字
search_google_scholar(query)
