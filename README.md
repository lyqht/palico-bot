# palico-bot

This bot was created for my capstone project to perform the features below.
The gantt chart template that our team used specifically is the Manual Gantt Chart that can be found [here](https://www.teamgantt.com/free-gantt-chart-excel-template).

## Features

This bot allows you to perform:

- Google Sheets Gantt Chart Tracking by week
- Trello Tasks Tracking by user

## Telegram Commands

- `/gantt` for current week updates
- `/trello` for selecting a group member and viewing uncompleted tasks assigned to them.

## Pull Requests

Contributions are welcome! Here are some tasks that I've in mind but yet to work on them.

- Connect data to SQLlite instead of saving them in `.json` format
- Add weekly reminder operation
- Allow users to mark complete Trello tasks with confirmation prompt when they view specific user's tasks
- Show the entire Gantt Chart somehow on Telegram
- Let the bot reply with

## Setup instructions 

Install necessary packages

```
pip install -r requirements.txt
```

All secret variables are imported in `settings.py` are used in other modules. For the list of secret variables required to set up this bot, refer to `.env.sample` to make your own `.env`.


### Deployment

Methods
1. Make your shell run the bot forever 
2. Deploy it via an Ubuntu machine and running permanantly via `tmux`.
3. Heroku
   - Here is a useful [link](https://coreyward.svbtle.com/how-to-send-a-multiline-file-to-heroku-config) for uploading `credentials.json` for Google API to work. 
