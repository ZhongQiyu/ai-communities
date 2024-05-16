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
