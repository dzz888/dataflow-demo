#
# Licensed to ASX under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
#

"""A GCS Text to BQ workflow."""

# crp-poc:
#   name: gcs_text_to_bq
#   description: takes csv data file from gcs bucket and load it to BigQuery table.
#   multifile: false
#   pipeline_options: --output dataset_name.table_name
#   categories:
#     - dataflow flex template
#   tags:
#     - dataflow
#     - flex template

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.io.gcp.bigquery import WriteToBigQuery

from google.cloud import bigquery

def run(argv=None, save_main_session=True):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://crp-inbound-data-demo/20220908/CASH_RATES_20220908.csv',
        help='Input file to ingest.')
    parser.add_argument('--project',
        dest='project',
        default='gcp-asx-crp-dev',
        help='GCP project ID.')      
    parser.add_argument(
        '--output',
        dest='output',
        default="CASH_RATES",
        required=False,
        help='Output BigQuery table to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = "gcp-asx-crp-dev.demo_dataset.CASH_RATES"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("CASH", "STRING"),
            bigquery.SchemaField("RATE", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = known_args.input

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()