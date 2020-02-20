import bot
import googlesheets
import os.path

if __name__ == "__main__":
    if not os.path.isfile("tasks.json"):
        googlesheets.main()

    bot.main()
