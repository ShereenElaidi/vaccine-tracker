FROM ubuntu 
WORKDIR /

RUN apt-get update || : && apt-get install python3 -y
RUN apt-get update || : && apt-get install python3-pip -y

COPY requirements.txt ./

RUN python3 -m pip install -r ./requirements.txt

COPY . . 

ENV PORT=56666
EXPOSE 56666

CMD ["python3", "main.py"]