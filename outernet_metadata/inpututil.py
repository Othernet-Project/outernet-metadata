"""
Utilities for working with user input

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

import sys
import textwrap

import validators

try:
    inp_read = raw_input
except NameError:
    inp_read = input


def menu(item_list):
    items = '\n'.join(['{:>2}) {}'.format(idx, v)
                       for idx, v in enumerate(item_list, 1)])
    choices = list(range(1, len(item_list) + 1))
    return items, choices


def rewrap(s, width=79):
    s = ' '.join([l.strip() for l in s.strip().split('\n')])
    return '\n'.join(textwrap.wrap(s, width))


def clean(s):
    return '\n'.join([l.strip() for l in s.strip().split('\n')])


def get_input(prompt, validator, error_msg='Invalid input', help=None,
              wrap=True):
    """ Asks user for inpt until valid input is obtained """
    if help:
        if wrap:
            print('{}\n'.format(rewrap(help)))
        else:
            print('{}\n'.format(clean(help)))
    val = inp_read('{}: '.format(prompt)).strip()
    if hasattr(val, 'decode'):
        val = val.decode(sys.stdin.encoding)
    try:
        validator(val)
    except ValueError:
        print(error_msg)
        return get_input(prompt, validator, error_msg)
    except validators.ReturnEarly:
        pass
    return val
