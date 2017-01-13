import logging
import configparser
from telegram.ext import Updater, CommandHandler

config = configparser.ConfigParser()
config.read('settings.ini')


updater = Updater(token=config.get("TELEGRAM", "token"))

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Тебе тут не рады...")
    print(update.message.chat_id)
    print(update.message)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
