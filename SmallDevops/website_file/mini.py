#!/usr/bin/env python3

"""
mini.py             - minify list of files
Author              - 0pb
Link                - https://github.com/0pb/minifier
LICENSE GNU V3
"""

# libraries
import sys
import os
from os import path
import re
import logginer

# --------------------------------------------------------------------------------------------
logger = logginer.set_logging(__name__, 20)  # 0 for notset, 10 for debug, ..


@logginer.logger_suppress(__name__)
def read_content(file_path : str) -> str:
    """ Read the content inside the file given as arg """
    try:
        with open(file_path) as file:
            content = file.read()
            logger.debug(f"{content}")
    except FileNotFoundError:
        return ""
    return content


def minifier(file_name : str, text : str) -> str:
    """ Minify a string """
    final_text = ""
    logger.info(f"minifying {file_name}")
    if file_name.endswith(".html"):
        final_text = re.sub(r'<!--[\S\s]*?-->', '', text)
        final_text = re.sub(r'(?<![\"\':-])(\B\s+|\s+\B)(?![\"\':-])', '', final_text)
        final_text = re.sub(r'\n', '', final_text)
    if file_name.endswith(".css"):
        final_text = re.sub(r'/\*[\S\s]*?\*/', '', text)
        final_text = re.sub(r' ', '', final_text)
        final_text = re.sub(r'\n', '', final_text)
    if file_name.endswith(".js"):
        final_text = re.sub(r'\/\/.*', '', text)
        final_text = re.sub(r'/\*[\S\s]*?\*/', '', final_text)
        final_text = re.sub(r'(?<![<>\"\'\/:-]|[return])(\B\s+|\s+\B)(?![<>\"\'\):-])', '', final_text)
        final_text = re.sub(r'\n', '', final_text)
    return final_text


@logginer.logger_suppress(__name__)
def checking_file(file_name : str) -> bool:
    """ Verify the file correspond to a certain type, and isn't bootstrap or jquery """
    file_type_accepted = [".js", ".css", ".html"]
    files_blacklist = ["bootstrap", "jquery", "chart", "luxon", "output"]
    file_name = os.path.basename(file_name)
    logger.info(f"{file_name}")

    for extension in file_type_accepted:
        for blacklisted_file in files_blacklist:
            logger.debug(f"  {blacklisted_file} {extension}")
            if blacklisted_file in file_name:
                return False
        if extension in file_name:
            return True
    return False


def get_correct_file(list_files : list) -> dict:
    """ return a list of the file name which will be minified """
    def join_path(string):
        return path.join(os.getcwd(), string)

    # check if a file type is valid or isn't bootstrap/jquery
    final_list_files = {}
    for file in list_files:
        if checking_file(file):
            final_list_files[file] = read_content(join_path(file))
    logger.info(f"List files that will be minified : {final_list_files.keys()}")
    return final_list_files


def get_list_file(path_to_files : str) -> list:
    """
    return every file in the directory (and sub directory)
    without regarde of type
    """
    logger.info(f"path_to_files : {path_to_files}")
    try:
        list_files = [os.path.join(root, name)
                    for root, dirs, files in os.walk(path_to_files)
                    for name in files]
    except IndexError:
        logger.error(f"Index error")
        return []
    logger.info(f"List files found : {list_files}")
    return list_files


def format_html_with_mini_str(str_html : str, str_css : str, str_js : str) -> str:
    """ replace the css part and js part inside the html bracket """
    try:
        result = str_html.format(css=str_css, javascript=str_js)
    except KeyError:
        result = str_html
    return result


def get_mini_str(dict_filename_content) -> str:
    """ get the string of every css, html and js """
    # get every file name and their content inside a dict
    js_text, css_text, html_text = "", "", ""

    # pass trought the list and concatenate every corresponding type except
    # for html, where it should be only one file
    for filename in dict_filename_content:
        value = minifier(filename, dict_filename_content[filename])
        if filename.endswith(".html"):
            html_text = value
        if filename.endswith(".js"):
            js_text += value
        if filename.endswith(".css"):
            css_text += value
    return [html_text, css_text, js_text]


def create_file(str_mini : str, file_name : str = "index.html") -> None:
    """ create a file """
    logger.info(f"{file_name} created")
    with open(file_name, 'wb+') as file:
        file.write((str_mini).encode('utf-8'))


def manage_args(args) -> dict:
    """
    create a dict containing configuration variables
    if html, js or css flag are on True then a separate html, js or css
    file are created.
    output manage the output file name and directory, ex :  index.html
                                                            test/index.html
    """
    config = {"output_file": "index.html"
            , "main_file": True
            , "html_flag": False
            , "css_flag": False
            , "js_flag": False}

    for arg in args:
        if "output" in arg or "-o" in arg:
            config["output_file"] = arg.split("=")[-1]
        if "-no_main" in arg or "-n" in arg:
            config["main_file"] = False
        if "-h" in arg:
            config["html_flag"] = True
        if "-c" in arg:
            config["css_flag"] = True
        if "-j" in arg:
            config["js_flag"] = True
    return config


def main(arguments) -> None:
    logger.info(f"current path : {os.getcwd()}")
    """
    take a directory folder
    get every html, js and css file inside except for bootstrap and jquery
    minify them, then create corresponding files depending on argument given
    """
    output_file = os.path.join(os.getcwd(), "index.html")

    # get the configurations variables
    config = manage_args([a for a in arguments if a.startswith("-")])
    logger.debug(f"config : {config}")

    args = [a for a in arguments if not a.startswith("-")]
    if args:
        mini_str = get_mini_str(get_correct_file(get_list_file(args[0])))
    else:
        mini_str = get_mini_str(get_correct_file(get_list_file("")))

    # check if the user want a different output directory or a different filename
    if config["output_file"]:
        output_file = os.path.join(os.getcwd(), config["output_file"])
    output_file_flag = output_file.split(".")[0]

    if not os.path.exists(os.path.dirname(os.path.abspath(output_file))):
        os.makedirs(os.path.dirname(os.path.abspath(output_file)))

    # check if the user want separate html, js or css files
    if config["html_flag"]:
        create_file((mini_str[0]), output_file_flag + "-redux.html")
    if config["css_flag"]:
        create_file((mini_str[1]), output_file_flag + ".css")
    if config["js_flag"]:
        create_file((mini_str[2]), output_file_flag + ".js")
    if config["main_file"]:
        create_file(format_html_with_mini_str(*mini_str), output_file)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except IndexError:
        print("error")
