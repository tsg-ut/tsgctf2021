FROM ubuntu:20.04

RUN apt update && \
        apt -y upgrade && \
        apt install -y xinetd iproute2

RUN groupadd -r user && useradd -r -g user user

COPY ./build/start.sh /home/user/start.sh
COPY ./build/ctf.conf /etc/xinetd.d/ctf
COPY ./build/flag /home/user/flag
COPY ./dist/chall /home/user/chall

WORKDIR /home/user

RUN chmod 444 ./flag && \
    chmod 555 ./chall && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

RUN chown -R root:user /home/user

USER user
EXPOSE 30007

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
