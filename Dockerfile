FROM python:3.8

WORKDIR /teslamon
COPY . /teslamon

ENV PYTHONUNBUFFERED="true"

RUN pip install -r requirements.txt
RUN mkdir /var/teslamon

CMD ["python", "-u", "teslamon.py"]


