FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive
RUN apt update \
  && apt install -y gcc build-essential

CMD [ "make", "-B" ]
