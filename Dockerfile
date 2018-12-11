FROM python:alpine3.7

ADD requirements.txt /
RUN pip install prombzex
RUN pip install -r requirements.txt

VOLUME ["/config.json", "/outdir"]

CMD ["prombzex", "/config.json"]
