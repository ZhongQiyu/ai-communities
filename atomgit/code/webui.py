import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import gradio as gr
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

# 定义GCN模型
class GCN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return torch.sigmoid(x)

# 实例化模型，定义图数据
num_features = 2
num_classes = 2
model = GCN(num_features, num_classes)
node_features = torch.tensor([[1, 2], [3, 4], [5, 6]], dtype=torch.float)
edge_index = torch.tensor([[0, 1], [1, 2]], dtype=torch.long)
graph_data = Data(x=node_features, edge_index=edge_index.t().contiguous())

# 模拟模型训练过程（实际应用中应使用真实数据集）
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
model.train()
for epoch in range(200):  # 这里只是模拟训练，没有定义真实的损失函数和数据
    optimizer.zero_grad()
    out = model(graph_data)
    loss = torch.sum(out)  # 模拟一个损失
    loss.backward()
    optimizer.step()

# 实例化RAG模型用于回答问题
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
rag_model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

def get_answer(question):
    input_ids = tokenizer(question, return_tensors="pt").input_ids
    output_ids = rag_model.generate(input_ids)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Gradio界面展示
def recommend(user_id):
    # 简化的推荐逻辑，实际应用中应根据用户ID和模型提供个性化推荐
    return "Desk 1: Modern, White, Medium\nDesk 2: Minimalistic, Black, Small"

def answer_question(question):
    return get_answer(question)

iface = gr.Interface(
    fn=[recommend, answer_question],
    inputs=[gr.inputs.Textbox(label="User ID"), gr.inputs.Textbox(label="Question about desks")],
    outputs=[gr.outputs.Textbox(label="Recommendations"), gr.outputs.Textbox(label="Answer")],
    title="Learning Desk Recommendation & FAQ"
)

iface.launch()
