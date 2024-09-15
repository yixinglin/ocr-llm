import sys
from typing import Tuple, List
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageFont, ImageDraw
from matplotlib import pyplot as plt
from pydantic import BaseModel

if sys.platform == "win32":
    # Arial
    FONT_PATH = "C:/Windows/Fonts/Arial.ttf"
elif sys.platform == "linux":
    # Noto
    FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

class OCR_Annotation(BaseModel):
    text: str # The text detected by OCR
    bbox: Tuple[int, int, int, int]  # (x, y, width, height). Note that x and y are the top-left corner of the bbox.
    confidence: int # Confidence score, 0-100

class OCRUtils:
    def __init__(self, image_path, lang, preprocessed, name:str, *args, **kwargs):
        self.image_path: str = image_path
        self.lang: str = lang
        self.preprocessed: bool = preprocessed
        self.name = name

    def to_data(self) -> List[OCR_Annotation]:
        raise NotImplementedError()

    def to_plain_text(self, annotations: List[OCR_Annotation]) -> str:
        raise NotImplementedError()

    def to_text(self, annotations: List[OCR_Annotation]) -> str:
        content = ""
        for item in annotations:
            text, bbox, confidence = item.text, item.bbox, item.confidence
            content += f"[\"{text}\", {bbox}, \"{confidence}%\"]\n"
        return content

    def show_image(self, annotations: List[OCR_Annotation], display_text=True, pop_window=True):
        if not self.preprocessed:
            image = cv2.imread(self.image_path)
        else:
            preprocessed_image = self.preprocess_image(self.image_path)
            image = cv2.cvtColor(preprocessed_image, cv2.COLOR_GRAY2BGR)

        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype(FONT_PATH, 20)
        # Traverse the pytesseract results and get the coordinates and text of each text
        for anno in annotations:
            (x, y, w, h) = anno.bbox
            text = f"{anno.text}: {anno.confidence}"
            # Draw the bounding box of the text
            draw.rectangle([x, y, x + w, y + h], outline=(0, 255, 0), width=2)
            if display_text:
                draw.text((x, y - 30), text, font=font, fill=(255, 0, 0))

        # Convert the Pillow image back to OpenCV image
        image_with_text = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Show the image with text
        if pop_window:
            plt.imshow(image_with_text)
            plt.show()
        return image_with_text

    def preprocess_image(self, image_path, thresh_val=127):
        """
        对图像进行预处理，返回处理后的二值化图像。

        Args:
            image_path (str): 原始图像的路径。

        Returns:
            numpy.ndarray: 处理后的二值化图像。
        """
        # 读取图像
        image = cv2.imread(image_path)

        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 使用高斯模糊去除噪声
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 二值化处理
        _, binary_image =cv2.threshold(blurred, thresh_val, 255, cv2.THRESH_BINARY)

        # 可选步骤：进行形态学操作，如膨胀和腐蚀，进一步消除噪声
        # kernel = np.ones((3, 3), np.uint8)
        # binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

        # 如果图片方向不正，可以尝试自动旋转校正（可选）
        # edges = cv2.Canny(binary_image, 50, 150)
        # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=5)
        # if lines is not None:
        #     angles = []
        #     for line in lines:
        #         x1, y1, x2, y2 = line[0]
        #         angle = np.arctan2(y2 - y1, x2 - x1)
        #         angles.append(angle)
        #     median_angle = np.median(angles)
        #     angle_degree = np.degrees(median_angle)
        #
        #     # 旋转图片
        #     (h, w) = binary_image.shape[:2]
        #     center = (w // 2, h // 2)
        #     M = cv2.getRotationMatrix2D(center, angle_degree, 1.0)
        #     binary_image = cv2.warpAffine(binary_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return binary_image


# pip install pytesseract
class TesseractOCR(OCRUtils):
    def __init__(self, image_path, lang="deu", preprocessed=False, thresh_val=127, *args, **kwargs):
        super().__init__(image_path, lang, preprocessed, name="Tesseract", *args, **kwargs)
        self.conf = '--psm 6 --oem 1'
        self.image = None
        self.thresh_val = thresh_val

    def to_data(self) -> List[OCR_Annotation]:
        """
        Note: 此数据格式会干扰ChatGPT的输出，因此暂时不使用。
        :return:
        """
        if not self.preprocessed:
            image = cv2.imread(self.image_path)
        else:
            preprocessed_image = self.preprocess_image(self.image_path, self.thresh_val)
            image = preprocessed_image

        raw_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=self.conf)
        data = []
        for i in range(len(raw_data['text'])):
            confidence = round(float(raw_data['conf'][i]))
            text = raw_data['text'][i]
            if text.strip() != "":
                data.append(OCR_Annotation(
                    text=text,
                    bbox=(raw_data['left'][i], raw_data['top'][i], raw_data['width'][i], raw_data['height'][i]),
                    confidence=int(confidence),
                    ))
        self.image = image
        return data

    def to_plain_text(self) -> str:
        """
        Note: 此数据格式和ChatGPT配合使用不错
        :return:
        """
        if not self.preprocessed:
            image = cv2.imread(self.image_path)
        else:
            preprocessed_image = self.preprocess_image(self.image_path, self.thresh_val)
            image = preprocessed_image
        text = pytesseract.image_to_string(image, lang=self.lang, config=self.conf)
        self.image = image
        return text

    def __str__(self):
        return "Tesseract OCR"

# pip install easyocr
class EasyOCR(OCRUtils):
    def __init__(self, image_path, gpu=False, preprocessed=False, *args, **kwargs):
        super().__init__(image_path, "", preprocessed, name="EasyOCR", *args, **kwargs)
        self.reader = easyocr.Reader(['de', 'en'], gpu=gpu)

    def to_data(self) -> List[OCR_Annotation]:
        if not self.preprocessed:
            image = cv2.imread(self.image_path)
        else:
            preprocessed_image = self.preprocess_image(self.image_path)
            image = cv2.cvtColor(preprocessed_image, cv2.COLOR_GRAY2BGR)

        results = self.reader.readtext(image)
        annotations = []
        for result in results:
            bbox, text, confidence = result
            # Convert bbox (four vertices) to left, top, width, height format
            x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
            x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))

            width = x_max - x_min
            height = y_max - y_min

            # Convert confidence to 0-100 integer
            confidence = int(confidence * 100)

            # Create OCR_Annotation object and append to list
            annotation = OCR_Annotation(text=text, bbox=(x_min, y_min, width, height), confidence=confidence)
            annotations.append(annotation)

        return annotations

    def __str__(self):
        return "Easy OCR"

def test_pytesseract():
    image_path = r"G:\hansagt\ocr-llm\backend\temp\quote\4.jpg"
    preprocessed = False
    ocr = TesseractOCR(image_path, lang="deu", preprocessed=preprocessed)

    if not preprocessed:
        image = cv2.imread(image_path)
    else:
        image = ocr.preprocess_image(image_path, thresh_val=127)

    # Show preprocessed image
    plt.imshow(image, cmap='gray')
    plt.show()

    anno = ocr.to_data()
    ocr.show_image(anno)
    text = ocr.to_text(anno)
    print(text)

def test_easyocr():
    image_path = r"G:\hansagt\ocr-llm\backend\temp\quote\4.jpg"
    preprocessed = False
    ocr = EasyOCR(image_path, gpu=True, preprocessed=preprocessed)

    if not preprocessed:
        image = cv2.imread(image_path)
    else:
        image = ocr.preprocess_image(image_path)

    plt.imshow(image, cmap='gray')
    plt.show()

    anno = ocr.to_data()
    print(anno)
    ocr.show_image(anno)

    text = ocr.to_text(anno)
    print(text)


if __name__ == "__main__":
    test_pytesseract()
    # test_easyocr()