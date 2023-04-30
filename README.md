# CRP Dataflow Demo

gcloud command for building the Dataflex Template
'''
  gcloud dataflow flex-template build gs://BUCKET_NAME/samples/dataflow/templates/streaming-beam-sql.json \
     --image-gcr-path "REGION-docker.pkg.dev/PROJECT_ID/REPOSITORY/dataflow/streaming-beam-sql:latest" \
     --sdk-language "PYTHON" \
     --flex-template-base-image "PYTHON3" \
     --metadata-file "metadata.json" \
     --py-path "." \
     --env "FLEX_TEMPLATE_PYTHON_PY_FILE=streaming_beam.py" \
     --env "FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE=requirements.txt"
'''

'''
  gcloud dataflow flex-template build gs://crp-dataflow-templates/dataflow-demo-job.json \
     --image-gcr-path "australia-southeast1-docker.pkg.dev/gcp-asx-crp-dev/REPOSITORY/dataflow/dataflow-demo:latest" \
     --sdk-language "PYTHON" \
'''