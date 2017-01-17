import logging
from lan_tester.bot import TelegramBotAlert
from lan_tester.tools import create_serialize_list_of_hosts


logging.basicConfig(filename='logs/history.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)


class Out:
    __all_host_online_message = "All host online."

    def __init__(self):
        self.__tbot = TelegramBotAlert()

    def all_host_online(self, telegram=False, send_to="All"):
        logging.info(self.__all_host_online_message)
        print(self.__all_host_online_message)
        if telegram:
            self.__tbot.send_message(self.__all_host_online_message, send_to)

    def offline_hosts(self, list_of_offline_hosts, telegram=False, send_to="All"):
        serialize_list = create_serialize_list_of_hosts(list_of_offline_hosts)
        print("Attention!\nThis host(s) is offline!\n")
        for group in serialize_list:
            print("Group name: {groupname}".format(groupname=group))
            for host in serialize_list[group]:
                # self.model.write_offline_host(host)
                print("\t{hostname}, {hostip}".format(hostname=host.get_name(), hostip=host.get_ip()))
                logging.warning("Group: {grouphost}, Host: {hostname}, IP: "
                                "{hostip} - is offline".format(grouphost=host.get_group(),
                                                               hostname=host.get_name(), hostip=host.get_ip()))
        if telegram:
            message_for_telegram = self.__tbot.create_alert_message_with_offline_hosts(serialize_list)
            if send_to == "All":
                self.__tbot.send_message(message_for_telegram)
            else:
                self.__tbot.send_message(message_for_telegram, send_to)

    def alredy_online_hosts(self, list_of_alredy_online_hosts, telegram=False, send_to="All"):
        serialize_list = create_serialize_list_of_hosts(list_of_alredy_online_hosts)
        print("This hosts is alredy online:\n")
        for group in serialize_list:
            print("Group name: {groupname}".format(groupname=group))
            for host in serialize_list[group]:
                print("\t{hostname}, {hostip}".format(hostname=host.get_name(), hostip=host.get_ip()))

        if telegram:
            message_for_telegram = self.__tbot.create_alert_message_with_alredy_online_hosts(serialize_list)
            if send_to == "All":
                self.__tbot.send_message(message_for_telegram)
            else:
                self.__tbot.send_message(message_for_telegram, send_to)
