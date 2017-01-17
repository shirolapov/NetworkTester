import logging
from lan_tester.tester import Tester
from lan_tester.tools import compare_lists_of_hosts, create_list_of_alredy_online_hosts
from lan_tester.bot import TelegramBotAlert
from lan_tester.model import Model
from lan_tester.out import Out


logging.basicConfig(filename='logs/history.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)


class Starter:

    def start(self, parameters=[], send_to="All"):
        self.__list_of_offline_host_in_past = []
        self.__list_of_online_hosts = []
        self.__list_of_alredy_online_hosts = []
        self.__list_of_offline_hosts = []

        self.model = Model()
        self.out = Out()

        __tester = Tester("datas/hosts_list.json")
        __tester.ping_all_hosts()

        tbot = TelegramBotAlert()

        self.__list_of_offline_host_in_past = self.model.get_host_from_data_file()
        self.__list_of_online_hosts = __tester.get_list_of_online_host()
        self.__list_of_alredy_online_hosts = create_list_of_alredy_online_hosts(self.__list_of_online_hosts,
                                                                                self.__list_of_offline_host_in_past)
        self.__list_of_offline_hosts = __tester.get_list_of_offline_host()

        self.model.clear_data()

        if len(self.__list_of_offline_hosts) > 0:
            self.model.write_list_of_offline_hosts(self.__list_of_offline_hosts)
            if parameters.count("-report") > 0:
                self.out.offline_hosts(self.__list_of_offline_hosts, telegram=True, send_to=send_to)
            else:
                self.out.offline_hosts(self.__list_of_offline_hosts, telegram=False)
        else:
            if parameters.count("-report") > 0:
                self.out.all_host_online(telegram=True, send_to=send_to)
            else:
                self.out.all_host_online(telegram=False, send_to=send_to)

        if len(self.__list_of_alredy_online_hosts) > 0 or len(self.__list_of_offline_hosts) > 0 and \
                not compare_lists_of_hosts(self.__list_of_offline_host_in_past, self.__list_of_offline_hosts):
            tbot.create_alert_message(self.__list_of_alredy_online_hosts, self.__list_of_offline_hosts)

        if not parameters.count("-silent") > 0:
            input("\nPress enter to exit.")
