

## Depandancies
- Tesseract-OCR
- OpenCV
- Pytesseract
- OpenAI
- FastAPI
- MongoDB

```shell
sudo apt install tesseract-ocr -y 
sudo apt install tesseract-ocr-deu -y  # for German language
sudo apt install tesseract-ocr-chi-sim -y  # for Chinese language
sudo apt install tesseract-ocr-chi-tra -y  # for Chinese language
 
pip install tesseract
pip install opencv-python
pip install pytesseract
pip install openai
pip install fastapi


docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest


pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```