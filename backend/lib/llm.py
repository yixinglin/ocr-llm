"""
Large Language Models
 
"""
from typing import List, Dict
import openai
from openai.types.chat import ChatCompletion

SYSTEM_PROMPT_ASSISTANT = "You are a helpful assistant."
SYSTEM_PROMPT_OCR = "You are a powerful OCR machine."


class LargeLanguageModel:
    def __init__(self, *args, **kwargs):
        self.model = None

    def chat(self, prompt, last_messages=None):
        raise NotImplementedError()

    def chat_with_image(self, prompt, image_path):
        raise NotImplementedError()


class GPTModel(LargeLanguageModel):
    def __init__(self, api_key, model, sys_prompt, temperature=0.7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.sys_prompt = sys_prompt
        self.temperature = temperature
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)

    def chat(self, prompt: str, last_messages: List[Dict[str, str]] = None):
        messages = [{"role": "system", "content": self.sys_prompt}]
        if last_messages:
            messages.extend(last_messages)
        messages.append({"role": "user", "content": prompt})

        completion: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=[

                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,  # Controls randomness in response, higher temperature means more randomness
        )

        usage = {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens,
        }
        ans = completion.choices[0].message.content
        return {
            "model": self.model,
            "temperature": self.temperature,
            "sys_prompt": self.sys_prompt,
            "usage": usage,
            "answer": ans,
        }

    def __str__(self):
        return f"GPTModel(model={self.model}, temperature={self.temperature}, sys_prompt={self.sys_prompt})"


class GPT4oMini(GPTModel):
    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-4o-mini", *args, **kwargs)


class GPT3_5Turbo(GPTModel):
    def __init__(self, *args, **kwargs):
        super().__init__(model = "gpt-3.5-turbo",*args, **kwargs)


class GPT4o_20240806(GPTModel):

    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-4o-2024-08-06", *args, **kwargs)


def demo1():
    gpt4 = GPT4oMini(api_key="", temperature=0.9, sys_prompt=SYSTEM_PROMPT_OCR)
    resp = gpt4.chat("Hello, who are you?")
    print(resp)
