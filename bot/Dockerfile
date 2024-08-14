FROM python:3.11 as builder
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt


WORKDIR /app


COPY . .


CMD ["python3", "bot.py"]
