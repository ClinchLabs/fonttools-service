FROM python:2

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9097

CMD [ "python", "server.py" ]
