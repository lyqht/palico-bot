from date_utils import DateUtils, DATE_HELPER
from settings import BOT_TOKEN, TRELLO_TOKEN
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

START_MESSAGE = "Henlo Meowster!"
IDK_MESSAGE = "Meow? I don't understand"
CURR_WEEK_TASKS_INTRO_MESSAGE = "Meow~ these are the tasks this week on Gantt Chart"


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=START_MESSAGE)


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=IDK_MESSAGE)


def curr_week_gantt_tasks(update, context):
    curr_week = DATE_HELPER.current_week_number()
    tasks = DATE_HELPER.get_tasks_by_week(curr_week)

    print(f"Number of tasks this week: {len(tasks)}")

    message = [CURR_WEEK_TASKS_INTRO_MESSAGE]
    for i in range(len(tasks)):
        task = tasks[i]
        task_name = task["TASK NAME"]
        task_start = task["START DATE"]
        task_end = task["END DATE"]
        task_members = task["TEAM MEMBER"]
        text = f"{i+1}. <b>{task_name}</b>: {task_start}-{task_end} [{task_members}]"
        message.append(text)

    result_message = "\n\n".join(message)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=result_message, parse_mode=ParseMode.HTML
    )


def main():
    # Initalize Updater, Dispatcher and Handlers
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    gantt_chart_handler = CommandHandler('gantt', curr_week_gantt_tasks)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # Add Handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(gantt_chart_handler)
    dispatcher.add_handler(unknown_handler)

    # Start bot
    updater.start_polling()
