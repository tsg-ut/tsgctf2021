FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive
RUN apt update \
  && apt install -y gcc python3 strace

CMD [ "python3", "./main.py" ]
