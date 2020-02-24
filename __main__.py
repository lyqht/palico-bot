import logging
import os.path
import sys

from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from bot import gantt_curr_week_handler
from bot import start_handler
from bot import trello_member_selected_callback
from bot import trello_tasks_handler
from bot import unknown_handler
from bot import weekly_callback_alarm
from settings import BOT_TOKEN
from settings import HEROKU_APP_NAME
from settings import OPERATION_MODE
from settings import PORT

from utils.date_utils import DATE_HELPER, FIRST_REMINDER_DAY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

logger = logging.getLogger()

if __name__ == "__main__":
    # Initalize Updater
    updater = Updater(token=BOT_TOKEN, use_context=True)

    if OPERATION_MODE == "dev":

        def run(updater):
            print("Running in development mode")
            updater.start_polling()

    elif OPERATION_MODE == "prod":

        def run(updater):
            print("Running in production mode")
            if not os.path.exists("data"):
                os.mkdir("data")
            updater.start_webhook(listen="0.0.0.0",
                                  port=PORT,
                                  url_path=BOT_TOKEN)
            updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(
                HEROKU_APP_NAME, BOT_TOKEN))

    else:
        logger.error("No MODE specified!")
        sys.exit(1)

    # Initialize Handlers

    start_handler = CommandHandler("start", start_handler)
    gantt_curr_week_handler = CommandHandler("gantt", gantt_curr_week_handler)
    trello_handler = CommandHandler("trello", trello_tasks_handler)
    unknown_handler = MessageHandler(Filters.command, unknown_handler)

    # Job Queue

    job_queue = updater.job_queue
    reminder_weekly_job = job_queue.run_repeating(
        weekly_callback_alarm, DATE_HELPER.get_one_week_interval(), FIRST_REMINDER_DAY)
    job_queue.start()
    print(job_queue.jobs())

    # Initialize Dispatcher and Add Handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(gantt_curr_week_handler)
    dispatcher.add_handler(trello_handler)
    dispatcher.add_handler(
        CallbackQueryHandler(trello_member_selected_callback))
    dispatcher.add_handler(unknown_handler)

    # Start bot
    run(updater)
