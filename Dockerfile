FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ENV WORK_DIRECTORY /app
WORKDIR ${WORK_DIRECTORY}
RUN mkdir -p "${WORK_DIRECTORY}"

ARG PYTHON_FILE_NAME=pipeline_helloWorld.py

# only copy selected files
copy pipeline_helloWorld.py ${WORK_DIRECTORY}/
copy requirements.txt ${WORK_DIRECTORY}/
copy ${PYTHON_FILE_NAME} ${WORK_DIRECTORY}/

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORK_DIRECTORY}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORK_DIRECTORY}/${PYTHON_FILE_NAME}"

#minimise the docker image size with --no-cache-dir
#install required packages
RUN pip install --no-cache-dir -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE \
    # Download the requirements to speed up launching the Dataflow job.
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE