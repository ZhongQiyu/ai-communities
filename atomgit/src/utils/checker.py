import pandas as pd

def load_and_process_data(file_path):
    # 加载Excel文件
    df = pd.read_excel(file_path)

    # 合并重复的列（基于列名）
    df = df.groupby(level=0, axis=1).agg(lambda x: x.dropna().iloc[0] if x.notna().any() else pd.NA)

    # 检查重复的行
    duplicate_rows = df[df.duplicated()]

    # 删除重复的行
    df = df.drop_duplicates()

    return df, duplicate_rows

# 请替换下面的路径为你的Excel文件路径
file_path = 'path_to_your_excel_file.xlsx'
# 如果Excel文件和Python脚本在同一目录下
# file_path = 'IJCAI2023_Accepted_Papers.xlsx'
# 如果Excel文件在脚本所在目录的子文件夹中，比如一个名为"data"的文件夹
file_path = 'data/IJCAI2023_Accepted_Papers.xlsx'

# 加载并处理文件路径等
processed_data, duplicates = load_and_process_data(file_path)

print("Processed Data:")
print(processed_data)
print("\nDuplicate Rows:")
print(duplicates)
