FROM node:16.3.0-alpine

COPY dist /root/app
WORKDIR /root/app

RUN apk add tcpdump supervisor curl --no-cache && \
    curl -L https://github.com/Asuri-Team/ctf-xinetd/raw/master/tcpdump.sh -o /usr/local/bin/tcpdump.sh && \
    chmod +x /usr/local/bin/tcpdump.sh && \
    ln -s /usr/bin/tcpdump /usr/sbin/tcpdump && \
    sed -i 's/\*\*\* CENSORED \*\*\*/TSGCTF{You_pR0ved_tHaT_you_knOW_tHe_6451C5_of_JavAsCriP7!_G0_4Nd_s0LvE_Mor3_wE6!}/' app.js && \
    npm install

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]
