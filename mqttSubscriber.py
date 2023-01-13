#Useful import

import random
# Module for mqtt client
import paho.mqtt.client as mqtt_client


broker = '10.11.6.153'
port = 1883
# On veut recevoir les qrcode
topic = "QRCODE"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'leivan'
password = 'naviel'

#message received from the capteur
msgReceived = ""

#CONNECT
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        #ACK
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#SUBSCRIBE - Receive the message
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        msgReceived = str(msg.payload.decode())
        print(f"Received `{msgReceived}` from `{msg.topic}` topic")
    client.subscribe(topic)
    client.on_message = on_message
#/!\ can't return the message sent by the broker
#return msgReceived

# Retrieve the message from the broker 
def retrieveMsg():
    print("Retrieving msg: " +msgReceived)
    return msgReceived

def run():
    client = connect_mqtt()
    subscribe(client)
    retrieveMsg()
    client.loop_forever()

if __name__ == '__main__':
    run()