from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_SECRET = os.getenv("TRELLO_SECRET")
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")
TESTMEMBER_ID = os.getenv("TESTMEMBER_ID")
GOOGLE_KEY = os.getenv("GOOGLE_KEY")
SHEETS_ID = os.getenv("SHEETS_ID")
