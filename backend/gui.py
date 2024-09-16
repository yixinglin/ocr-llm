import base64
from io import BytesIO
import pandas as pd
import gradio as gr
import requests
import json

def load_config():
    with open('conf/gui.json', 'r') as f:
        config = json.load(f)
    return config

config = load_config()
username = config["ocrllm-api"]["username"]
password = config["ocrllm-api"]["password"]
base_url = config["ocrllm-api"]["url"]

def recognize_text(image):
    # 使用 Tesseract 从图片中提取文本

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    body = {
        "base64_image": img_str,
        "format": "JPG",
        "temperature": 0.7,
        "im_preprocess": True,
        "enable_bbox": False,
    }
    url = f"{base_url}/v1/ocrllm/extract-quote-image/base64/"
    response = requests.post(url, json=body, auth=(username, password)).json()
    answer = response["data"]["llm"]["answer"]
    orderlines = answer["orderlines"]
    df = pd.DataFrame(orderlines)
    return df

# 创建 Gradio 界面
iface = gr.Interface(
    fn=recognize_text,
    title="Text Recognition from Image",
    inputs=gr.Image(type='pil', label="Upload Image"),
    outputs=gr.Dataframe(label="Extracted Text")
)


# 启动应用
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=6998, root_path="/ocrllm-gui")