FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir tornado

COPY . .

EXPOSE 8001

CMD ["python", "webserver.py"]
