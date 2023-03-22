FROM python:3.8.10
ARG APP_HOME=/app
ENV PYTHONUNBUFFERED 1

# Update
RUN echo "[+] Update..........................................................."
RUN  sed -i s@/deb.debian.org/@/mirrors.cloud.tencent.com/@g /etc/apt/sources.list && \
     sed -i s/security.debian.org/mirrors.cloud.tencent.com/g /etc/apt/sources.list && \
     ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
     echo 'Asia/Shanghai' >/etc/timezone
RUN  apt-get clean all && \
     apt-get update -y && \
     apt-get upgrade -y

# Create app home
RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

# Install dependencies
RUN echo "[+] Install dependencies............................................."
COPY . .
RUN cp ./app/config/settings.py.bak ./app/config/settings.py
RUN chmod +x ./install.sh
RUN chmod +x ./run.sh
RUN ["/bin/bash", "./install.sh"]

# Start
EXPOSE 8000
CMD ["/bin/bash", "run.sh"]
