import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

# 定义 Gemma 模型
class GemmaModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GemmaModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# 定义新的模型配置
new_input_size = 10
new_hidden_size = 20
new_output_size = 1
num_epochs = 10  # 假设训练的 epoch 数量

# 准备数据集
X = ...
y = ...

# 定义交叉验证
kfold = KFold(n_splits=5, shuffle=True)

# 定义空列表来存储每个折的准确率
accuracies = []

# 进行交叉验证
for fold, (train_indices, val_indices) in enumerate(kfold.split(X)):
    X_train, y_train = X[train_indices], y[train_indices]
    X_val, y_val = X[val_indices], y[val_indices]

    # 创建新的 Gemma 模型实例
    new_model = GemmaModel(new_input_size, new_hidden_size, new_output_size)

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.SGD(new_model.parameters(), lr=0.01)  # 重新配置学习率

    # 使用新的模型配置重新训练模型
    for epoch in range(num_epochs):
        # 前向传播
        outputs = new_model(X_train)
        loss = criterion(outputs, y_train)
        
        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # 在验证集上评估模型
    val_outputs = new_model(X_val)
    val_predictions = torch.argmax(val_outputs, dim=1)  # 假设输出是分类问题，使用 argmax 得到预测结果
    val_accuracy = accuracy_score(y_val, val_predictions)
    accuracies.append(val_accuracy)
    print(f"Fold {fold+1}, Validation Accuracy: {val_accuracy}")

# 计算平均准确率
avg_accuracy = sum(accuracies) / len(accuracies)
print(f"Average Validation Accuracy: {avg_accuracy}")

# 计算平均验证分数
avg_val_score = ...  # 计算所有折的验证分数的平均值
print(f"Average Validation Score: {avg_val_score}")



import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

response = openai.Completion.create(
  engine="text-davinci-003",  # 可替换为其他模型
  prompt="假面骑士剑角色扮演对话系统：\nHuman: 你好，剑。\nAI: 欢迎来到假面骑士的世界！你今天的任务是什么？\nHuman: ",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=["\n"]
)

print(response.choices[0].text.strip())
