import configparser
import logging
from telegram import Bot, ParseMode
from lan_tester.tools import create_serialize_list_of_hosts
from lan_tester.model import Model


logging.basicConfig(filename='logs/python-telegram-bot.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)


class TelegramBotAlert:


    def __init__(self):
        self.model = Model()
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.__list_of_chat_ids = self.model.get_chat_ids()
        self.__token = config.get("TELEGRAM", "token")
        self.__bot = Bot(token=self.__token)

    def create_alert_message(self, list_of_alredy_online_hosts, list_of_offline_hosts):
        message = ""

        if len(list_of_alredy_online_hosts) > 0:
            serialize_list_of_alredy_online_hosts = create_serialize_list_of_hosts(list_of_alredy_online_hosts)
            message += self.create_alert_message_with_alredy_online_hosts(serialize_list_of_alredy_online_hosts)

        if len(list_of_offline_hosts) > 0:
            serialize_list_of_offline_hosts = create_serialize_list_of_hosts(list_of_offline_hosts)
            message += self.create_alert_message_with_offline_hosts(serialize_list_of_offline_hosts)
        else:
            message += "Все узлы доступны."

        self.send_message(message)

    def create_alert_message_with_offline_hosts(self, list_of_hosts):
        message = "<b>Следующие узлы недоступны!</b>\n"
        for group in list_of_hosts:
            message += "\tГруппа: <i>{group_name}</i>\n".format(group_name=group)
            for host in list_of_hosts[group]:
                message += "\t\t{host}, {hostip}\n".format(host=host.get_name(), hostip=host.get_ip())
            message += "\n"
        return message

    def create_alert_message_with_alredy_online_hosts(self, list_of_hosts):
        message = "<b>Следующие узлы снова доступны:</b>\n"
        for group in list_of_hosts:
            message += "\tГруппа: <i>{group_name}</i>\n".format(group_name=group)
            for host in list_of_hosts[group]:
                message += "\t\t{host}, {hostip}\n".format(host=host.get_name(), hostip=host.get_ip())
            message += "\n"
        return message

    def send_message(self, message, send_to="All"):
        if send_to == "All":
            for chat_id in self.__list_of_chat_ids:
                self.__bot.send_message(chat_id=str(chat_id), text=message, parse_mode=ParseMode.HTML)
        else:
            self.__bot.send_message(chat_id=str(send_to), text=message, parse_mode=ParseMode.HTML)
