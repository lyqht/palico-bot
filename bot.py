import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

import trello
from settings import (BOT_TOKEN, HOUSE_ID, TELEGRAM_GROUP_CHAT_ID,
                      TELEGRAM_TEST_TELEGRAM_CHAT_ID, TRELLO_TOKEN, DEMO_STATUS)
from utils.date_utils import DATE_HELPER
from utils.progress_utils import get_progress
from mqtt import mqtt_client


# Paths

MEMBERS_DATA_PATH = "data/members.json"
TASKS_DATA_PATH = "data/tasks.json"
MQTT_LOOP_ACTIVATED = False

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


def formatted_text_for_trello_task(task, members):
    if task.due:
        formatted_text = (
            f"    🔗[link]({task.shortUrl}) _Due {DATE_HELPER.convert_datetime_to_string(task.due)}_.\n")
    else:
        formatted_text = (
            f"    🔗[link]({task.shortUrl})\n")
    if len(members):
        members_text = " ".join([member for member in list(members)])
        formatted_text += f"    🍻({members})\n"
    return formatted_text


# Handler functions


def start_handler(update, context: CallbackContext):
    START_MESSAGE = "Henlo Meowster!"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=START_MESSAGE)
    
def status_subscribe_handler(update, context: CallbackContext):
    global MQTT_LOOP_ACTIVATED
    
    current_chat_id = update.effective_chat.id
    if DEMO_STATUS == "OFF":
        MESSAGE = "Demo is currently Offline! Contact the Catstone Meowsters if you think this is a bug!"
    
    elif DEMO_STATUS == "ON":
        
        # MQTT Configuration
        if current_chat_id not in mqtt_client.subscribers:
            mqtt_client.add_subscriber(current_chat_id)
            MESSAGE = "Activated Subscription to: " + HOUSE_ID
        else:
            MESSAGE = "Already subscribed to: " + HOUSE_ID
            
        if not MQTT_LOOP_ACTIVATED:
            print("Starting MQTT loop")
            mqtt_client.bot = context.bot
            mqtt_client.client.loop_start()
            MQTT_LOOP_ACTIVATED = True
            
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGE)

def status_unsubscribe_handler(update, context: CallbackContext):
    global MQTT_LOOP_ACTIVATED
    
    if DEMO_STATUS == "OFF":
        MESSAGE = "Demo is currently Offline! Contact the Catstone Meowsters if you think this is a bug!"
    
    elif DEMO_STATUS == "ON":
        current_chat_id = update.effective_chat.id
        if current_chat_id in mqtt_client.subscribers:
            MESSAGE = "Deactivated Subscription to: " + HOUSE_ID
            try:
                mqtt_client.remove_subscriber(current_chat_id)
            except ValueError:
                pass
        else:
            MESSAGE = "Not subscribed to any house. Failed to unsubscribe."
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=MESSAGE)
    
    if len(mqtt_client.subscribers) == 0:
        print("No more subscribers, Stopping MQTT Loop")
        mqtt_client.client.loop_stop()
        MQTT_LOOP_ACTIVATED = False
        
def unknown_handler(update, context: CallbackContext):
    IDK_MESSAGE = "Meow? I don't understand"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=IDK_MESSAGE)


def gantt_curr_week_handler(update, context: CallbackContext):
    if not os.path.isfile(TASKS_DATA_PATH):
        import googlesheets
        googlesheets.main()
    curr_week = DATE_HELPER.current_week_number()
    tasks = DATE_HELPER.get_gantt_tasks_by_week(curr_week)

    message = ["Meow~ these are the tasks for the next 2 weeks on Gantt Chart 📚"]
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


def trello_tasks_handler(update, context: CallbackContext):
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


def reminders_handler(update, context: CallbackContext):
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


def trello_member_selected_callback(update, context: CallbackContext):
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
        formatted_text = formatted_text_for_trello_task(
            task, partners_on_same_task)
        message.append(formatted_text)

    query.edit_message_text(text="\n".join(
        message), parse_mode=ParseMode.MARKDOWN)

# Jobs


def weekly_reminder(update, context: CallbackContext):
    curr_week = DATE_HELPER.current_week_number()
    WEEKLY_REMINDER_INTRO_MESSAGE = f"It is almost *Week {curr_week+1}*, and here are some updates!\n"
    tasks = trello.get_tasks_due_two_weeks()
    message = [WEEKLY_REMINDER_INTRO_MESSAGE]

    message.append(
        f"*The team's progress for Week {curr_week-1}-{curr_week} 🎉🎉*")
    list_of_progress = get_progress()
    for achievement in list_of_progress:
        message.append(f"✨ {achievement}")

    message.append("")
    message.append(
        f"*Trello Tasks for Week {curr_week}-{curr_week+1}*")
    for i in range(len(tasks)):
        task = tasks[i]
        message.append(f"{i+1}. {task.name}\n" +
                       formatted_text_for_trello_task(task, trello.translate_ids_to_names(task.members)))

    message.append(
        "⚠ Please check out the actual [trello board](https://trello.com/b/Ap7y9llJ/capstone)/[gantt chart](https://docs.google.com/spreadsheets/d/1G65rGEH_ih8r-J82EWFCzllOlZcU7jGWzfzCZkIYgZE/edit#gid=2140549662) from time to time too 🙌 Have a wonderful week ahead meow~")

    context.bot.send_message(
        chat_id=TELEGRAM_GROUP_CHAT_ID, text="\n".join(message), parse_mode=ParseMode.MARKDOWN)
