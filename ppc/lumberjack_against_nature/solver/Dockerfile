FROM python:3.9.7-alpine

RUN apk add build-base && \
    python -m pip install ptrlib mpmath

ADD solver.py /tmp

ENTRYPOINT ["python", "/tmp/solver.py"]
