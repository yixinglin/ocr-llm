import base64
from io import BytesIO
import pandas as pd
import gradio as gr
import requests
import json


with open("conf/gui.json", 'r', encoding='utf-8') as f:
    conf = json.load(f)
    conf = conf['ocrllm-api']
    DOMAIN = conf['url']
    PASSWD = conf['password']
    USERNAME = conf['username']

print("API Domain:", DOMAIN)

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
    
    url = f"http://{DOMAIN}/v1/ocrllm/extract-quote-image/base64/"
    response = requests.post(url, json=body, auth=(USERNAME, PASSWD)).json()
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

# with gr.Blocks() as iface:
#     gr.Markdown("## Text Recognition from Image")
#     with gr.Row():
#         image = gr.Image(type='pil', label="Upload Image")
#     with gr.Row():
#         output = gr.Dataframe(label="Extracted Text")
#     image.change(recognize_text, inputs=[image], outputs=[output])

# 启动应用
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=6998)