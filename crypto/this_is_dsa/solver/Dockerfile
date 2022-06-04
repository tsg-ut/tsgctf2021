FROM sagemath/sagemath

RUN sudo apt-get update -y && \
    sudo apt-get install git -y && \
    sudo apt-get clean

ARG GITHUB_TOKEN
RUN sage -python -m pip install ptrlib git+https://github.com/tsg-ut/pycryptodome.git

ADD solve.sage /home/sage
ADD decode.py /home/sage

ENTRYPOINT ["sage", "/home/sage/solve.sage"]
