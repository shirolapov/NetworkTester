import configparser
from telegram.ext import Updater, CommandHandler
from starter import Starter
from lan_tester.model import Model
from lan_tester.wol import send_magic_packet


config = configparser.ConfigParser()
config.read('settings.ini')

updater = Updater(token=config.get("TELEGRAM", "token"))

dispatcher = updater.dispatcher


def check(bot, update):
    model = Model()
    if model.check_is_exist_chat_id(update.message.chat_id):
        starter = Starter()
        starter.start(parameters=['-silent', '-report'], send_to=update.message.chat_id)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Тебя тут не ждали...")


def wake_on_lan(bot, update):
    model = Model()
    if model.check_is_exist_chat_id(update.message.chat_id):

        send_magic_packet('78-E7-D1-73-46-EC')  # WIN.DOMAIN.local
        send_magic_packet('90-FB-A6-81-7D-8A')  # CUBA.DOMAIN.local
        send_magic_packet('00:26:18:E0:2D:8C')  # FURIOSA.DOMAIN.local
        send_magic_packet('00:90:A9:6B:A2:50')  # CARACAS
        send_magic_packet('28:10:7B:25:3A:80')  # DNR-322L

        bot.sendMessage(chat_id=update.message.chat_id, text="Отправлен сигнал wake on lan.")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Тебя тут не ждали...")


start_handler = CommandHandler('check', check)
wol_handler = CommandHandler('wol', wake_on_lan)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(wol_handler)
updater.start_polling()
