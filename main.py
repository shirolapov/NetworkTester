import sys
import logging
from lan_tester.tester import Tester
from lan_tester.tools import compare_hosts, create_serialize_list_of_hosts, compare_lists_of_hosts
from lan_tester.bot import TelegramBotAlert
from lan_tester.model import Model


logging.basicConfig(filename='logs/history.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)


class Main:

    def __init__(self, parameters):
        self.model = Model()
        tester = Tester("datas/hosts_list.json")
        tbot = TelegramBotAlert()

        self.__list_of_offline_host_in_past = self.model.get_host_from_data_file()
        self.__list_of_online_hosts = tester.get_list_of_online_host()
        self.__list_of_alredy_online_hosts = self.__create_list_of_alredy_online_hosts()
        self.__list_of_offline_hosts = tester.get_list_of_offline_host()

        self.model.clear_data()

        if len(self.__list_of_alredy_online_hosts) > 0:
            self.__have_alredy_online_hosts()

        if len(self.__list_of_offline_hosts) > 0:
            self.__have_offline_hosts()
        else:
            self.__all_host_online()
            if parameters.count("-report") > 0:
                tbot.send_message("Все узлы доступны.")

        if len(self.__list_of_alredy_online_hosts) > 0 or len(self.__list_of_offline_hosts) > 0 and \
                not compare_lists_of_hosts(self.__list_of_offline_host_in_past, self.__list_of_offline_hosts):
            tbot.create_alert_message(self.__list_of_alredy_online_hosts, self.__list_of_offline_hosts)

        if parameters.count("-silent") > 0:
            exit()
        else:
            input("\nPress enter to exit.")

    def __have_alredy_online_hosts(self):
        serialize_list = create_serialize_list_of_hosts(self.__list_of_alredy_online_hosts)
        print("This host(s) alredy online:")
        for group in serialize_list:
            print("Group name: {groupname}".format(groupname=group))
            for host in serialize_list[group]:
                print("\t{hostname}, {hostip}".format(hostname=host.get_name(), hostip=host.get_ip()))
                logging.info("Group: {grouphost}, Host: {hostname}, IP: "
                                "{hostip} - is online again".format(grouphost=host.get_group(),
                                                               hostname=host.get_name(), hostip=host.get_ip()))
        print("\n")

    def __create_list_of_alredy_online_hosts(self):
        list_of_alredy_online_hosts = []

        for online_host in self.__list_of_online_hosts:
            for offline_host_in_past in self.__list_of_offline_host_in_past:
                if compare_hosts(online_host, offline_host_in_past):
                    list_of_alredy_online_hosts.append(online_host)
        return list_of_alredy_online_hosts

    def __all_host_online(self):
        logging.info("All host online.")
        print("All host is online.\n")

    def __have_offline_hosts(self):
        serialize_list = create_serialize_list_of_hosts(self.__list_of_offline_hosts)
        print("Attention!\nThis host(s) is offline!\n")
        for group in serialize_list:
            print("Group name: {groupname}".format(groupname=group))
            for host in serialize_list[group]:
                self.model.write_offline_host(host)
                print("\t{hostname}, {hostip}".format(hostname=host.get_name(), hostip=host.get_ip()))
                logging.warning("Group: {grouphost}, Host: {hostname}, IP: "
                                "{hostip} - is offline".format(grouphost=host.get_group(),
                                                               hostname=host.get_name(), hostip=host.get_ip()))

parameters_shell = sys.argv

Main(parameters_shell)
