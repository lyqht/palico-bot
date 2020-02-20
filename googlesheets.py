from settings import SHEETS_ID
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from utils.json_utils import write_to_json


def get_ganttchart():
    SCOPE = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', SCOPE)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(SHEETS_ID)
    worksheet = sheet.get_worksheet(0)
    return worksheet


headers = ["TASK NAME", "START DATE", "END DATE",
           "DURATION (WORK DAYS)", "TEAM MEMBER"]
noise_values = ["Exploration and acquisition",
                "Solution Investigation", "Reviews", "Legend:", "Radar", "Other Sensors", "Logistics/Administration"]


def main():
    worksheet = get_ganttchart()
    items = {}

    for header in headers:
        cell = worksheet.find(header)
        # print("Found header %s at R%sC%s" % (header, cell.row, cell.col))
        values = worksheet.col_values(cell.col)
        values = filter(lambda x: x != "" and x !=
                        header and x not in noise_values, values)
        items[header] = list(values)

    tasks = []

    num_tasks = len(items[headers[0]])
    for i in range(num_tasks):
        task = {}
        for header in headers:
            task[header] = items[header][i]
        tasks.append(task)

    write_to_json(tasks, "data/tasks.json")
