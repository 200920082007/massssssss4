FROM python:3.9.1-buster

WORKDIR /root/MashaRoBot

COPY . .

RUN pip install -r requirements.txt

CMD ["python3","-m","MashaRoBot"]
FROM python:3.9.1

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /TigerShroff
WORKDIR /TigerShroff
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
