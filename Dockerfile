FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR C:\\Users\belus\Kwork\vpnbot-master

COPY requirements.txt C:\\Users\belus\Kwork\vpnbot-master
RUN pip install -r C:\\Users\belus\Kwork\vpnbot-master\requirements.txt
COPY . C:\\Users\belus\Kwork\vpnbot-master
