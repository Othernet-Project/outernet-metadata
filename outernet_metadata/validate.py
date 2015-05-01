#!/usr/bin/env python

"""
Validate metadata

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

import re
import sys
import json

import validators as v


try:
    FILE_ERRORS = (FileNotFoundError, OSError)
except NameError:
    FILE_ERRORS = (OSError,)


PLACEHOLDER_RE = re.compile(r'^\$[A-Z]+$')
LOCALE_RE = re.compile(r'^[a-z]{2}([_-][a-zA-Z]+)?$', re.I)
COMMASEP_RE = re.compile(r'^[\w ]+(?:, ?[\w ]+)*$', re.U)
RELPATH_RE = re.compile(r'^[^/]+(/[^/]+)*$')
TS_FMT = '%Y-%m-%d %H:%M:%S UTC'
DATE_FMT = '%Y-%m-%d'
LICENSES = ('CC-BY', 'CC-BY-ND', 'CC-BY-NC', 'CC-BY-ND-NC', 'CC-BY-SA',
            'CC-BY-NC-SA', 'GFDL', 'OPL', 'OCL', 'ADL', 'FAL', 'PD', 'OF',
            'ARL', 'ON')

SPECS = {
    'title': [v.required, v.nonempty],
    'url': [v.required, v.nonempty, v.url],
    'timestamp': [v.required, v.nonempty, v.timestamp(TS_FMT)],
    'broadcast': [v.required, v.nonempty,
                  v.OR(v.timestamp(DATE_FMT), v.match(PLACEHOLDER_RE))],
    'license': [v.required, v.isin(LICENSES)],
    'images': [v.optional(), v.istype(int), v.gte(0)],
    'language': [v.optional(''), v.nonempty, v.match(LOCALE_RE)],
    'multipage': [v.optional(), v.istype(bool)],
    'index': [v.optional(''), v.match(RELPATH_RE)],
    'keywords': [v.optional(''), v.nonempty, v.match(COMMASEP_RE)],
    'archive': [v.optional(''), v.nonempty],
    'partner': [v.optional(''), v.nonempty],
    'publisher': [v.optional(''), v.nonempty],
    'is_partner': [v.optional(), v.istype(bool)],
    'is_sponsored': [v.optional(), v.istype(bool)],
    'keep_formatting': [v.optional(), v.istype(bool)],
}

VALIDATOR = v.spec_validator(SPECS, key=lambda k: lambda obj: obj.get(k))


def load(path):
    """ Load JSON data from file """
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def validate(data):
    res = VALIDATOR(data)
    if res:
        return res
    # Additional validation that cannot be done using the specs
    if 'publisher' not in data or 'partner' not in data:
        return {}
    if data['publisher'] == data['partner']:
        return {}
    return {
        'publisher': ValueError('must match partner'),
        'partner': ValueError('must match publisher')
    }


def main():
    import os
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate metadata file')
    parser.add_argument('path', metavar='PATH', help='optional path to '
                        'metadata file (defaults to info.json in current '
                        'directory, ignored if used in a pipe',
                        default='./info.json', nargs='?')
    args = parser.parse_args()

    def validate_path(path):
        path = path.strip()
        try:
            data = load(path)
        except FILE_ERRORS:
            print('{}: file not found'.format(path), file=sys.stderr)
            sys.exit(1)
        except ValueError:
            print('{}: invalid JSON format'.format(path), file=sys.stderr)
            sys.exit(1)
        errors = validate(data)
        if errors:
            for key, err in sorted(errors.items(), key=lambda x: x[0]):
                print('{}: {}'.format(key, err), file=sys.stderr)
            return 1
        return 0

    if os.isatty(0):
        sys.exit(validate_path(args.path))
    else:
        errors = 0
        path = sys.stdin.readline()
        while path:
            errors = errors or validate_path(path)
            path = sys.stdin.readline()
        sys.exit(errors)


if __name__ == '__main__':
    main()
