FROM python:3.9-slim-buster

ENV WORK_DIRECTORY /dataflow-demo
RUN mkdir -p $(WORK_DIRECTORY)

WORKDIR(WORK_DIRECTORY)

ARG PYTHON_FILE_NAME=main

copy . ${WORK_DIRECTORY}/

ENV REQUIREMENTS_FILE="${WORK_DIRECTORY}/requirements.txt"
ENV PY_FILE="${WORK_DIRECTORY}/${PYTHONFILENAME}.py"

RUN python3 --version

#minimise the docker image size with --no-cache-dir
#then download the packages into /tmp
RUN pip install --no-cache-dir -r $REQUIREMENTS_FILE \
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $REQUIREMENTS_FILE

    