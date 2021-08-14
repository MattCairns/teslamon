FROM python:3.8

WORKDIR /teslamon
COPY . /teslamon

RUN pip install -r requirements.txt
RUN mkdir /var/teslamon

ENTRYPOINT ["python", "teslamon.py"]


