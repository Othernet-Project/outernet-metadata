"""
Functions for working with program arguments

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import argparse

from . import __version__, __copyright__

VERSION = "%(prog)s v{}".format(__version__)


def getparser(desc, usage=None):
    parser = argparse.ArgumentParser(
        description=desc,
        usage=usage,
        epilog=__copyright__)
    parser.add_argument('--version', '-V', action='version', version=VERSION)
    return parser
