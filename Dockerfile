FROM python:3.12-bookworm

ARG DATA_DIR=./data/
ARG LOG_DIR=./logs/

WORKDIR "/opt/issyou-detector/"

COPY "./requirements.txt" "./requirements.txt"
RUN python -m pip install --no-cache-dir -r "./requirements.txt"

COPY "./issyou_detector/" "./issyou_detector/"
COPY "./issyou-detector.py" "./"

RUN ln --symbolic "$(realpath ${DATA_DIR})" "/var/lib/issyou-detector"
RUN ln --symbolic "$(realpath ${LOG_DIR})" "/var/log/issyou-detector"

CMD [ "python", "./issyou-detector.py" ]
