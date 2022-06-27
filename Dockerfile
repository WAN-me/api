FROM python:3.9-slim

EXPOSE 3000

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN mkdir /databases/

RUN pip install -r requirements.txt


CMD [ "python", "./main.py"]