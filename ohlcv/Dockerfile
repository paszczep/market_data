FROM python:3.10-slim-buster
RUN mkdir -p /ohlcv && mkdir -p /ohlcv/tmp
WORKDIR ohlcv/

COPY ohlcv/requirements.txt /ohlcv/tmp/requirements.txt
RUN apt install libpq-dev python3-dev
RUN pip install -r /ohlcv/tmp/requirements.txt
RUN rm -r /ohlcv/tmp

COPY config.json config.json
COPY .env /ohlcv/.env
COPY ./ohlcv/src /ohlcv/src/
CMD python /ohlcv/src/run.py