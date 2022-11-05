FROM python:alpine

WORKDIR /app

RUN pip install redis

COPY . .

EXPOSE 3434

CMD [ "python", "main.py" ]