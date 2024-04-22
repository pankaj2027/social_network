FROM python:3.11
ENV PYTHONUNBUFFERED 1

ARG PROJECT_DIR=/social_network

RUN mkdir ${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}
COPY requirements.txt ${PROJECT_DIR}

COPY . ${PROJECT_DIR}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt