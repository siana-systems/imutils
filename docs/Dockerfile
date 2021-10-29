FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-pip python3-sphinx libgl1-mesa-dev libglib2.0-0 libsm6 libxrender1 libxext6

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /src