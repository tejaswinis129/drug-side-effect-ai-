FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install gradio numpy

EXPOSE 7860

CMD ["python", "app.py"]