FROM python:3.10-slim-buster
RUN mkdir -p /ohlcv && mkdir -p /ohlcv/tmp

COPY ohlcv/requirements.txt /ohlcv/tmp/requirements.txt
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install -r /ohlcv/tmp/requirements.txt
RUN rm -r /ohlcv/tmp

COPY ohlcv/config.json ohlcv/config.json
COPY .env /ohlcv/.env
COPY ./ohlcv/src /ohlcv/src/
CMD python /ohlcv/src/run.py