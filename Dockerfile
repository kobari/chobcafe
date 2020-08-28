FROM python:3-slim-buster
ARG APPDIR="/var/www/chobcafe"

RUN mkdir -p ${APPDIR}
WORKDIR ${APPDIR}
COPY requirements.txt ${APPDIR}
RUN pip install -r requirements.txt
