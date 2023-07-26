from influxdb_client import InfluxDBClient

# Informations de connexion à InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "your_token"
INFLUXDB_ORG = "your_organization"
INFLUXDB_BUCKET = "your_bucket"

# Fonction pour récupérer les points de données depuis InfluxDB
def get_data():
    # Connexion à InfluxDB
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

    # Requête Flux pour récupérer les points de données
    query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -1h)'
    tables = client.query_api().query(query, org=INFLUXDB_ORG)

    # Parcours des tables de résultats
    for table in tables:
        for record in table.records:
            print(record.values)

    # Fermeture de la connexion à InfluxDB
    client.close()

# Appel de la fonction pour récupérer les données
get_data()


