# main.py

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

# pip install -e .\[full\]

# as_studio conversation.py

# bash-3.2$ as_studio conversation.py
