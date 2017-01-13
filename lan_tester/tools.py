def compare_hosts(host1, host2):
    if str(host1.get_group()) == str(host2.get_group()) and \
            str(host1.get_name()) == str(host2.get_name()) and \
            str(host1.get_ip()) == str(host2.get_ip()):
        return True
    else:
        return False

def create_serialize_list_of_hosts(list_of_hosts):
    list_of_groups = []
    for host_obj in list_of_hosts:
        group_name = host_obj.get_group()
        if list_of_groups.count(group_name) == 0:
            list_of_groups.append(group_name)

    def get_serialize_list():
        serialize_list = {}
        for group in list_of_groups:
            list_of_host = []
            for host_obj in list_of_hosts:
                if host_obj.get_group() == group:
                    list_of_host.append(host_obj)
            serialize_list[group] = list_of_host
        return serialize_list

    return get_serialize_list()

def check_exist_host_in_list(host, list):
    for host_from_list in list:
        if compare_hosts(host_from_list, host):
            return True
    return False

def compare_lists_of_hosts(list1, list2):
    if not len(list1) == len(list2):
        return False

    for host_from_list in list1:
        if not check_exist_host_in_list(host_from_list, list2):
            return False

    return True