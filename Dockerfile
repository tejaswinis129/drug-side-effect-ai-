FROM python:3.9

WORKDIR /app
COPY . .

RUN pip install numpy

CMD ["python", "inference.py"]