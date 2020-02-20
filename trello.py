import requests
from settings import TRELLO_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID
from settings import TESTMEMBER_ID  # for testing. comment if not required.

BOARD_INFO_URL = "https://api.trello.com/1/boards/" + TRELLO_BOARD_ID
BOARD_MEMBERS_URL = "https://api.trello.com/1/boards/" + TRELLO_BOARD_ID + "/members"


def get_board_members():
    url = BOARD_MEMBERS_URL
    querystring = {"key": TRELLO_KEY, "token": TRELLO_TOKEN, "members": "none"}
    response = requests.request("GET", url, params=querystring)
    return response.json()


def get_member_detail(members, user="", param="id"):
    # iterate through boardMembers
    for i in range(len(members)):
        member = members[i]
        if user.lower() in member["username"]:
            return members[i][param]


def get_member_cards(memberID):
    BOARD_MEMBERS_CARD_URL = "https://api.trello.com/1/members/" + memberID + "/cards"
    url = BOARD_MEMBERS_CARD_URL
    querystring = {"filters": "all", "key": TRELLO_KEY, "token": TRELLO_TOKEN}
    response = requests.request("GET", url, params=querystring)
    return response.json()

# def printCards(cards):
#   # TODO:


cards = get_member_cards(TESTMEMBER_ID)
