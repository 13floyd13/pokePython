import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client import query_api
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv()

# init client
url = "http://localhost:8086"
token = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
org = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
bucket = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
userName = os.getenv("DOCKER_INFLUXDB_INIT_USERNAME")
password = os.getenv("DOCKER_INFLUXDB_INIT_PASSWORD")
INFLUXDB_HOST = 'localhost'
INFLUXDB_PORT = 8086

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'data_topic'

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

def insert_data():
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for value in range(1):
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", value)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        time.sleep(1)  # separate points by 1 second

def read_data():
    query_api = client.query_api()

    query = """from(bucket: "mybucket")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org=org)
    print(tables)

    mqtt_client = mqtt.Client("pyScript")
    mqtt_client.connect(MQTT_BROKER)

    for table in tables:
        for record in table.records:
            print(record)
            print(record.get_time().isoformat())

            mqtt_client.publish(MQTT_TOPIC, str(record))


if __name__ == "__main__":
    print(token)
    print(bucket)
    print(org)
    print(os.getenv("DOCKER_INFLUXDB_INIT_USERNAME"))
    # insert_data()
    read_data()
