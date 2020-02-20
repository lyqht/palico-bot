import requests
import os.path
from utils.json_utils import write_to_json
from settings import TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID
from settings import TESTMEMBER_ID  # for testing. comment if not required.
from utils.date_utils import DATE_HELPER

BOARD_INFO_URL = "https://api.trello.com/1/boards/" + TRELLO_BOARD_ID
BOARD_MEMBERS_URL = "https://api.trello.com/1/boards/" + TRELLO_BOARD_ID + "/members"


def get_board_members():
    url = BOARD_MEMBERS_URL
    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN, "members": "none"}
    response = requests.request("GET", url, params=querystring)
    members = response.json()
    result = {}
    for member in members:
        result[member["id"]] = member["fullName"]
    return result


def get_member_detail(members, user="", param="id"):
    # iterate through boardMembers
    for i in range(len(members)):
        member = members[i]
        if user.lower() in member["username"]:
            return members[i][param]


def get_member_cards(memberID: str):
    BOARD_MEMBERS_CARD_URL = "https://api.trello.com/1/members/" + memberID + "/cards"
    url = BOARD_MEMBERS_CARD_URL
    querystring = {"filters": "all", "key": TRELLO_KEY,
                   "token": TRELLO_TOKEN,}
    response = requests.request("GET", url, params=querystring)
    return response.json()


class Task():
    def __init__(self, name, shortUrl, due, members=[]):
        self.name = name
        self.shortUrl = shortUrl
        self.members = members
        self.due = due


def get_member_tasks(memberID: str):
    cards = get_member_cards(memberID)
    tasks = [Task(card['name'], card['shortUrl'], card['due'], card['idMembers'])
             for card in cards if not card["dueComplete"]]
    
    return tasks


MEMBERS_DATA_PATH = "data/members.json"

# tasks = get_member_tasks("5e310b3f62949e4f2c912610")
# print(DATE_HELPER.convert_datetime_to_string(tasks[0].due))


