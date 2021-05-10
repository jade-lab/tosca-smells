FROM ubuntu:20.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN mkdir /shared

WORKDIR /app
COPY large_class.csv .
COPY lazy_class.csv .
COPY long_method.csv .
COPY screen.py .
COPY validate.py .

RUN pip install pandas pyyaml requests

CMD [ "python", "validate.py", "/shared" ]
