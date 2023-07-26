import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'  # Adresse IP ou nom d'hôte de votre broker MQTT
MQTT_TOPIC = 'data_topic'  # Le topic sur lequel vous souhaitez vous abonner

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connecté au broker MQTT')
        client.subscribe(MQTT_TOPIC)
    else:
        print('Échec de la connexion au broker MQTT')

def on_message(client, userdata, msg):
    print(f"Message reçu sur le topic {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
print("Salut")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)
client.loop_forever()
