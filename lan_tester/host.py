class Host:
    __available = False

    def __init__(self, group, name, ip):
        self.group = group
        self.name = name
        self.ip = ip

    def get_group(self):
        return self.group

    def get_name(self):
        return self.name

    def get_ip(self):
        return self.ip

    def __str__(self):
        return self.name

    def set_availables(self, available):
        if type(available) == bool:
            self.__available = available

    def get_availables(self):
        return self.__available
