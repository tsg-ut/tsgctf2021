FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
        apt-get -y upgrade && \
        apt-get install -y apt-utils && \
        apt-get install -y xinetd iproute2
RUN apt-get install -y qemu-system-x86

RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./build/start.sh /home/user/start.sh
COPY --chown=root:user ./build/run.sh /home/user/run.sh
COPY --chown=root:root ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./deploy/rootfs.cpio /home/user/rootfs.cpio
COPY --chown=root:user ./build/bzImage /home/user/bzImage

WORKDIR /home/user

RUN chmod 555 ./start.sh && \
    chmod 555 ./run.sh && \
    chmod 444 /etc/xinetd.d/ctf

USER user
EXPOSE 25252

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]