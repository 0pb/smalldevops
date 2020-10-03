#!/usr/bin/env python3

"""
base_class_test.py  - used in the SmallDevops module
Author              - 0pb
Link                - https://github.com/0pb/smalldevops
LICENSE GNU V3
"""

# print(f"Module {__name__} imported")
# libraries
import datetime
from ..core.execute_cli import *
from abc import ABCMeta, abstractmethod


# --------------------------------------------------------------------------------------------


class top_class_test(metaclass=ABCMeta):
    def __init__(self, dict_config):
        self.dict_config = dict_config

    @abstractmethod
    def get_discover_command(self) -> list:
        pass

    @staticmethod
    def return_date() -> str:
        """
            => str
            2020-10-1-19-35-39
        """
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

    @abstractmethod
    def get_last_commit(self) -> list:
        pass

    @abstractmethod
    def true_if_error_in_tests(self, list_stats : list) -> bool:
        pass

    @abstractmethod
    def get_timing_test(self, list_stats : list) -> float:
        pass

    @abstractmethod
    def get_dict_failed_test(self, list_failure_test : list, list_failure_msg : list) -> dict:
        pass

    @abstractmethod
    def get_list_failure_test(self, list_test_name : list) -> list:
        pass

    @abstractmethod
    def get_failure(self, string : str) -> list:
        pass

    @abstractmethod
    def get_test_names(self, string : str) -> list:
        pass

    @abstractmethod
    def get_statistics(self, string : str) -> list:
        pass

    @abstractmethod
    def get_list_success_test(self, list_test_name : list) -> list:
        pass

    @abstractmethod
    def get_output_test(self) -> str:
        pass

    def get_execution_time(self, command : list, true_if_print_output : bool) -> float:
        """ call "usr/bin/time" (!= "time" which is shell specific) with a format real|user|sys """
        """
            ['python3', 'mini.py', 'test/Image_viewer', 'test/test_mini.py'], false
            => float
            0:00.04

            ['python3', 'mini.py', 'test/Image_viewer', 'test/test_mini.py'], true
            => float
            0:00.04

            and print the stdout output in the console, useful for log as an example
        """
        str_command = shlex.split('\\time -f "%E|%U|%S" ') + command
        output_from_execution = execute_command_in_cmd(str_command)[0]
        if true_if_print_output:
            print(output_from_execution)
        timing = str(output_from_execution).split("\n")
        return float(timing[-2].split("|")[0].split(":")[1])

    def create_dict(self) -> dict:
        """
            Those function are the one that need to be modified for other test (because the output is not similar)
            get_last_commit() may be modified to add more commit data, but it require change in javascript file later
            same for self.get_execution_time(shlexifier(self.dict_config["list_argument_module"])
                                                        , self.dict_config["show_output"])

            self.get_list_success_test(list_test_name)
            self.get_test_names(output_test)
            self.get_failure(output_test)
            self.get_statistics(output_test)

            self.get_last_commit()
            self.get_execution_time(shlexifier(self.dict_config["list_argument_module"])
                                             , self.dict_config["show_output"])
            self.true_if_error_in_tests(list_stats)
            self.get_timing_test(list_stats)
            self.get_dict_failed_test(self.get_list_failure_test(list_test_name), list_failure_msg)
        """

        output_test = self.get_output_test()
        try:
            list_test_name = self.get_test_names(output_test)
        except IndexError:
            list_test_name = []
        try:
            list_failure_msg = self.get_failure(output_test)
        except IndexError:
            list_failure_msg = []
        try:
            list_stats = self.get_statistics(output_test)
        except IndexError:
            list_stats = []

        list_success_tests = self.get_list_success_test(list_test_name)

        amount_test_failure = len(list_failure_msg)
        amount_test_success = len(list_success_tests)

        return {"total_amount" : amount_test_success + amount_test_failure  #
                , "commit" : self.get_last_commit()
                , "timing_function" : self.get_execution_time(shlexifier(self.dict_config["list_argument_module"])
                    , self.dict_config["show_output"])
                , "failed_amount" : amount_test_failure  #
                , "success_amount" : amount_test_success  #
                , "error_unittest" : self.true_if_error_in_tests(list_stats)
                , "timing_test" : self.get_timing_test(list_stats)
                , "date" : self.return_date()  #
                , "failed_test" : self.get_dict_failed_test(self.get_list_failure_test(list_test_name), list_failure_msg)
                , "success_test" : list_success_tests  #
                }
