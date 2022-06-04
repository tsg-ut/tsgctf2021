FROM ubuntu:20.04

RUN apt update && \
        apt -y upgrade && \
        apt install -y xinetd iproute2

RUN groupadd -r user && useradd -r -g user user

COPY ./dist/start.sh /home/user/start.sh
COPY ./build/ctf.conf /etc/xinetd.d/ctf
COPY ./build/flag /home/user/flag
COPY ./dist/coffee /home/user/coffee

WORKDIR /home/user

RUN chmod 444 ./flag && \
    chmod 555 ./coffee && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

RUN mv flag flag-$(md5sum flag | awk '{print $1}')
RUN chown -R root:user /home/user

USER user
EXPOSE 30001

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
