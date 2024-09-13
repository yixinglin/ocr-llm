

class OCRUtils:
    def __init__(self, image_path, config):
        self.config = config
        self.image_path = image_path

    def to_text(self):
        raise NotImplementedError()

class TesseractOCR(OCRUtils):
    def __init__(self, image_path, config):
        super().__init__(image_path, config)

    def to_text(self):
        pass

    def __str__(self):
        return "Tesseract OCR"

class GoogleVisionOCR(OCRUtils):
    def __init__(self, image_path, config):
        super().__init__(image_path, config)

    def to_text(self):
        pass

    def __str__(self):
        return "Google Vision OCR"