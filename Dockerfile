FROM python:alpine3.7

RUN pip install -r requirements.txt ; pip install prombzex

VOLUME ["/config.json", "/outdir"]

CMD ["prombzex /config.json"]
