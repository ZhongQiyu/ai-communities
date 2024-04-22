import os

"""
在环境变量中设置了'DASHSCOPE_API_KEY'：
命令行中执行：export DASHSCOPE_API_KEY='替换成你的apikey'
可以通过命令行：echo $DASHSCOPE_API_KEY 来检查是否真的设置成功
"""

dashscope_example_config = {
    "model_type": "dashscope_chat",
    "config_name": "tongyi_qwen_config",
    "model_name": "qwen-max",
    "api_key": f"{os.environ.get('DASHSCOPE_API_KEY')}",
}

# 使用OpenAI模型(gpt-3.5-turbo，或者替换成其他openai模型)的配置 
# 相似的可以echo $OPENAI_API_KEY 来检查OPENAI_API_KEY是否设置成功
openai_example_config = {
    "model_type": "openai",
    "config_name": "gpt-3.5-config",
    "model_name": "gpt-3.5-turbo",
    "api_key": f"{os.environ.get('OPENAI_API_KEY')}",
    "generate_args": {
        "temperature": 0.5,
    },
}

# 其他可以通过post 访问的LLM接口
# 下面的my_postapi_config可以对应的open ai的post ai端口规则
# curl $YOUR_URL_TO_MODEL \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer $YOUR_API_KEY_IF_ANY" \
# -d '{
#   "model": "XXX",
#   "messages": [
#      .....
#   ]
# }'

postapi_example_config = {
    "model_type": "post_api_chat",
    "config_name": "my_postapi_config",
    "api_url": "$YOUR_URL_TO_MODEL",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY_IF_ANY"
    },
    "messages_key": "messages",
    "json_args": {
        "model": "XXX",
    }
}
