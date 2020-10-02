#!/usr/bin/env python3

"""
__main__.py  	 - used in the SmallDevops module
Author           - 0pb
Link             - https://github.com/0pb/smalldevops
LICENSE GNU V3
"""

import sys

# if you remove this line the module crash
# it seems the __file__ need to be evaluated somewhere (it work if that line exist the devop.py file for example)


from .core.devop import devop_main

if __name__ == "__main__":
    try:
        value = __file__
        devop_main(sys.argv)
    except IndexError:
        print("error")
