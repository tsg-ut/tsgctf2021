FROM python:3.7-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN cd /tmp && \
    wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -O ngrok.zip && \
    unzip ngrok.zip && \
    mv ngrok /usr/local/bin && \
    chmod +x /usr/local/bin/ngrok && \
    rm -rf ngrok.zip

COPY ./solver.py /app/solver.py
ENTRYPOINT ["python",  "solver.py"]