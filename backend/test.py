from services.OcrGptService import TesseractOCR_GPT_Service

if __name__ == '__main__':
    image_path = r"G:\hansagt\ocr-llm\backend\temp\original\7.jpg"
    svc = TesseractOCR_GPT_Service(temperature=0.7)
    response = svc.run(image_path=image_path)
    print(response)
    svc.save_results("temp")
    print("Done")