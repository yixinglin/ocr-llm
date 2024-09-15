FROM python:3.10.14-slim

ADD . /code
WORKDIR /code

RUN apt-get update
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install -y tesseract-ocr tesseract-ocr-deu tesseract-ocr-chi-sim tesseract-ocr-chi-tra

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 6995

CMD ["python", "main.py"]