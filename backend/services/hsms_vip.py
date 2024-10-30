import asyncio

import aiohttp
import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageFile

from crud.hsms_vip import HsmsVipCRUD
import os

from lib.cnn import FeatureExtractor
from utils.http import encode_url
from utils.imutils import faiss_search
from utils.ioutils import file_to_md5
from core.config import config

vip_service_config = config.vip_service

DOMAIN = vip_service_config.domain  # 下载图片的站点域名
VIP_ROOT = vip_service_config.root       # VIP图片下载目录

class VipProductSearchService:
    def __init__(self):
        self.crud = HsmsVipCRUD()
        self.csv_path = f"{VIP_ROOT}/product_images.csv"
        self.image_dir = f"{VIP_ROOT}/product_images"
        self.feature_dir = f"{VIP_ROOT}/product_features"
        self.checkpoint_dir = f"{VIP_ROOT}/checkpoints"
        self.checkpoint_down_url = f"https://download.pytorch.org/models/resnet50-0676ba61.pth"
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.feature_dir, exist_ok=True)
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    async def fetch_vip_product_images(self):
        product_list = await self.crud.query_all_products()
        image_list = []
        for product in product_list:
            if product.deleted:
                continue
            images = product.images
            if images is not None and images[0] == '/':
                for path in images.split(','):
                    md5 = file_to_md5(path.encode('utf-8'))
                    image_url = f"https://{DOMAIN}{path}"
                    image_url = encode_url(image_url)
                    item = dict(id=product.id, name=product.name,
                                image_path=path, image_url=image_url, article_number=product.article_number, md5=md5)
                    image_list.append(item)

        df = pd.DataFrame(image_list)
        csv_path = f"{VIP_ROOT}/product_images.csv"
        df.to_csv(csv_path, index=False)

        for item in image_list:
            image_path = f"{self.image_dir}/{item['md5']}.jpg"
            if os.path.exists(image_path):
                print(f"{image_path} exists, skip")
                continue
            image_url = item['image_url']
            print(image_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        # Sleep to avoid too many requests
                        await asyncio.sleep(0.3)

            with open(image_path, "wb") as f:
                f.write(content)

        return {
            "data": csv_path,
            "image_dir": self.image_dir,
            "count": len(image_list),
        }

    def __get_feature_extractor(self):
        cp_path = f'{self.checkpoint_dir}/resnet50-0676ba61.pth'
        if not os.path.exists(cp_path):
            print(f"Downloading checkpoint from {self.checkpoint_down_url}")
            resp = requests.get(self.checkpoint_down_url, allow_redirects=True)
            with open(cp_path, 'wb') as f:
                f.write(resp.content)
            print(f"Checkpoint downloaded to {cp_path}")
        fe = FeatureExtractor.from_checkpoint(cp_path)
        return fe

    def extract_vip_product_features(self):
        data = pd.read_csv(f"{VIP_ROOT}/product_images.csv")
        fe = self.__get_feature_extractor()
        for i, row in data.iterrows():
            image_path = f"{self.image_dir}/{row['md5']}.jpg"
            feature_path = f"{self.feature_dir}/{row['md5']}.npy"
            if os.path.exists(feature_path):
                print(f"{feature_path} exists, skip")
                continue
            img = Image.open(image_path).convert('RGB')
            features = fe.extract(img)
            with open(feature_path, "wb") as f:
                np.save(f, features)
                print(f"Features (i) saved for {image_path}")
        print("All features extracted")


    def search_products_by_image(self, image: ImageFile, k=5):
        data = pd.read_csv(f"{VIP_ROOT}/product_images.csv")
        product_list = data.to_dict('records')
        feature_list = []
        for product in product_list:
            md5 = product['md5']
            feature_path = f"{self.feature_dir}/{md5}.npy"
            feature = np.load(feature_path)
            feature_list.append(feature)
        feature_list = np.array(feature_list)
        img = image
        fe = self.__get_feature_extractor()
        query_feature = fe.extract(img)

        distances, indices = faiss_search(query_feature, feature_list, k=k)

        founded_product_list = [product_list[i] for i in indices]
        df = pd.DataFrame(founded_product_list)
        # Add distance column
        df['simularity'] = distances
        df['simularity'] = df['simularity'].apply(lambda x: round(x, 4))

        # Sort by simularity
        df = df.sort_values('simularity', ascending=False)
        df = df.drop_duplicates(subset='id', keep='first')

        image_url_list = df['image_url'].tolist()  # [im['imageUrl'] for im in founded_product_list]
        # columns=['id', 'articleNumber', 'name', "imageUrl"]
        df = df[['id', 'article_number', "simularity", 'name', ]]
        return df, image_url_list