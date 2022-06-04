FROM alpine:3

WORKDIR /home/user

RUN apk --no-cache add curl
COPY ./result/kls_symbol.rgb /home/user/image.rgb
COPY ./solve.sh /home/user/solve.sh

RUN chmod 755 ./solve.sh

CMD [ "./solve.sh" ]
