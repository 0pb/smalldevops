#!/usr/bin/env python3

"""
devop.py            - used in the SmallDevops module
Author              - 0pb
Link                - https://github.com/0pb/smalldevops
LICENSE GNU V3
"""

# libraries
import sys
import os
import json
import shutil
from importlib import import_module


# --------------------------------------------------------------------------------------------


class cd:
    """ Context manager for changing the current working directory in a safe way """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def import_module_template(base_path : str, template_folder_name : str, path_external_template : str = "") -> list:
    """ import dinamically module, so that a module can be added without adding import folder.module """
    list_module = {}
    if path_external_template:
        sys.path.append(os.path.dirname(path_external_template))
        list_module[os.path.basename(path_external_template)[:-3]] = import_module(f"{os.path.basename(path_external_template)[:-3]}")
    else:
        import_module(f"{os.path.basename(base_path)}.{template_folder_name}")
        template_path = os.path.join(base_path, template_folder_name)
        # template_path = f"{template_folder_name}"
        list_file_folder = [os.path.join(root, name)
                            for root, dirs, files in os.walk(template_path) for name in files]
        for file in list_file_folder:
            if os.path.dirname(file) == template_path and os.path.basename(file) != "__init__.py":
                list_module[os.path.basename(file)[:-3]] = import_module(f"{os.path.basename(base_path)}.{template_folder_name}.{os.path.basename(file)[:-3]}")
    return list_module


def create_json(dict_unittest : dict, output_path : str):
    """ get a json object from the dict in argument, then write the file given in output_path (may be json or js for example) """
    json_dump = json.dumps(dict_unittest, sort_keys=True, indent=1)
    if not os.path.isfile(output_path):
        output_text = '['
        if ".js" in os.path.basename(output_path):
            output_text = 'var data = ['
        if ".json" in os.path.basename(output_path) :
            output_text = '['
        with open(output_path, "w+") as file:
            file.write(output_text)

    """
        get last line and remove it :
        when adding another text to the end of the file, mean the
        json object is not "closed"
        ex :
            [{
                "commit": [
                    "Ap4Hkx42js"
                ],
                ...
                "total_amount": 13
            }]

        the last line is "}]"" and therefore need to be replaced by "},{""
        when adding another dict in the file
    """
    with open(output_path, "r") as file:
        lines = file.readlines()
        if len(lines) > 1:
            lines = lines[:-1]
    with open(output_path, "w") as file:
        file.write("".join(lines))
        if len(lines) > 1:
            file.write('},' + f'{json_dump}' + ']')
        else:
            file.write(f'{json_dump}' + ']')
    return json_dump


def devop_main(args : list) -> None:
    """
        python -m SmallDevops "[command to execute]"|create_website [list arg]
                    -dir
                    -show
                    -output
                    -nooutput
                    -template
                    -path_template

        list argument possible =
            "-dir" : cd inside that dir for executing the script given as command
                     is required if you execute a script from another folder
                ex: -dir=/relative/path/script
                    -dir=/absolute/path/to/different/script

            "-show" : show the output from the command executed, ex a script that print
                    "hello" to the console will then print "hello
                                                            json created
                                                            devop script done"
            ex: -show

            "-output" : create the output file in the corresponding folder
                        if the output is a path (/absolute/path/), then a output.js will be created at that
                        location
                        if the output is a path with a file name (/absolute/path/filename.js) which mean an
                        extension, then the file "filename.js" will be created at that path
                        if the output is simply a file name (filename.js) the file "filename.js" will be
                        created in the folder where the SmallDevops script has been executed, NOT in the folder
                        in the "-dir" option
                ex: -output=/absolute/path/folder/
                    -output=/relative/path/data.js
                    -output=/relative/path/data.random_ext
                    -output=data.output

            "-nooutput" : doesn't create an output file
                ex: -nooutput

            "-template" : use the corresponding template, require -path_template
                ex: -template=pytest_timing_git

            "-path_template" : fetch the corresponding template, require -template
                ex: -path_external_template=/absolute/path/to/template

        =========================================================================================
        -----------------------------------------------------------------------------------------
        Exemple of tree :

        top_folder
            ├─── file.py
            ├─── folder_with_files
            │       ├─── file1.ext
            │       └─── file2.ext
            └─── sub_folder
                    └─── sub_folder_file.py

        Exemple of use :
        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 file.py"
        =>
        - execute "python3 file.py" in /top_folder
        - create a file output.js in /top_folder
        - eventually create other file from the command "python3 file.py" in /top_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 file.py" -nooutput
        =>
        - execute "python3 file.py" in /top_folder
        - eventually create other file from the command "python3 file.py" in /top_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 file.py" -output=other_name_output.js
        =>
        - execute "python3 file.py" in /top_folder
        - create a file other_name_output.js in /top_folder
        - eventually create other file from the command "python3 file.py" in /top_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 file.py folder_with_files/*" -output=other_name_output.js
        =>
        - execute "python3 file.py folder_with_files/file1.ext folder_with_files/file2.ext" in /top_folder
        - create a file other_name_output.js in /top_folder
        - eventually create other file from the command "python3 file.py" in /top_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 sub_folder_file.py" -dir=/sub_folder
        =>
        - execute "python3 sub_folder_file.py" in /top_folder/sub_folder
        - create a file output.js in /top_folder
        - eventually create other file from the command "python3 sub_folder_file.py" in /top_folder/sub_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 file.py" -output=/absolute/path/top_folder/folder_with_files/special_json_file.json
        =>
        - execute "python3 file.py" in /top_folder
        - create a file special_json_file.json in /absolute/path/top_folder/folder_with_files/
        - eventually create other file from the command "python3 file.py" in /top_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 file.py" -output=/absolute/path/top_folder/folder_with_files/output.json
        =>
        - execute "python3 file.py" in /top_folder
        - create a file output.json in /absolute/path/top_folder/folder_with_files/
        - eventually create other file from the command "python3 file.py" in /top_folder

        -----------------------------------------------------------------------------------------
        current directory = /top_folder
        python -m SmallDevops "python3 other_folder.py" -dir=/absolute/path/to/other_folder/ \
                        -output=/absolute/path2/to/another_folder/
        =>
        - execute "python3 other_folder.py" in /absolute/path/to/other_folder/
        - create a file output.js in /absolute/path2/to/another_folder/
        - eventually create other file from the command "python3 other_folder.py" in /top_folder
        -----------------------------------------------------------------------------------------
        =========================================================================================


        don't forget to write post-commit or post-receive in .git/hooks, exemple :

        #!/bin/sh
        exec python -m SmallDevops "python3 script_to_execute.py" -output=/absolute/path/to/file/
    """
    path_module = os.path.dirname(args[0])

    # get every path eventually needed
    directory = os.getcwd()
    for arg in args:
        if args == "create_website":
            if len(args) > 2:
                shutil.copyfile(os.path.join(path_module, "website_file", "file.html"), os.path.join(args[-1], "file.html"))
            else:
                shutil.copyfile(os.path.join(path_module, "website_file", "file.html"), os.path.join(os.getcwd(), "file.html"))
            print("file.html created")
            return

    args = args[1:]
    true_if_json = True
    true_if_show_output_execution = False
    json_file_path = os.path.join(directory, "output.js")
    current_template = "unittest_timing_git"
    path_external_template = ""

    list_args = [a for a in args if a.startswith("-")]
    for arg in list_args:
        if "-template" in arg:
            # use the template, by default "unittest_timing_git"
            current_template = arg.split("=")[-1]
        if "-path_template" in arg:
            path_external_template = arg.split("=")[-1]
        if "-dir" in arg:
            try:
                dir_value = arg.split("=")[-1]
                if os.path.exists(dir_value):
                    directory = os.path.join(directory, dir_value)
            except FileNotFoundError:
                return "Dir doesn't exist"
        if "-nooutput" in arg:
            true_if_json = False
        if "-show" in arg:
            true_if_show_output_execution = True
        if "-output" in arg or "-o" in arg:
            json_file_path = arg.split("=")[-1]
            if os.path.isdir(json_file_path):
                json_file_path = os.path.join(json_file_path, "output.js")

    list_template = import_module_template(path_module, "template_class", path_external_template)

    dict_config = {"list_argument_module" : args[0]
                , "directory" : directory
                , "json" : true_if_json
                , "json_output_dir" : json_file_path
                , "show_output" : true_if_show_output_execution}

    """
        go into the dir directory if specified, otherwise stay on the current path
        it allow the user to execute script with more freedom, as well as compatibility.
        dir can be a relative or absolute path, the default path is absolute.
    """
    # get into the dir specified, if the option isn't used then the default (current dir) is used
    with cd(dict_config["directory"]):
        dict_data = list_template[current_template].datacls(dict_config).create_dict()
        if dict_config["json"]:
            create_json(dict_data, dict_config["json_output_dir"])
            print("json created")

    print("devop script done")


if __name__ == "__main__":
    try:
        devop_main(sys.argv[1:])
    except IndexError:
        print("error")
