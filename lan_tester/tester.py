import json
from subprocess import call
from lan_tester.host import Host


class Tester:

    def __init__(self, file):
        self.__list_of_host = []
        self.__list_of_checked_host = []
        self.__list_of_online_host = []
        self.__list_of_offline_host = []

        self.__get_list_of_hosts(file)  # Get list of all host (object host) from JSON file
        self.__ping_all_hosts()  # Ping of all host from __list_of_host
        self.__create_list_of_online_and_offline_hosts()

    def __get_list_of_hosts(self, file):
        f = open(file)
        data = json.load(f)
        for group in data:
            for host in data[group]:
                self.__list_of_host.append(Host(group, host, data[group][host]))

    def __ping_all_hosts(self):
        for host in self.__list_of_host:
            print("Ping: {hostname}, from {groupname}".format(hostname=host.get_name(), groupname=host.get_group()))
            result = self.ping(host)
            print("Result: {result}\n".format(result=result))
            self.__list_of_checked_host.append(host)

    @staticmethod
    def ping(host):
        response = call("ping -n 1 " + host.get_ip(), stdout=-1)
        if response == 0:
            host.set_availables(True)
            return True
        else:
            host.set_availables(False)
            return False

    def __create_list_of_online_and_offline_hosts(self):
        for host in self.__list_of_checked_host:
            if host.get_availables():
                self.__list_of_online_host.append(host)
            else:
                self.__list_of_offline_host.append(host)

    def get_list_of_checked_hosts(self):
        return self.__list_of_checked_host

    def get_list_of_online_host(self):
        return self.__list_of_online_host

    def get_list_of_offline_host(self):
        return self.__list_of_offline_host
