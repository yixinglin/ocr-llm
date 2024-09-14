import json
import os.path
from typing import List

import cv2
import pandas as pd
import yaml

from core.exceptions import LLM_JsonDecodeError
from lib.llm import LargeLanguageModel, SYSTEM_PROMPT_OCR, GPT4oMini, GPT4o_20240806
from lib.ocrutils import TesseractOCR, OCRUtils, OCR_Annotation
from string import Template


def gpt_answer_to_json(answer):
    data = answer.replace("```json", "").replace("```", "")
    # Delete empty lines
    data = "\n".join([line for line in data.split("\n") if line.strip()])
    data = json.loads(data)
    return data


class OCR_LLM_Service:

    def __init__(self, *args, **kwargs):
        pass


class TesseractOCR_GPT_Service(OCR_LLM_Service):

    def __init__(self, temperature=0.7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt_path = os.path.join("assets", "prompts.md")
        self.conf_path = os.path.join("conf", "config.yaml")
        self.temperature = temperature
        self.sys_prompt = SYSTEM_PROMPT_OCR
        self.prompt_template = None
        self.conf = None
        self.api_key = None
        self.initialize()
        self.GPT_MODEL = GPT4oMini
        self.results = None
        self.ocr = None
        self.llm = None

    def initialize(self):
        with open(self.prompt_path, "r", encoding="utf-8") as fp:
            self.prompt_template = fp.read()

        with open(self.conf_path, 'r', encoding="utf-8") as fp:
            self.conf = yaml.safe_load(fp)

        self.api_key = self.conf['openai']['api_key']

    def run(self, image_path):
        ocr = TesseractOCR(image_path=image_path, lang="deu")
        llm = self.GPT_MODEL(api_key=self.api_key, temperature=self.temperature,
                             sys_prompt=self.sys_prompt)
        self.ocr = ocr
        self.llm = llm
        anno = ocr.to_data()
        for a in anno:
            a.confidence = 100

        text = ocr.to_plain_text()


        template = Template(self.prompt_template)
        json_anno = [ a.dict() for a in anno]
        prompt = template.substitute(OCR_NAME=ocr.name, OCR_OUTPUT=text)
        chat_response = llm.chat(prompt)
        try:
            chat_response['answer'] = gpt_answer_to_json(chat_response['answer'])
        except json.JSONDecodeError:
            raise LLM_JsonDecodeError("GPT model returned invalid JSON response.")

        print(prompt)
        response = {
            "llm": chat_response,
            "annotations": json_anno,
            "prompt": prompt,
            "ocr_name": ocr.name,
        }
        self.results = response
        return response

    def save_results(self, output_path):
        prompt_path = os.path.join(output_path, "prompt.md")
        ocr_image_path = os.path.join(output_path, "ocr_image.png")
        llm_output_path = os.path.join(output_path, "llm_output.json")
        csv_path = os.path.join(output_path, "quotes.csv")

        with open(prompt_path, "w", encoding="utf-8") as fp:
            fp.write(self.results['prompt'])

        with open(llm_output_path, "w", encoding="utf-8") as fp:
            json.dump(self.results['llm'], fp, ensure_ascii=False, indent=4)

        json_quotes: List[dict] = self.results['llm']['answer']
        df = pd.DataFrame(json_quotes['orderlines'])
        df.to_csv(csv_path, index=False)

        annotations = self.results['annotations']
        annotations: List[OCR_Annotation] = [OCR_Annotation(**a) for a in annotations]
        img = self.ocr.show_image(annotations=annotations, pop_window=False)
        # Save OpenCV image to file
        cv2.imwrite(ocr_image_path, img)










