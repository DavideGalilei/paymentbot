FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

RUN apk add gcc python3-dev jpeg-dev zlib-dev jpeg-dev zlib-dev libjpeg build-base linux-headers

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -U wheel pip
RUN pip install -r requirements.txt
COPY . /code/

ENTRYPOINT [ "python3", "main.py" ]
