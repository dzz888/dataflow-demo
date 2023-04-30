#
# Licensed to ASX under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
#

"""A on-prem files to gcp bucket."""

# pytype: skip-file

# beam-playground:
#   name: onprem_files_to_gcp
#   description: upload on-prem files to gcp bucket via on-prem file share
#   multifile: false
#   pipeline_options:
#   categories:
#     - dataflow flex template
#   complexity: MEDIUM
#   tags:
#     - dataflow
#     - flex template

import argparse
import logging
import re
import getpass

import os
import io
import tempfile
import apache_beam as beam
from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure
from apache_beam.io.filesystems import FileSystems
from google.cloud import storage

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_path', dest='source_path',
                        default='CASH_RATES_20220908.csv',
                        help='Source path of file to download from the Windows network share folder.')
    parser.add_argument('--server_name', dest='server_name',
                        default='DFSMDM202',
                        help='Windows network share folder URL.')
    parser.add_argument('--username', dest='username',
                        default='danny.zhang@asx.com.au',
                        help='Username for Windows network share folder.')
    parser.add_argument('--password', dest='password', required=0,
                        help='Password for Windows network share folder.')
    parser.add_argument('--bucket_name', dest='bucket_name',
                        default='crp-inbound-data-demo',
                        help='Google Cloud Storage bucket name.')
    parser.add_argument('--dest_blob_name ', dest='dest_blob_name ',
                        default='CASH_RATES_20220908-02.csv',
                        help='Destination path of file to upload to the Google Cloud Storage bucket.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    share_name = 'outbound'

    # GCP credentials
    project_id = 'gcp-asx-crp-dev'

    # Prompt the user for a password without echoing the characters
    password = getpass.getpass(f"Enter your password to access files on {known_args.server_name}: ")

    # Create SMB connection
    conn = SMBConnection(known_args.username, password, 'dataflow', 'remote', use_ntlm_v2=True, is_direct_tcp=True)
    conn.connect(known_args.server_name, 445)

    # Get list of files in shared folder
    file_list = conn.listPath(share_name, '/')

    # Create GCP client
    client = storage.Client(project=project_id)

    # Get GCP bucket
    bucket = client.get_bucket(known_args.bucket_name)

    # Upload files to GCP bucket
    for file in file_list:
        if file.isDirectory:
            continue
        file_name = os.path.basename(file.filename)
        file_obj = io.BytesIO()
        conn.retrieveFile(share_name, file.filename, file_obj)
        file_contents = file_obj.getvalue()  
        blob = bucket.blob(file_name)
        blob.upload_from_string(file_contents)

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()