
import openai
from openai.types.chat import ChatCompletion

SYSTEM_PROMPT_OCR = "You are a powerful OCR machine."

class LargeLanguageModel:
    def __init__(self, *args, **kwargs):
        self.model = None

    def chat(self, prompt):
        raise NotImplementedError()


class GPTModel(LargeLanguageModel):
    def __init__(self, api_key, model, sys_prompt, temperature=0.7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.sys_prompt = sys_prompt
        self.temperature = temperature
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)

    def chat(self, prompt: str):
        completion: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,  # Controls randomness in response, higher temperature means more randomness
        )

        usage = completion.usage
        ans = completion.choices[0].message.content
        return {
            "ans": ans,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }

class GPT4oMini(GPTModel):
    def __init__(self, *args, **kwargs):
        super().__init__(model="gpt-4o-mini", *args, **kwargs)

class GPT3_5Turbo(GPTModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = "gpt-3.5-turbo"

class GPT4o_20240806(GPTModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = "gpt-4o-2024-08-06"

def demo1():
    gpt4 = GPT4oMini(api_key="", temperature=0.9, sys_prompt=SYSTEM_PROMPT_OCR)
    resp = gpt4.chat("Hello, who are you?")
    print(resp)