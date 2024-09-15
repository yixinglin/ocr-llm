import json
import os.path
from string import Template
from typing import List
import cv2
import pandas as pd
from core.config import config
from core.exceptions import LLM_JsonDecodeError
from lib.llm import SYSTEM_PROMPT_OCR, GPT4oMini
from lib.ocrutils import TesseractOCR, OCR_Annotation
from models.quote import OrderLineItem


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

    def __init__(self, im_preprocess=False, temperature=0.7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt_path = os.path.join("assets", "prompts_de.md")
        self.temperature = temperature
        self.sys_prompt = SYSTEM_PROMPT_OCR
        self.prompt_template = None
        self.api_key = config.openai.api_key
        self.GPT_MODEL = GPT4oMini
        self.results = None
        self.ocr = None
        self.llm = None
        self.im_preprocess = im_preprocess
        self.image = None
        self.initialize()

    def initialize(self):
        with open(self.prompt_path, "r", encoding="utf-8") as fp:
            self.prompt_template = fp.read()

    def get_image(self):
        return self.image

    def save_image(self, output_path):
        if self.image is not None:
            cv2.imwrite(output_path, self.image)

    def run(self, image_path):
        ocr = TesseractOCR(image_path=image_path, lang="deu+eng",
                           preprocessed=self.im_preprocess, thresh_val=120)
        llm = self.GPT_MODEL(api_key=self.api_key, temperature=self.temperature,
                             sys_prompt=self.sys_prompt)
        self.ocr = ocr
        self.llm = llm
        anno = ocr.to_data()

        text = ocr.to_plain_text()
        template = Template(self.prompt_template)
        json_anno = [a.dict() for a in anno]
        prompt = template.substitute(OCR_NAME=ocr.name, OCR_OUTPUT=text)
        chat_response = llm.chat(prompt)
        try:
            chat_response['answer'] = gpt_answer_to_json(chat_response['answer'])
        except json.JSONDecodeError:
            raise LLM_JsonDecodeError("GPT model returned invalid JSON response.")

        # Validate answer
        is_valid = self.validate_answer(chat_response['answer'])
        print(f"Answer is valid: {is_valid}")

        print(prompt)
        response = {
            "llm": chat_response,
            "ocr_name": ocr.name,
            "prompt": prompt,
            "annotations": json_anno,
        }
        self.results = response
        self.image = ocr.image
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


    def validate_answer(self, answer):
        orderlines = answer['orderlines']
        line = {}
        try:
           for line in orderlines:
               item = OrderLineItem(**line)
        except Exception as e:
            raise RuntimeError(f"Invalid answer format: {line} {e}")
        return True










