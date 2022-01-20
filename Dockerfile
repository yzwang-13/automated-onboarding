FROM python:3.10.2-slim-buster
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3", "csv-client.py"]