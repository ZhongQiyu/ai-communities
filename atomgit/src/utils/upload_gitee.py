# 创建组织仓库
import requests
import json

# 定义API URL
api_url = 'https://gitee.com/api/v5/orgs/icrl2023/repos'

# 定义请求的headers和data
headers = {'Content-Type': 'application/json;charset=UTF-8'}
data = {'access_token': '','name': 'wqe','has_issues': True,'has_wiki': True,'can_comment': True}

# 将data转换为JSON格式的字符串
json_data = json.dumps(data)

# 发送POST请求
response = requests.post(api_url, headers=headers, data=json_data)

# 检查响应状态码
if response.status_code == 201:
	print('Repository created successfully.')
else:
	print(f'Error: {response.status_code}')
	print(response.json())  # 打印错误信息

# 打印响应头信息
print(response.headers)
