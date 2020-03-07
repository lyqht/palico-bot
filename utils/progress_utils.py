from collections import defaultdict
from utils.json_utils import read_json
from utils.date_utils import DATE_HELPER
achievements = defaultdict(list)


def add_achievement(week: int, achievement: str):
    achievements[week].append(achievement)


def get_progress():
    list_of_progress = []
    progress = read_json("data/progress.json")
    for achievement in progress:
        difference = achievement["Week"] - DATE_HELPER.current_week_number()
        if difference >= -2 and difference <= 0:
            list_of_progress.extend(achievement["Achievements"])
    return list_of_progress
