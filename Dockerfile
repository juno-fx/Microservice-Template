FROM python:3.12-alpine as dev

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN apk add zip curl git && \
    pip install uv && \
    uv pip install --system -r requirements.txt --no-cache && \
    rm -rfv requirements.txt

COPY src src

CMD uvicorn src:app --host 0.0.0.0 --reload

FROM dev AS test

COPY .coveragerc .coveragerc
COPY dev-requirements.txt .
RUN uv pip install --system -r dev-requirements.txt --no-cache

COPY tests tests

CMD sh tests/run_tests.sh

FROM dev AS prod

# ditch the reload and increase workers
CMD uvicorn --workers 2 src:app --host 0.0.0.0
