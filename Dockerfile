FROM python:3.8.3-alpine

RUN apk --update add bash

RUN mkdir /app

WORKDIR /app

COPY api.py /app/

COPY requirements.txt /app/

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl http://localhost:9200" ] || exit 1

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl http://localhost/tracking" ] || exit 1

RUN pip install -r requirements.txt


CMD python /app/api.py
