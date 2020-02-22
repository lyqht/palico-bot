from dotenv import load_dotenv
import os

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
PORT = int(os.getenv("PORT"))
OPERATION_MODE = os.getenv("OPERATION_MODE")

TESTMEMBER_ID = os.getenv("TESTMEMBER_ID")
