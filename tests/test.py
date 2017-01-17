import unittest
from lan_tester.host import Host
from lan_tester.tools import compare_hosts, compare_lists_of_hosts, check_exist_host_in_list
from lan_tester.out import Out


class TestToolsMethods(unittest.TestCase):

    def test_compare_hosts(self):
        host1 = Host("GROUP1", "NAME1", "192.168.0.3")
        host2 = Host("GROUP1", "NAME1", "192.168.0.3")
        host3 = Host("GROUP1", "NAME1", "192.168.0.4")
        self.assertTrue(compare_hosts(host1, host2))
        self.assertFalse(compare_hosts(host2, host3))

    def test_check_exist_host_in_list(self):
        host11 = Host("GROUP1", "NAME1", "192.168.0.3")
        host12 = Host("GROUP2", "NAME2", "192.168.0.4")
        host13 = Host("GROUP3", "NAME3", "192.168.0.5")
        host14 = Host("GROUP4", "NAME4", "192.168.0.6")

        list1 = (host11, host12, host13)

        self.assertTrue(check_exist_host_in_list(host11, list1))
        self.assertTrue(check_exist_host_in_list(host12, list1))
        self.assertTrue(check_exist_host_in_list(host13, list1))
        self.assertFalse(check_exist_host_in_list(host14, list1))

    def test_compare_lists_of_hosts(self):
        host11 = Host("GROUP1", "NAME1", "192.168.0.3")
        host12 = Host("GROUP2", "NAME2", "192.168.0.4")
        host13 = Host("GROUP3", "NAME3", "192.168.0.5")

        host21 = Host("GROUP1", "NAME21", "192.168.0.6")
        host22 = Host("GROUP2", "NAME22", "192.168.0.8")

        host31 = Host("GROUP3", "NAME1", "1.1.1.1")
        host32 = Host("GROUP3", "NAME2", "1.2.1.1")
        host33 = Host("GROUP3", "NAME2", "1.2.1.2")

        host41 = Host("GROUP3", "NAME1", "1.1.1.1")
        host42 = Host("GROUP3", "NAME2", "1.2.1.1")
        host43 = Host("GROUP3", "NAME2", "1.2.1.2")

        list1 = (host11, host12, host13)
        list2 = (host21, host22)

        list1_1 = (host11, host12, host13)
        list1_2 = (host11, host12, host13)

        list3 = (host31, host32, host33)
        list4 = (host41, host42, host43)

        self.assertFalse(compare_lists_of_hosts(list1, list2))
        self.assertTrue(compare_lists_of_hosts(list1_1, list1_2))
        self.assertTrue(compare_lists_of_hosts(list3, list4))


class TestOutMethods(unittest.TestCase):

    def test_all_host_online(self):
        out = Out()
        out.all_host_online(telegram=True, send_to="All")

    def test_offline_hosts(self):
        list_of_offline_hosts = (
            Host("GROUP1", "NAME11", "192.168.0.1"),
            Host("GROUP1", "NAME12", "192.168.0.2"),
            Host("GROUP1", "NAME13", "192.168.0.3"),
            Host("GROUP1", "NAME14", "192.168.0.4"),
            Host("GROUP2", "NAME21", "192.168.0.5"),
            Host("GROUP2", "NAME22", "192.168.0.6"),
            Host("GROUP2", "NAME23", "192.168.0.7"),
            Host("GROUP3", "NAME31", "192.168.0.8"),
            Host("GROUP3", "NAME32", "192.168.0.9"),
            Host("GROUP3", "NAME33", "192.168.0.10"),
            Host("GROUP1", "NAME34", "192.168.0.11"),
            Host("GROUP1", "NAME35", "192.168.0.12"),
        )

        out = Out()
        out.offline_hosts(list_of_offline_hosts, telegram=True, send_to="All")

    def test_alredy_online_hosts(self):
        list_of_alredy_online_hosts = (
            Host("GROUP1", "NAME11", "192.168.0.1"),
            Host("GROUP1", "NAME12", "192.168.0.2"),
            Host("GROUP1", "NAME13", "192.168.0.3"),
            Host("GROUP1", "NAME14", "192.168.0.4"),
            Host("GROUP2", "NAME21", "192.168.0.5"),
        )

        out = Out()
        out.alredy_online_hosts(list_of_alredy_online_hosts, telegram=True, send_to="All")

if __name__ == '__main__':
    unittest.main()
