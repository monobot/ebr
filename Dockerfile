FROM python:3.6

ENV PYTHON_BURY 1

RUN mkdir /ebury
WORKDIR /ebury

ADD scripts/requirements /ebury/

RUN pip install -r requirements

ADD . /ebury/
