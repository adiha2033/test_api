FROM docker.io/library/python:3.8.3-alpine

RUN mkdir /app

WORKDIR /app

COPY ./api /app/

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl http://localhost:9200" ]

RUN pip install -r ./requirements.txt

RUN python /app/api.py
