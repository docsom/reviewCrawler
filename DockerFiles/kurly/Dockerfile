FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y sudo
RUN sudo apt install -y software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN sudo apt install -y python3.9

RUN sudo apt install -y python3-pip
RUN sudo apt-get install -y python-lxml
RUN sudo apt-get install -y python3-bs4
RUN sudo apt-get install -y python3-pandas
RUN pip3 install requests

RUN cd home
RUN mkdir crawler
RUN cd crawler
