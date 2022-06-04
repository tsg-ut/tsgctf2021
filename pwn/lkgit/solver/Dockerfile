FROM ubuntu:latest

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y python2 curl
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN python2 get-pip.py

RUN python2 -m pip install pwntools pathlib2

COPY exploit.py /exploit.py
COPY exploit.gz.b64 /exploit.gz.b64

ENTRYPOINT ["python2", "/exploit.py"]
