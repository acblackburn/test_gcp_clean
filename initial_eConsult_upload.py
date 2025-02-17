import os
import pandas as pd
import numpy as np
import xlrd
import json
from datetime import datetime
from google.cloud import bigquery

def initial_reason_upload(input_file):
    df = pd.read_excel(input_file, dtype={"Time":"str"})

    df['List_Size'] = df['List_Size'].round().astype(int)
    df['Div_List'] = df['Div_List'].round().astype(int)
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Diverted'] = df['Diverted'].fillna('N')

    project = os.environ.get("BQ_PROJECT")

    bq_client = bigquery.Client(project=project)
    table_id = f"{project}.eConsult.Reason"

    json_file = open("metadata.json")
    data = json.load(json_file)
    metadata = data['Reason']

    # Create BigQuery schema from json metadata
    schema = [bigquery.SchemaField(entry['bq_name'], entry['bq_dtype']) for entry in metadata if entry['bq_name'] != None]

    job_config = bigquery.LoadJobConfig(schema=schema)

    # Load DataFrame in BigQuery
    job = bq_client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )

    job.result()
    json_file.close()

def initial_usage_upload(input_file):
    df = pd.read_excel(input_file)

    df['List_Size'] = df['List_Size'].round().astype(int)

    project = os.environ.get("BQ_PROJECT")

    bq_client = bigquery.Client(project=project)
    table_id = f"{project}.eConsult.Usage"

    json_file = open("metadata.json")
    data = json.load(json_file)
    metadata = data['Usage']

    # Create BigQuery schema from json metadata
    schema = [bigquery.SchemaField(entry['bq_name'], entry['bq_dtype']) for entry in metadata if entry['bq_name'] != None]

    job_config = bigquery.LoadJobConfig(schema=schema)

    # Load DataFrame in BigQuery
    job = bq_client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )

    job.result()
    json_file.close()
