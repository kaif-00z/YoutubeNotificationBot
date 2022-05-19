FROM python:3.9.7-slim-buster
COPY . /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git wget pv jq wget python3-dev ffmpeg
RUN pip3 install -r requirements.txt
CMD ["bash", "run.sh"]
