import logging
import configparser
import random
import logging
from telegram.ext import Updater, CommandHandler
from lan_tester.model import Model


logging.basicConfig(filename='logs/telegram_add_admin.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


logging.info("Start app.")
config = configparser.ConfigParser()
config.read('settings.ini')

model = Model()


def generate_pin():
    new_pin = ""
    for x in range(0, 6):
        new_pin = new_pin + str(random.randint(0, 9))
    print(new_pin)
    return new_pin

pin = generate_pin()

updater = Updater(token=config.get("TELEGRAM", "token"))

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def register_admin(bot, update, args):
    if args:
        if args[0] == pin:
            if model.check_is_exist_chat_id(update.message.chat_id):
                bot.sendMessage(chat_id=update.message.chat_id, text="Уже зарегестрирован.")
                logging.info("Admin alredy registered.")
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text="Добро пожаловать...")
                model.add_chat_id(update.message.chat_id, update.message.chat)
                print("Admin is added.")
                logging.info("Admin added.")
        else:
            logging.warning("Wrong pin!")
            bot.sendMessage(chat_id=update.message.chat_id, text="Тебе тут не рады...")
    else:
        logging.info("Request without arguments")


register_admin_handler = CommandHandler('registeradmin', register_admin, pass_args=True)
dispatcher.add_handler(register_admin_handler)
updater.start_polling()
