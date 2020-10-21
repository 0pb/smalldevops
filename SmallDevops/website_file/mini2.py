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

# --------------------------------------------------------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))


def main(arguments) -> None:
    path_of_files = arguments[0]
    path_of_files = os.path.join(basedir, path_of_files)

    list_files = [os.path.join(root, name)
                for root, dirs, files in os.walk(path_of_files)
                for name in files]
    print(list_files)

    dict_js = {}
    dict_css = {}
    for file in list_files:
        if file.endswith(".html"):
            with open(file) as html_file:
                html_content = html_file.read()
        if file.endswith(".css"):
            with open(file) as css_file:
                dict_css[os.path.basename(file)] = css_file.read()
        if file.endswith(".js"):
            with open(file) as css_file:
                dict_js[os.path.basename(file)] = css_file.read()

    for js_file in dict_js:
        html_content = html_content.replace(f'<script src="{js_file}"></script>', f'<script>{dict_js[js_file]}</script>')
    for css_file in dict_css:
        html_content = html_content.replace(f'<link href="{css_file}" rel="stylesheet">', f'<style>{dict_css[css_file]}</style>')

    with open(os.path.join(path_of_files, "file.html"), "w+") as file:
        file.write(html_content)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except IndexError:
        print("error")
