from lib.llm import GPT4oMini, SYSTEM_PROMPT_OCR
import yaml
import openai

if __name__ == '__main__':
    with open('conf/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    gpt4 = GPT4oMini(api_key=config['openai']['api_key'], temperature=0.9, sys_prompt=SYSTEM_PROMPT_OCR)
    resp = gpt4.chat("Hello, who are you?")
    print(resp)