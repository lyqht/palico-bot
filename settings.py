import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_SECRET = os.getenv("TRELLO_SECRET")
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_PRIVATE_KEY = os.getenv("GOOGLE_PRIVATE_KEY")
GOOGLE_PRIVATE_KEY_ID = os.getenv("GOOGLE_PRIVATE_KEY_ID")
GOOGLE_CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SHEETS_ID = os.getenv("SHEETS_ID")

HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
BOT_PORT = int(os.getenv("BOT_PORT"))
OPERATION_MODE = os.getenv("OPERATION_MODE")

TELEGRAM_GROUP_CHAT_ID = os.getenv("TELEGRAM_GROUP_CHAT_ID")

TELEGRAM_TEST_TELEGRAM_CHAT_ID = os.getenv("TEST_TELEGRAM_CHAT_ID")


MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_IP = os.getenv("MQTT_SERVER")
HOUSE_ID = os.getenv("HOUSE_ID")
DEMO_STATUS = os.getenv("DEMO_STATUS")


