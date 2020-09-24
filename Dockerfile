FROM python:3
ARG APP_USER="chobcafe"
ARG APPDIR="/var/www/chobcafe"

# Create a non-root user for containers to run as
RUN apt-get update && useradd -rM -s /bin/bash ${APP_USER}

RUN mkdir -p ${APPDIR}
WORKDIR ${APPDIR}
COPY requirements.txt ${APPDIR}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all files
COPY ./apps ${APPDIR}

# uWSGI will listen on this port
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=chobcafe.settings

# Change to a non-root user
#USER ${APP_USER}:${APP_USER}
USER ${APP_USER}

CMD ["uwsgi", "--ini", "/var/www/chobcafe/uwsgi.ini"]
