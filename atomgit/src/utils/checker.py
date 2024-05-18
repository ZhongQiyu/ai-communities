import os
import pandas as pd

def load_and_process_data(file_path, output_dir):
    # 加载Excel文件
    df = pd.read_excel(file_path)

    # 使用.T转置DataFrame，然后根据列名合并重复的列
    df = df.T.groupby(level=0).agg(lambda x: x.dropna().iloc[0] if x.notna().any() else pd.NA).T

    # 检查重复的行
    duplicate_rows = df[df.duplicated()]

    # 删除重复的行
    df = df.drop_duplicates()

    return df, duplicate_rows

def process_multiple_files(file_paths, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_path in file_paths:
        # 处理数据
        processed_data, duplicates = load_and_process_data(file_path, output_dir)
        
        # 文件名处理
        base_name = os.path.basename(file_path)
        new_file_name = f'processed_{base_name}'
        duplicate_file_name = f'duplicates_{base_name}'

        # 保存处理后的数据和重复行数据
        processed_data.to_excel(os.path.join(output_dir, new_file_name))
        duplicates.to_excel(os.path.join(output_dir, duplicate_file_name))

        print(f'Processed file saved as: {new_file_name}')
        print(f'Duplicates file saved as: {duplicate_file_name}')

# 文件
file_path = 'data/paper/IJCAI2023_Accepted_Papers(1).xlsx'

# 文件列表
file_paths = [
    'data/paper/IJCAI2023_Accepted_Papers(1).xlsx',
    'data/paper/IJCAI2023_Accepted_Papers(2).xlsx'
]

# 输出目录
output_dir = 'data/paper/'

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 处理多个文件
process_multiple_files(file_paths, output_dir)
