from .host import Host


class DataFile:

    @staticmethod
    def clear_data_file():
        f = open("datas/data.txt", "w")
        f.write("")
        f.close()

    @staticmethod
    def get_host_from_data_file():
        list_of_host = []
        f = open("datas/data.txt", "r")
        for line in f:
            host_str = line.split(":")
            list_of_host.append(Host(host_str[0], host_str[1], host_str[2].replace("\n", "")))
        f.close()
        return list_of_host

    @staticmethod
    def write_offline_host(host_obj):
        if not DataFile.check_exist_host_in_data_file(host_obj):
            f = open("datas/data.txt", "a")
            f.write("{group}:{name}:{ip}\n".format(group=host_obj.get_group(),
                                                   name=host_obj.get_name(), ip=host_obj.get_ip()))
            f.close()

    @staticmethod
    def check_exist_host_in_data_file(host_obj):
        f = open("datas/data.txt", "r")
        for line in f:
            check_line = "{group}:{name}:{ip}\n".format(group=host_obj.get_group(),
                                                        name=host_obj.get_name(), ip=host_obj.get_ip())
            if line == check_line:
                return True
        f.close()
