import torch
from transformers import AutoTokenizer, RwkvConfig, RwkvModel

model = RwkvModel.from_pretrained("sgugger/rwkv-430M-pile")
tokenizer = AutoTokenizer.from_pretrained("sgugger/rwkv-430M-pile")

inputs = tokenizer("This is an example.", return_tensors="pt")
# Feed everything to the model
outputs = model(inputs["input_ids"])
output_whole = outputs.last_hidden_state

outputs = model(inputs["input_ids"][:, :2])
output_one = outputs.last_hidden_state

# Using the state computed on the first inputs, we will get the same output
outputs = model(inputs["input_ids"][:, 2:], state=outputs.state)
output_two = outputs.last_hidden_state

torch.allclose(torch.cat([output_one, output_two], dim=1), output_whole, atol=1e-5)

from transformers import StoppingCriteria

class RwkvStoppingCriteria(StoppingCriteria):
    def __init__(self, eos_sequence = [187,187], eos_token_id = 537):
        self.eos_sequence = eos_sequence
        self.eos_token_id = eos_token_id

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        last_2_ids = input_ids[:,-2:].tolist()
        return self.eos_sequence in last_2_ids


output = model.generate(inputs["input_ids"], max_new_tokens=64, stopping_criteria = [RwkvStoppingCriteria()])

from transformers import RwkvConfig, RwkvModel

# Initializing a Rwkv configuration
configuration = RwkvConfig()

# Initializing a model (with random weights) from the configuration
model = RwkvModel(configuration)

# Accessing the model configuration
configuration = model.config

from transformers import AutoTokenizer, RwkvModel
import torch

tokenizer = AutoTokenizer.from_pretrained("RWKV/rwkv-4-169m-pile")
model = RwkvModel.from_pretrained("RWKV/rwkv-4-169m-pile")

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs)

last_hidden_states = outputs.last_hidden_state

import torch
from transformers import AutoTokenizer, RwkvForCausalLM

tokenizer = AutoTokenizer.from_pretrained("RWKV/rwkv-4-169m-pile")
model = RwkvForCausalLM.from_pretrained("RWKV/rwkv-4-169m-pile")

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs, labels=inputs["input_ids"])
loss = outputs.loss
logits = outputs.logits


