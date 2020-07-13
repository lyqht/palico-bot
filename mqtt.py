from settings import MQTT_IP, MQTT_PORT
from settings import TELEGRAM_TEST_TELEGRAM_CHAT_ID
import paho.mqtt.client as mqtt
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print ("Connection OK!")
    else:
        print("Bad connection, Returned Code: ", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))
    
def mqtt_on_msg_callback(client, userdata, msg):
    global mqtt_client
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("=============================")
    
    # check topic
    topic=msg.topic
    sensor_type, house_id, room_type = topic.split("/")
    print("Sensor Type: {}, House_ID: {}, Room_Type: {}".format(sensor_type, house_id, room_type))
    if sensor_type == "bps" or sensor_type == "mlx":
        print("Activity Levels MQTT Message received")
        mqtt_client.send_message("Current Room that the user is in: " + room_type)
        
    elif sensor_type == "Fall":
        print("Fall Detection MQTT Message received")
        # TODO
    print("=============================")

class MQTTClientForTelegramBot:
    def __init__(self, broker, port):

        client = mqtt.Client("palico")
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = mqtt_on_msg_callback
        print("connecting to broker, ", broker)
        client.connect(broker, port)
        self.client = client
        self.bot = None

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Subscribed to topic:", topic)
        
    def send_message(self, msg):
        assert self.bot != None
        print("Sending message")
        self.bot.send_message(chat_id=TELEGRAM_TEST_TELEGRAM_CHAT_ID, text=msg)
        
    
mqtt_client = MQTTClientForTelegramBot(MQTT_IP, int(MQTT_PORT))
roomtypes= ["livingroom", "bedroom", "outside", "kitchen"]
for x in roomtypes:
    mqtt_client.subscribe(topic="bps/testhouse/"+x)