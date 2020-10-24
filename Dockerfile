FROM python:3.8.3-alpine

ENV PYTHONUNBUFFERED=1 COLUMNS=200 TZ=Asia/Almaty

RUN apk add --no-cache git linux-headers bash python3-dev

RUN rm -rf /src
COPY ./src /src
WORKDIR /src
RUN pip install --upgrade pip && pip install -U -r requirements.txt
ADD . /src/
