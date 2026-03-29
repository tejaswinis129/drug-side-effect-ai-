FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install gradio numpy huggingface_hub==0.19.4

EXPOSE 7860

CMD ["python", "app.py"]