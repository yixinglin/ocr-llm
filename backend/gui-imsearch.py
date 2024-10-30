import io
import json
import os

import pandas as pd
import requests
import gradio as gr
from PIL import Image

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

with open("conf/gui.json", 'r', encoding='utf-8') as f:
    conf = json.load(f)
    conf = conf['ocrllm-api']
    DOMAIN = conf['url']
    PASSWD = conf['password']
    USERNAME = conf['username']

print("API Domain:", DOMAIN)

def search_products(image: Image):
    url = f"http://{DOMAIN}/v1/imsearch/upload/"
    # Convert PIL Image to bytes
    im_io = io.BytesIO()
    image.save(im_io, format='JPEG')
    im_data = im_io.getvalue()
    ans = requests.post(url, auth=(USERNAME, PASSWD), files={"image": im_data})
    data = ans.json()
    products = data['data']['products']
    df = pd.DataFrame.from_dict(products)
    image_url_list = df['image_url'].tolist()
    df = df.drop(columns=['image_url'])
    return df, image_url_list



# 创建 Gradio 界面
iface = gr.Interface(
    fn=search_products,
    title="Search Products by Image",
    inputs=gr.Image(type='pil', label="Upload Image"),
    outputs=[gr.Dataframe(label="Extracted Text"),
             gr.Gallery(label="Product Images")]
)


# 启动应用
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=6999, root_path="/im-search-gui")