FROM node:16.3.0-alpine

COPY dist /root/app
WORKDIR /root/app

RUN apk add tcpdump supervisor curl --no-cache && \
    curl -L https://github.com/Asuri-Team/ctf-xinetd/raw/master/tcpdump.sh -o /usr/local/bin/tcpdump.sh && \
    chmod +x /usr/local/bin/tcpdump.sh && \
    ln -s /usr/bin/tcpdump /usr/sbin/tcpdump && \
    npm install

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]
