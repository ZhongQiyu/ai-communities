import agentscope

# 让config生效
agentscope.init(
    model_configs=[
      dashscope_example_config,
      openai_examaple_config,
      # 其他模型配置也可以继续添加在这里~
    ],
)

from agentscope.agents import DialogAgent

dialog_agent = DialogAgent(
    name="Assistant",
    sys_prompt="You're a helpful assistant.",
    model_config_name="tongyi_qwen_config",  # 其中一个你在上面步骤准备好的配置名字（config_name对应的值）
)

import os
import agentscope
from agentscope.agents import DialogAgent
from agentscope.agents.user_agent import UserAgent

def main() -> None:
    """A basic conversation demo"""

    dashscope_example_config = {
      "model_type": "dashscope_chat",
      "config_name": "tongyi_qwen_config",
      "model_name": "qwen-max",
      "api_key": f"{os.environ.get('DASHSCOPE_API_KEY')}",
    }
    agentscope.init(
        model_configs=[dashscope_example_config],
    )

    dialog_agent = DialogAgent(
        name="Assistant",
        sys_prompt="You're a helpful assistant.",
        model_config_name="tongyi_qwen_config",
    )
    user_agent = UserAgent()

    x = None
    while x is None or x.content != "exit":
        x = dialog_agent(x) 
        x = user_agent(x)

from agentscope.agents.user_agent import UserAgent

user_agent = UserAgent()

# start the conversation between user and assistant
x = None
while x is None or x.content != "exit":
    x = dialog_agent(x)
    x = user_agent(x)
