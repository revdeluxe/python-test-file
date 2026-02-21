from transformers import pipeline
import torch
from .base import AIProvider

class LocalProvider(AIProvider):
    def __init__(self, model_path="./models/gemma-3"):
        self.pipe = pipeline(
            "text-generation",
            model=model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )

    def generate(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        outputs = self.pipe(messages, max_new_tokens=256)
        return outputs[0]["generated_text"][-1]["content"]