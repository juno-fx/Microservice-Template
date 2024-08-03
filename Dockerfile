FROM python:3.12 as base

WORKDIR /app

ENV PYTHONPATH=/app

RUN apt update && apt install -y zip curl git && \
	apt clean -y && \
	apt autoclean -y && \
	apt autoremove --purge -y && \
	rm -rf /var/lib/{apt,cache,log}/ /tmp/* /etc/systemd \

COPY requirements.txt .
RUN pip install uv \
    && uv pip install --system -r requirements.txt \
    && rm -rfv requirements.txt

FROM dev AS test

COPY .coveragerc .coveragerc
COPY dev-requirements.txt .
RUN uv pip install --system -r dev-requirements.txt

COPY tests tests

CMD sh tests/run_tests.sh

FROM dev AS prod


