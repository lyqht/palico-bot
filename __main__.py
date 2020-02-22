import logging
import os.path
import sys
from settings import PORT, HEROKU_APP_NAME, BOT_TOKEN, OPERATION_MODE, print_variables
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot import start_handler, gantt_curr_week_handler, trello_tasks_handler, unknown_handler, trello_member_selected_callback

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

if __name__ == "__main__":
    # Initalize Updater, Dispatcher and Handlers
    updater = Updater(token=BOT_TOKEN, use_context=True)

    if OPERATION_MODE == "dev":
        def run(updater):
            print("Running in development mode")
            updater.start_polling()
    elif OPERATION_MODE == "prod":
        def run(updater):
            print("Running in production mode")
            if not os.path.exists('data'):
                os.mkdirs('data')
            updater.start_webhook(listen="0.0.0.0",
                                  port=PORT,
                                  url_path=BOT_TOKEN)
            updater.bot.set_webhook(
                "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, BOT_TOKEN))
    else:
        logger.error("No MODE specified!")
        sys.exit(1)

    start_handler = CommandHandler('start', start_handler)
    gantt_curr_week_handler = CommandHandler(
        'gantt', gantt_curr_week_handler)
    trello_handler = CommandHandler('trello', trello_tasks_handler)
    unknown_handler = MessageHandler(Filters.command, unknown_handler)

    # Add Handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(gantt_curr_week_handler)
    dispatcher.add_handler(trello_handler)
    dispatcher.add_handler(CallbackQueryHandler(
        trello_member_selected_callback))
    dispatcher.add_handler(unknown_handler)

    # Start bot
    run(updater)
