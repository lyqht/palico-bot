import trello
import os
from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from settings import BOT_TOKEN, TRELLO_TOKEN
from utils.date_utils import DATE_HELPER


# Paths

MEMBERS_DATA_PATH = "data/members.json"
TASKS_DATA_PATH = "data/tasks.json"

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


def start_handler(update, context):
    START_MESSAGE = "Henlo Meowster!"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=START_MESSAGE)


def unknown_handler(update, context):
    IDK_MESSAGE = "Meow? I don't understand"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=IDK_MESSAGE)


def gantt_curr_week_handler(update, context):
    if not os.path.isfile(TASKS_DATA_PATH):
        import googlesheets
        googlesheets.main()
    curr_week = DATE_HELPER.current_week_number()
    tasks = DATE_HELPER.get_tasks_by_week(curr_week)

    print(f"Number of tasks this week: {len(tasks)}")

    message = ["Meow~ these are the tasks this week on Gantt Chart 📚"]
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


def trello_tasks_handler(update, context):
    TRELLO_INTRO_MESSAGE = "Who are you trying to track on Trello?"
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


def reminders_handler(update, context):
    choices = ["Add Reminder", "View Reminders"]
    buttons = [InlineKeyboardButton(
        choice, callback_data=choice) for choice in choices]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=2))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Leave it to me Meowster!",
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_notification=True
    )

# Callbacks


def trello_member_selected_callback(update, context):
    query = update.callback_query
    requested_member_id = query.data
    members = trello.get_board_members()
    member = members[requested_member_id]

    separator_line = "―" * 20
    TRELLO_QUERY_COMPLETE_MESSAGE = "Tasks that were assigned to \n"
    message = [TRELLO_QUERY_COMPLETE_MESSAGE +
               f"*{member}* 🤟	 \n" + separator_line + "\n"]
    tasks = trello.get_member_tasks(requested_member_id)
    for i in range(len(tasks)):
        task = tasks[i]
        partners_on_same_task = [members[id]
                                 for id in task.members if id != requested_member_id]
        message.append(f"{i+1}. *{task.name}*")
        if task.due:
            formatted_text = (
                f"    🔗[link]({task.shortUrl}) _Due {DATE_HELPER.convert_datetime_to_string(task.due)}_.\n")
        else:
            formatted_text = (
                f"    🔗[link]({task.shortUrl})\n")
        if len(partners_on_same_task):
            formatted_text += f"    🍻({partners_on_same_task})\n"
        message.append(formatted_text)

    query.edit_message_text(text="\n".join(
        message), parse_mode=ParseMode.MARKDOWN)
