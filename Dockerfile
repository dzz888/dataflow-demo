FROM images-proxy-group.pkg.asx.com.au/python:3.9-slim-buster

ENV WORK_DIRECTORY /dataflow-demo
WORKDIR ${WORK_DIRECTORY}
RUN mkdir -p "${WORK_DIRECTORY}"

ARG PYTHON_FILE_NAME=main

copy . ${WORK_DIRECTORY}/

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORK_DIRECTORY}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORK_DIRECTORY}/${PYTHON_FILE_NAME}.py"

RUN python3 --version

#minimise the docker image size with --no-cache-dir
#install required packages
RUN pip install --no-cache-dir -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE \
    # Download the requirements to speed up launching the Dataflow job.
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE