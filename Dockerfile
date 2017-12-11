FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir tornado

COPY . .

CMD ["python", "webserver.py"]
