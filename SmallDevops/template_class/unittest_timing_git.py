#!/usr/bin/env python3

"""
unittest_timing_git.py  - used in the SmallDevops module
Author                  - 0pb
Link                    - https://github.com/0pb/smalldevops
LICENSE GNU V3
"""

# print(f"Module {__name__} imported")
# libraries
import sys
from ..core.execute_cli import *
from . import base_class_test as class_template


# --------------------------------------------------------------------------------------------


class datacls(class_template.top_class_test):
    def __init__(self, dict_config):
        self.dict_config = dict_config

    def get_discover_command(self):
        """
            (if you have python3.6)
            => str
            ['python3.6', '-m', 'unittest', 'discover', 'path/to/folder', '-v']

            (if you have python3.7)
            => str
            ['python3.7', '-m', 'unittest', 'discover', 'path/to/folder', '-v']
        """
        version_number = sys.version_info[:-2]
        current_python_version = f'python{str(version_number[0])}.{str(version_number[1])}'
        # require an __init__ file inside the directory where the test are located
        return shlex.split(f'{current_python_version} -m unittest discover {self.dict_config["directory"]} -v')

    def get_last_commit(self) -> list:
        """ return <hash string>|<author>|<short message> """
        """
            => float
            ["6eee3bf49fb019b110c6fd8d0ea419b56a38aeab", "<0pb>", "fixed issues"]
        """
        str_command = shlex.split('git log -1 --branches=* --pretty=format:"%H|<%cn>|%s"')
        # the output is on stderr
        last_log = str(execute_command_in_cmd(str_command)[1])[2:-1:]  # remove b' and last ' from byte type
        return last_log.split("|")

    def true_if_error_in_tests(self, list_stats : list) -> bool:
        """
            ['Ran 15 tests in 0.004s', 'FAILED (failure=3)']
            => bool
            false

            ['Ran 15 tests in 0.004s', 'FAILED (errors=3)']
            => bool
            true
        """
        for line in list_stats:
            if "errors" in line:
                return True
        return False

    def get_timing_test(self, list_stats : list) -> float:
        """
            ['Ran 15 tests in 0.004s', 'FAILED (failure=3)']
            => float
            0.004
        """
        try:
            time = list_stats[0].split("in ")[-1]
            time = float(time[:-1])
        except IndexError:
            time = 0.000
        return time

    def get_dict_failed_test(self, list_failure_test : list, list_failure_msg : list) -> dict:
        """
            ["test_sample1 (test.test_mini.ContainTest) ... FAIL", "test_sample2 (test.test_mini.ContainTest) ... FAIL"],
            ["===================================================================\n"
                                "FAILURE: test_sample1 (test.test_mini.ContainTest)\n etc. you get the idea"
            , "===================================================================\n
                                "FAILURE: test_sample2 (test.test_mini.ContainTest)\n etc. you get the idea"
            ]
            => { str : list[str], str : list[str], .. }
            {"test_sample1 (test.test_mini.ContainTest) ... FAIL" : ["===================================================================\n"
                                                        , "FAILURE: test_sample1 (test.test_mini.ContainTest)\n etc. you get the idea", ..]
            , "test_sample2 (test.test_mini.ContainTest) ... FAIL" : ["===================================================================\n"
                                                        , "FAILURE: test_sample2 (test.test_mini.ContainTest)\n etc. you get the idea", ..]
            }
        """
        dict_failed = {}
        for test_name, failure_message in zip(list_failure_test, list_failure_msg):
            dict_failed[test_name.split(" ... ")[0]] = failure_message.split("\n")
        return dict_failed

    def get_list_failure_test(self, list_test_name : list) -> list:
        """
            "
            test_sample1 (test.test_mini.ContainTest) ... FAIL\n
            test_sample2 (test.test_mini.ContainTest) ... FAIL\n
            \n
            ===================================================================\n
            FAILURE: test_sample1 (test.test_mini.ContainTest)\n
            ----------------------------------------------------------------------\n
            Traceback (most recent call last):\n
                [message of traceback]\n
            TypeError: expected str, bytes or os.PathLike object, not list\n
            \n
            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            ===================================================================\n
            FAILURE: test_sample2 (test.test_mini.ContainTest)\n
            ----------------------------------------------------------------------\n
            Traceback (most recent call last):\n
                [message of traceback]\n
            TypeError: expected str, bytes or os.PathLike object, not list\n
            \n
            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            FAILED (failure=3)\n
            "
            => [string, string, ..]
            ["test_sample1 (test.test_mini.ContainTest) ... FAIL", "test_sample2 (test.test_mini.ContainTest) ... FAIL"]
            ]
        """
        list_failure_tests = []
        for line in list_test_name:
            if line.endswith(" FAIL") or line.endswith(" ERROR"):
                list_failure_tests += [line]
        return list_failure_tests

    def get_failure(self, string : str) -> list:
        """
            "
            test_sample1 (test.test_mini.ContainTest) ... FAIL\n
            test_sample2 (test.test_mini.ContainTest) ... FAIL\n
            \n
            ===================================================================\n
            FAILURE: test_sample1 (test.test_mini.ContainTest)\n
            ----------------------------------------------------------------------\n
            Traceback (most recent call last):\n
                [message of traceback]\n
            TypeError: expected str, bytes or os.PathLike object, not list\n
            \n
            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            ===================================================================\n
            FAILURE: test_sample2 (test.test_mini.ContainTest)\n
            ----------------------------------------------------------------------\n
            Traceback (most recent call last):\n
                [message of traceback]\n
            TypeError: expected str, bytes or os.PathLike object, not list\n
            \n
            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            FAILED (failure=3)\n
            "
            => [string, string, ..]
            ["===================================================================\n"
                                "FAILURE: test_sample1 (test.test_mini.ContainTest)\n etc. you get the idea"
            , "===================================================================\n
                                "FAILURE: test_sample2 (test.test_mini.ContainTest)\n etc. you get the idea"
            ]
        """
        list_error = string.split("\n\n===")[1:]

        # remove Ran 10 tests in 0.00s .. etc
        list_error[-1] = list_error[-1].split("----------------------------"
                       "------------------------------------------\nRan")[0]
        return list_error

    def get_test_names(self, string : str) -> list:
        """
            "
            test_sample1 (test.test_mini.ContainTest) ... FAIL\n
            test_sample2 (test.test_mini.ContainTest) ... ok\n
            \n
            ===================================================================\n
            FAILURE: test_sample1 (test.test_mini.ContainTest)\n
            ----------------------------------------------------------------------\n
            Traceback (most recent call last):\n
                [message of traceback]\n
            TypeError: expected str, bytes or os.PathLike object, not list\n
            \n
            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            FAILED (failure=3)\n
            "
            => [string, string, ..]
            ["test_sample1 (test.test_mini.ContainTest) ... FAIL", "test_sample2 (test.test_mini.ContainTest) ... ok"]
        """
        list_string = string.split("\n\n")[0]
        list_test = list_string.split("\n")
        return list_test

    def get_statistics(self, string : str) -> list:
        """
            "
            test_sample1 (test.test_mini.ContainTest) ... FAIL\n
            test_sample2 (test.test_mini.ContainTest) ... ok\n
            \n
            ===================================================================\n
            FAILURE: test_sample1 (test.test_mini.ContainTest)\n
            ----------------------------------------------------------------------\n
            Traceback (most recent call last):\n
                [message of traceback]\n
            TypeError: expected str, bytes or os.PathLike object, not list\n
            \n
            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            FAILED (failure=3)\n
            "
            => [string, string]
            ['Ran 15 tests in 0.092s', 'FAILED (failure=3)']
        """
        stats = string.split("\n\n")[-2:]
        list_stats = [stats[0].split("\n")[-1], stats[1].split("\n")[0]]
        return list_stats

    def get_list_success_test(self, list_test_name : list) -> list:
        """
            "
            test_sample1 (test.test_mini.ContainTest) ... ok\n
            test_sample2 (test.test_mini.ContainTest) ... ok\n
            test_sample3 (test.test_mini.ContainTest) ... FAIL\n

            ----------------------------------------------------------------------\n
            Ran 15 tests in 0.092s\n
            \n
            FAILED (failure=3)\n
            "
            => [string, string, ..]
            ['test_sample1 (test.test_mini.ContainTest) ... ok', 'test_sample2 (test.test_mini.ContainTest) ... ok']
        """
        list_success_tests = []
        for line in list_test_name:
            if not line.endswith(" FAIL") and not line.endswith(" ERROR"):
                list_success_tests += [line.split(" ... ")[0]]
        return list_success_tests

    def get_output_test(self) -> str:
        return execute_command_in_cmd(self.get_discover_command())[0]
