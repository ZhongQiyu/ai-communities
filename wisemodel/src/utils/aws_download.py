# Jupyter Notebook - Cell 1
# 安装awscli和boto3
!pip install awscli boto3

# Jupyter Notebook - Cell 2
# 配置AWS CLI（需要手动输入密钥）
!aws configure

# Jupyter Notebook - Cell 3
# 创建一个S3存储桶
!aws s3 mb s3://your-bucket-name

# Jupyter Notebook - Cell 4
# 上传模型文件到S3存储桶
!aws s3 cp model_file s3://your-bucket-name/model_file

# Jupyter Notebook - Cell 5
# 导入boto3和定义辅助函数
import boto3
import json

def download_model_from_s3(bucket_name, model_key, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, model_key, download_path)

def generate_question_answer_pairs(model_file_path, input_text):
    # 这里你需要加载和运行你的模型
    with open(model_file_path, 'r') as model_file:
        model_data = model_file.read()
    return f'Question: {input_text}\nAnswer: {model_data}'  # 模拟生成的问答对

# Jupyter Notebook - Cell 6
# 使用函数从S3下载模型并生成问答对
bucket_name = 'your-bucket-name'
model_key = 'model_file'
download_path = 'local_model_file'

# 从S3下载模型
download_model_from_s3(bucket_name, model_key, download_path)

# 使用模型生成问答对
input_text = 'What is the capital of France?'
qa_pairs = generate_question_answer_pairs(download_path, input_text)

print(qa_pairs)
