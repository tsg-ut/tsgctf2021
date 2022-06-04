FROM asuri/ctf-xinetd

RUN rm -rf /etc/xinetd.d/* && \
    apt-get update && \
    apt-get -y upgrade --option=Dpkg::Options::=--force-confdef

RUN apt-get install git autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3 libgdbm-dev libdb-dev -y && \
    git clone https://github.com/rbenv/ruby-build.git && \
    PREFIX=/usr/local ./ruby-build/install.sh && \
    /usr/local/bin/ruby-build 3.0.2 /usr/local

COPY ./src/xinetd.conf /etc/xinetd.d/ctf
COPY ./dist /home/user/app

WORKDIR /home/user/app

RUN chmod 444 /etc/xinetd.d/ctf
