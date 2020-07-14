import requests
import os.path
from utils.json_utils import write_to_json
from settings import TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID
from utils.date_utils import DATE_HELPER


class Task():
    def __init__(self, name, shortUrl, due, members=[]):
        self.name = name
        self.shortUrl = shortUrl
        self.members = members
        self.due = due


def get_board_lists():
    url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists"
    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN, "members": "none"}
    response = requests.request("GET", url, params=querystring)
    result = response.json()
    return result


def get_board_members():
    BOARD_MEMBERS_URL = "https://api.trello.com/1/boards/" + TRELLO_BOARD_ID + "/members"
    url = BOARD_MEMBERS_URL
    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN, "members": "none"}
    response = requests.request("GET", url, params=querystring)
    members = response.json()
    result = {}
    for member in members:
        result[member["id"]] = member["fullName"]
    return result


def get_member_detail(members, user="", param="id"):
    for i in range(len(members)):
        member = members[i]
        if user.lower() in member["username"]:
            return members[i][param]


def get_member_cards(memberID: str):
    BOARD_MEMBERS_CARD_URL = "https://api.trello.com/1/members/" + memberID + "/cards"
    url = BOARD_MEMBERS_CARD_URL
    querystring = {"filters": "all", "key": TRELLO_KEY,
                   "token": TRELLO_TOKEN, }
    response = requests.request("GET", url, params=querystring)
    return response.json()


def get_member_tasks(memberID: str):
    cards = get_member_cards(memberID)

    return make_tasks(cards)


def get_filtered_boards(boards):
    BOARD_LISTS = get_board_lists()
    TO_DO_LISTS_ID = []
    DONE_LISTS_ID = []

    for board in BOARD_LISTS:
        if "to-dos" in board["name"].lower():
            TO_DO_LISTS_ID.append(board["id"])
        elif "done" in board["name"].lower():
            DONE_LISTS_ID.append(board["id"])
    return TO_DO_LISTS_ID, DONE_LISTS_ID


def get_cards_due_two_weeks():
    BOARD_INFO_URL = "https://api.trello.com/1/boards/" + TRELLO_BOARD_ID
    url = BOARD_INFO_URL + "/cards/visible"
    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN}
    response = requests.request("GET", url, params=querystring)
    cards = response.json()

    def target_card(card):
        if card["due"]:
            due_date = DATE_HELPER.get_datetime_from_card(card["due"])
            due_date = due_date.date()
            return DATE_HELPER.in_sprint_range(due_date) and not card["dueComplete"]

    cards = filter(target_card, cards)
    return list(cards)


def get_tasks_due_two_weeks():
    cards = get_cards_due_two_weeks()
    return make_tasks(cards)


def make_tasks(cards):
    tasks = [Task(card['name'], card['shortUrl'], card['due'], card['idMembers'])
             for card in cards if not card["dueComplete"] and card["due"]]
    return tasks


def translate_ids_to_names(ids):

    members = get_board_members()
    return [members[id] for id in ids]
