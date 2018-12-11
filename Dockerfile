FROM python:alpine3.7

ADD . /prombzex
WORKDIR /prombzex

RUN pip install -r requirements.txt
RUN pip install .

VOLUME ["/config.json", "/outdir"]

CMD ["prombzex", "/config.json"]
