from utils.date_utils import DATE_HELPER
from settings import BOT_TOKEN, TRELLO_TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode
import trello
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

START_MESSAGE = "Henlo Meowster!"
IDK_MESSAGE = "Meow? I don't understand"
CURR_WEEK_TASKS_INTRO_MESSAGE = "Meow~ these are the tasks this week on Gantt Chart"
TRELLO_INTRO_MESSAGE = "Who are you trying to track on Trello?"
TRELLO_QUERY_COMPLETE_MESSAGE = "Tasks that were assigned to "

# UI functions


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

# Handler functions


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=START_MESSAGE)


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=IDK_MESSAGE)


def curr_week_gantt_tasks(update, context):
    if not os.path.isfile(TASKS_DATA_PATH):
        googlesheets.main()
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


def trello_tasks(update, context):
    members = trello.get_board_members()

    buttons = [InlineKeyboardButton(
        members[member_id], callback_data=member_id) for member_id in members]

    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TRELLO_INTRO_MESSAGE,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_notification=True
    )


def trello_member_selected(update, context):
    query = update.callback_query
    requested_member_id = query.data
    members = trello.get_board_members()
    member = members[requested_member_id]

    message = [TRELLO_QUERY_COMPLETE_MESSAGE +
               f"*{member}* 🤟	 \n" + "―"*30 + "\n"]
    tasks = trello.get_member_tasks(requested_member_id)
    for i in range(len(tasks)):
        task = tasks[i]
        partners_on_same_task = [members[id]
                                 for id in task.members if id != requested_member_id]
        message.append(f"{i+1}. *{task.name}*")
        if task.due:
            message.append(
                f"    🔗[link]({task.shortUrl}) _Due {DATE_HELPER.convert_datetime_to_string(task.due)}_.    \n   🍻({partners_on_same_task})\n")
        else:
            message.append(
                f"    🔗[link]({task.shortUrl})\n    🍻({partners_on_same_task})\n")

    query.edit_message_text(text="\n".join(
        message), parse_mode=ParseMode.MARKDOWN)


def main():
    # Initalize Updater, Dispatcher and Handlers
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    gantt_chart_handler = CommandHandler('gantt', curr_week_gantt_tasks)
    trello_handler = CommandHandler('trello', trello_tasks)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # Add Handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(gantt_chart_handler)
    dispatcher.add_handler(trello_handler)
    dispatcher.add_handler(CallbackQueryHandler(trello_member_selected))
    dispatcher.add_handler(unknown_handler)

    # Start bot
    updater.start_polling()
