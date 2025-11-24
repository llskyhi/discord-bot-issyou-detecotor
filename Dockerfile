FROM python:3.12-bookworm

ARG DATA_DIR=./data/
ARG LOG_DIR=./logs/

WORKDIR "/opt/issyou-detector/"

COPY "./requirements.txt" "./requirements.txt"
RUN python -m pip install --no-cache-dir -r "./requirements.txt"

COPY "./issyou_detector/" "./issyou_detector/"
COPY "./issyou-detector.py" "./"

RUN mkdir -p "/var/lib/issyou-detector"
RUN ln --symbolic "/var/lib/issyou-detector" "$(realpath ${DATA_DIR})"
RUN mkdir -p "/var/log/issyou-detector"
RUN ln --symbolic "/var/log/issyou-detector" "$(realpath ${LOG_DIR})"

CMD [ "python", "./issyou-detector.py" ]
