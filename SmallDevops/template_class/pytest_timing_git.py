#!/usr/bin/env python3

"""
unittest_timing_git.py  - used in the SmallDevops module
Author                  - 0pb
Link                    - https://github.com/0pb/smalldevops
LICENSE GNU V3
"""

# print(f"Module {__name__} imported")
# libraries
from ..core.execute_cli import *
from . import base_class_test as class_template


# --------------------------------------------------------------------------------------------
# --no-header
"""
pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

pytest -v --no-header /mnt/s/programmation/Website/Money_calculator/calc/in_folder
"""


class datacls(class_template.top_class_test):
    def __init__(self, dict_config):
        self.dict_config = dict_config

    def get_discover_command(self):
        """
            => str
            ['pytest', '-v', '--no-header', 'path/to/folder']
        """
        # require an __init__ file inside the directory where the test are located
        return shlex.split(f'pytest -v --no-header {self.dict_config["directory"]}')

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
        for line in list_stats:
            if "error" in line:
                return True
        return False

    def get_timing_test(self, list_stats : list) -> float:
        try:
            time = list_stats[-1]
            time = float(time[:-1])
        except IndexError:
            time = 0.000
        return time

    def get_dict_failed_test(self, list_failure_test : list, list_failure_msg : list) -> dict:
        dict_failed = {}
        for test_name, failure_message in zip(list_failure_test, list_failure_msg):
            if "FAILED" in test_name:
                dict_failed[test_name.split(" FAILED")[0]] = failure_message.split("\n")
            else:
                dict_failed[test_name.split(" ERROR")[0]] = failure_message.split("\n")
        return dict_failed

    def get_list_failure_test(self, list_test_name : list) -> list:
        list_failure_tests = []
        for line in list_test_name:
            if line.endswith(" FAILED") or line.endswith(" ERROR"):
                test_name_case_test = "".join(line.split(" ")[:-1]).split("::")[-2:]
                list_failure_tests += [test_name_case_test[1] + " " + test_name_case_test[0]]
        return list_failure_tests

    def get_failure(self, string : str) -> list:
        try:
            string_error_failure = string.split('= ERRORS =')[1]
        except IndexError:
            string_error_failure = string.split('= FAILURES =')[1]
        string_error_failure = string_error_failure.split("= short test summary info =")[0]

        # only get the error and failure
        string_error_failure = string_error_failure.split("\n")[1:-1]

        # remove the "====== failures ======" line
        new_list = []
        for line in string_error_failure:
            if "= FAILURES =" in line:
                pass
            else:
                new_list += [line]

        # remove the ====== error ====== at the first line
        list_error = ("\n".join(new_list)).split("\n_")
        return list_error

    def get_test_names(self, string : str) -> list:
        list_string = string.split("\n\n")[1].split("\n")
        new_list_string = []
        for line in list_string:
            file_class_name_result = line.split("[")[0].rstrip()
            new_list_string += [file_class_name_result]
        return new_list_string

    def get_statistics(self, string : str) -> list:
        # get the line with the stats
        list_string = string.split("\n")[-2]

        # remove the ==== on both side
        list_string = "".join(list_string.split("= ")[1]).split(" =")[0]

        # get a list with failed, passed and error and the timing
        list_string = list_string.split(" in ")
        return list_string

    def get_list_success_test(self, list_test_name : list) -> list:
        list_success_tests = []
        for line in list_test_name:
            if not line.endswith(" FAILED") and not line.endswith(" ERROR"):
                test_name_case_test = "".join(line.split(" ")[:-1]).split("::")
                if len(test_name_case_test) > 2:
                    test_name_case_test = test_name_case_test[1:]
                    list_success_tests += [test_name_case_test[1] + " " + test_name_case_test[0] + " ".join(test_name_case_test[2:])]
                else:
                    list_success_tests += [test_name_case_test[1] + " " + test_name_case_test[0]]
        return list_success_tests

    def get_output_test(self) -> str:
        # [1] get stderr
        # [0] get stdout
        return execute_command_in_cmd(self.get_discover_command())[1]
