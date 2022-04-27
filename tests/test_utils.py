import unittest
from iplkp.utils import parse_args, parse_address_args
from unittest import mock

class TestUtils(unittest.TestCase):
    def test_parse_args_single_ip(self):
        supplied_args = ["-i", "192.168.1.1", "-g", "-o", "output.txt", "-f", "-c"]
        expected = {
            "filename": None,
            "ip_addr": "192.168.1.1",
            "just_geo": True,
            "just_rdap": False,
            "overwrite": True,
            "save_output": "output.txt",
            "use_cache": False
        }
        self.assertDictEqual(vars(parse_args(supplied_args)), expected)

    def test_parse_address_args_single_ip(self):
        supplied_args = ["-i", "192.168.1.1", "-g"]
        args = parse_args(supplied_args)
        results = parse_address_args(args)
        expected = ["192.168.1.1"]
        self.assertEquals(expected, results)

    def test_parse_address_args_bulk(self):
        file_contents = "8.8.8.8\n8.8.4.4\nand maybe an ip in the middle like 10.0.0.5\nend"
        supplied_args = ["-b", "ip_list.txt"]
        args = parse_args(supplied_args)
        with mock.patch("builtins.open", mock.mock_open(read_data=file_contents)):
            results = parse_address_args(args)
        expected = ["8.8.8.8", "8.8.4.4", "10.0.0.5"]
        self.assertEquals(expected, results)
