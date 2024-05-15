import requests
import os

# 从环境变量中获取敏感信息
GITHUB_API = "https://api.github.com/search/repositories"
ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')  # GitHub Access Token

ATOMGIT_API = 'https://api.atomgit.com/upload'
ATOMGIT_TOKEN = os.getenv('ATOMGIT_ACCESS_TOKEN')  # AtomGit Access Token

def search_github(paper_title, keywords):
    query = f"{paper_title} {keywords} in:readme,description"
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    params = {'q': query, 'sort': 'stars', 'order': 'desc'}
    response = requests.get(GITHUB_API, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print("Failed to search GitHub:", response.status_code, response.text)
        return None

def upload_to_atomgit(repo_url):
    headers = {
        'Authorization': f'Bearer {ATOMGIT_TOKEN}',
        'X-Api-Version': '2023-02-21'
    }
    data = {'url': repo_url}
    response = requests.post(ATOMGIT_API, headers=headers, json=data)
    if response.status_code == 200:
        print("Successfully uploaded to AtomGit.")
    else:
        print(f"Failed to upload to AtomGit: {response.status_code}, {response.text}")

def main():
    paper_title = input("Enter the paper title: ")
    keywords = input("Enter keywords: ")
    
    repos = search_github(paper_title, keywords)
    if repos:
        for repo in repos:
            print("Found repo:", repo['html_url'])
            upload_to_atomgit(repo['html_url'])

if __name__ == '__main__':
    main()
