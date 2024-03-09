# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from google.cloud import bigquery
from datetime import datetime
import os



app = Flask(__name__)

# Configura la instancia de cliente de BigQuery
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ibust/OneDrive/Escritorio/IKER MASTER/Website/pythonWebApp/pythonWebApp/secrets/nfcbigquery-909170f97741.json"
clientbq = bigquery.Client()

# Nombre del dataset y la tabla en BigQuery
dataset_name = 'NFCdataset'
table_name = 'NFCregister'

# Comprueba si el dataset existe, y si no, créalo
def create_dataset(dataset_name):
    
    dataset_ref = clientbq.dataset(dataset_name)
    try:
        clientbq.get_dataset(dataset_ref)
    except Exception as e:
        dataset = bigquery.Dataset(dataset_ref)
        clientbq.create_dataset(dataset)

# Comprueba si la tabla existe, y si no, créala
def create_table(table_name, dataset_name):
    
    dataset_ref = clientbq.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)
    try:
        clientbq.get_table(table_ref)
    except Exception as e:
        schema = [
            bigquery.SchemaField('client', 'STRING'),
            bigquery.SchemaField('destination_id', 'STRING'),
            bigquery.SchemaField('visit_date', 'DATE'),
            bigquery.SchemaField('visit_time', 'TIME'),
        ]
        table = bigquery.Table(table_ref, schema=schema)
        clientbq.create_table(table)

create_dataset(dataset_name)
create_table(table_name, dataset_name)
dataset_ref = clientbq.dataset(dataset_name)
table_ref = dataset_ref.table(table_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<client>/')
def client_home(client):
    if request.path == '/favicon.ico':
        return '', 204
    return render_template(f'clients/{client}.html', client=client)

@app.route('/<client>/destination/<destination_id>/')
def destination(client, destination_id):
    # Registra la visita en BigQuery
    visit_date = datetime.now().strftime('%Y-%m-%d')  # Formato YYYY-MM-DD
    visit_time = datetime.now().strftime('%H:%M:%S')

    row = {
        'client': client,
        'destination_id': destination_id,
        'visit_date': visit_date,
        'visit_time': visit_time,
    }

    # Inserta la fila en la tabla de BigQuery
    table = clientbq.get_table(table_ref)
    
    print("Antes de insertar en BigQuery")
    errors = clientbq.insert_rows(table, [row])
    print("Despues de insertar en BigQuery")

    if errors:
        print(f"Error al insertar en BigQuery: {errors}")

    # Resto de la lógica para renderizar la plantilla
    template_path = f'clients/destinations{client.capitalize()}/destination{destination_id}.html'
    return render_template(template_path, client=client, destination_id=destination_id)

if __name__ == '__main__':
    app.run(debug=True)
