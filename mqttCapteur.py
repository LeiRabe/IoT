import random
import time
from datetime import date
# Module for mqtt client
from paho.mqtt import client as mqtt_client

today = date.today()

broker = '10.11.6.153'
port = 1883
# On veut envoyer le qrcode
topic = "QRCODE"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'leivan'
password = 'naviel'

#CONNECT
def connect_mqtt():
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

# Imitate the QRcode captor 
# by generating the message to send to the broker
def generateMsg():
    msg = ""
    qrCode = random.choice([4545445484,454544,400512])
    dateAccess = today.strftime("%Y/%m/%d")
    idPortique = random.randint(1,6)
    msg = str(qrCode)+","+str(dateAccess)+","+str(idPortique)
    return msg

# PUBLISH to the broker
def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        # Simulate existing and none existing qrcode/message to send
        if(msg_count%2==0):
            msg = generateMsg()
        else:
            msg = f"454544,2022-12-01,5"
        
        # publish the generated message and it topic
        result = client.publish(topic, msg)
        # result: [0: true, 1: false]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()