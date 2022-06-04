FROM sagemath/sagemath

RUN sudo apt-get update -y && \
    sudo apt-get install git -y && \
    sudo apt-get clean

RUN sage -python -m pip install --upgrade pip && \
    sage -python -m pip install ptrlib

ADD solve.sage /home/sage

ENTRYPOINT ["sage", "/home/sage/solve.sage"]
