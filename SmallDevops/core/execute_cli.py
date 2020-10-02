#!/usr/bin/env python3

"""
execute_cli.py          - used in the SmallDevops module
Author                  - 0pb
Link                    - https://github.com/0pb/smalldevops
LICENSE GNU V3
"""

# libraries
import subprocess
import shlex
import glob
import os
# print(f"Module {__name__} imported")


# --------------------------------------------------------------------------------------------


def shlexifier(str_command : str) -> list:
    """
        get a string, return a list of arg, glob is used to manage wildcard stuff, ex :
        ls -al | grep *.py
        not using shlex could allow for command injection, not using glob would fail any
        command using the * character to represent differents files/folders
        ---------------------------------------------------------------
        "python3 script.py argument1 argument2"
        =>
        ["python3", "script.py", "argument1", "argument2"]
        ---------------------------------------------------------------
        "python3 script.py path/to/folder/*"
        =>
        ["python3", "script.py", "file1", "file2"]
    """
    list_argument_shlex = shlex.split(str_command)
    new_list_arg = []
    for argument in list_argument_shlex:
        # if it's a path
        if os.path.dirname(argument):
            new_list_arg += (glob.glob(argument) or [argument])
        else:
            new_list_arg += [argument]
    return new_list_arg


def execute_command_in_cmd(list_arg : list) -> list:
    """ return [stdout str format, stderr] """
    process = subprocess.Popen(list_arg
                , stdout=subprocess.PIPE
                , stderr=subprocess.PIPE)
    stderr, stdout = process.communicate()
    return [stdout.decode("utf-8"), stderr]
