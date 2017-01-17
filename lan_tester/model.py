import os
import json
import sqlite3
from lan_tester.host import Host


class Model:

    def __init__(self):
        if not os.path.isfile('datas/data.db'):
            self.__initialization_db()

    def __initialization_db(self):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE offline_hosts
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            group_name VARCHAR(255) NOT NULL,
            host_name VARCHAR(255) NOT NULL,
            ip_host VARCHAR(15) NOT NULL
        )''')

        c.execute('''CREATE TABLE chat_ids
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            chat_id VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NULL,
            first_name VARCHAR(255) NULL,
            username VARCAHR(255) NULL,
            datetime TIMESTAMP NULL
        )''')
        conn.close()

    def write_offline_host(self, host_obj):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        c.execute("INSERT INTO offline_hosts (group_name, host_name, ip_host) VALUES (?, ?, ?)",
                  (host_obj.get_group(), host_obj.get_name(), host_obj.get_ip()))
        conn.commit()
        conn.close()

    def get_host_from_data_file(self):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        list_of_host = []
        for row in c.execute("SELECT * FROM offline_hosts ORDER BY 'id'"):
            list_of_host.append(Host(row[1], row[2], row[3]))
        return list_of_host

    def check_exist_host_in_data_file(self, host_obj):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        list_of_host = []
        for row in c.execute("SELECT * FROM offline_hosts WHERE group_name=? AND host_name=? AND ip_host=?",
                             (host_obj.get_group(), host_obj.get_name(), host_obj.get_ip())):
            list_of_host.append(Host(row[1], row[2], row[3]))
        conn.close()
        if len(list_of_host) > 0:
            return True
        else:
            return False

    def clear_data(self):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        c.execute("DELETE FROM offline_hosts")
        conn.commit()
        conn.close()

    def get_chat_ids(self):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        list_of_chat_ids = []
        for row in c.execute("SELECT * FROM chat_ids"):
            list_of_chat_ids.append(row[1])
        return  list_of_chat_ids

    def add_chat_id(self, chat_id, chat_info):
        if not self.check_is_exist_chat_id(chat_id):
            conn = sqlite3.connect('datas/data.db')
            c = conn.cursor()
            c.execute("INSERT INTO chat_ids (chat_id, last_name, first_name, username, datetime) VALUES (?, ?, ?, ?, DATETIME())", (chat_id, chat_info['last_name'], chat_info['first_name'], chat_info['username']))
            conn.commit()
            conn.close()

    def check_is_exist_chat_id(self, chat_id):
        conn = sqlite3.connect('datas/data.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM chat_ids"):
            if str(row[1]) == str(chat_id):
                return True
        else:
            return False

    def get_hosts_list(self, file):
        hosts_list = []
        f = open(file)
        data = json.load(f)
        for group in data:
            for host in data[group]:
                hosts_list.append(Host(group, host, data[group][host]))
        return hosts_list

    def write_list_of_offline_hosts(self, list_of_offline_hosts):
        for host in list_of_offline_hosts:
            if not self.check_exist_host_in_data_file(host):
                self.write_offline_host(host)
