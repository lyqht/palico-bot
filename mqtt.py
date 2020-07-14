import paho.mqtt.client as mqtt

from settings import HOUSE_ID
from settings import MQTT_IP
from settings import MQTT_PORT
from settings import TELEGRAM_TEST_TELEGRAM_CHAT_ID


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK!")
    else:
        print("Bad connection, Returned Code: ", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code " + str(rc))


def mqtt_on_msg_callback(client, userdata, msg):
    global mqtt_client
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("=============================")

    # check topic
    topic = msg.topic
    sensor_type, house_id, room_type = topic.split("/")
    print("Sensor Type: {}, House_ID: {}, Room_Type: {}".format(
        sensor_type, house_id, room_type))
    if sensor_type == "bps" or sensor_type == "mlx":
        print("Activity Levels MQTT Message received")
        mqtt_client.send_message("Current Room that the user is in: " +
                                 room_type)

    elif sensor_type == "Fall":
        print("Fall Detection MQTT Message received")
        # TODO for fall detection message

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
        self.subscribers = []

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Subscribed to topic:", topic)

    def send_message(self, msg):
        assert self.bot != None
        print("Sending message from bot...")
        for x in self.subscribers:
            self.bot.send_message(chat_id=x, text=msg)

    def add_subscriber(self, chat_id):
        self.subscribers.append(chat_id)
        print("New Subscriber: ", chat_id)
        print("Current number of subscribers :", len(self.subscribers))

    def remove_subscriber(self, chat_id):
        self.subscribers.remove(chat_id)
        print("Removing Subscriber: ", chat_id)
        print("Current number of subscribers :", len(self.subscribers))


mqtt_client = MQTTClientForTelegramBot(MQTT_IP, int(MQTT_PORT))
roomtypes = ["livingroom", "bedroom", "outside", "kitchen"]
for x in roomtypes:
    mqtt_client.subscribe(topic="/".join(["bps", HOUSE_ID, x]))
    mqtt_client.subscribe(topic="/".join(["mlx", HOUSE_ID, x]))
    # TODO for fall detection topic
