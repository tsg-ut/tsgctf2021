FROM ubuntu:focal

RUN apt-get update && apt-get install -y hashcash python3 python3-pip && pip3 install pwntools
COPY solve.py /solve.py
COPY ans_input.txt /ans_input.txt

ENTRYPOINT ["python3", "/solve.py"]
