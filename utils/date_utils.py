import pandas as pd
import numpy as np
import datetime
from utils.json_utils import read_json


class DateUtils():
    def __init__(self, start_date, num_weeks, start_week):
        workdays = pd.date_range(
            start=start_date, periods=7*num_weeks)
        self.workdays = workdays
        self.gantt_start = workdays[0]
        self.start_week = start_week
        self.gantt_end = workdays[-1]
        self.workdays_per_week = np.resize(workdays, (num_weeks, 7))

    def get_datetime(self, task_date_string: str):
        return datetime.datetime.strptime(task_date_string + " 2020", "%d %b %Y")

    def get_week(self, day: datetime.datetime, output_week_number=False):
        """
        returns the week range and week number
        @example: week, week_number = week_range(datetime.datetime(2020, 2, 20))
        """
        for i in range(len(self.workdays_per_week)):
            week = self.workdays_per_week[i]
            start = pd.to_datetime(week[0])
            end = pd.to_datetime(week[-1])
            if (day >= start) and (day <= end):
                if output_week_number:
                    return (week, i+self.start_week)
                else:
                    return week
        return "No week range found for this workday, is this a weekend?"

    def current_week(self):
        today = datetime.datetime.today().date()
        week = self.get_week(today)
        return week

    def current_week_number(self):
        today = datetime.datetime.now().date()
        week, i = self.get_week(today, output_week_number=True)
        return i

    def convert_datetime_to_string(self, obj):
        parsed_date = datetime.datetime.strptime(obj, "%Y-%m-%dT%H:%M:%S.%fZ")
        return f"{parsed_date.day} {parsed_date.strftime('%B')}"

    def get_tasks_by_week(self, week_number: int):
        tasks = read_json('data/tasks.json')
        queried_tasks = []
        for task in tasks:
            start = DATE_HELPER.get_datetime(task["START DATE"])
            end = DATE_HELPER.get_datetime(task["END DATE"])
            start_week = DATE_HELPER.get_week(start, output_week_number=True)[
                1]
            end_week = DATE_HELPER.get_week(end, output_week_number=True)[1]

            in_curr_week = start_week == week_number or end_week == week_number
            if in_curr_week:
                queried_tasks.append(task)

            after_curr_week = DATE_HELPER.get_week(start, output_week_number=True)[
                1] > week_number
            if after_curr_week:
                break
        return queried_tasks


CAPSTONE_START_DAY = datetime.datetime(2020, 2, 3)
DATE_HELPER = DateUtils(CAPSTONE_START_DAY, 12, start_week=2)

CURRENT_WEEK_NUMBER = DATE_HELPER.current_week_number()
# CURRENT_WEEK_TASKS = DATE_HELPER.get_tasks_by_week(CURRENT_WEEK_NUMBER)
