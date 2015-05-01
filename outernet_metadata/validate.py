#!/usr/bin/env python

"""
Validate metadata

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

import sys
import json

import validators as v

from . import values

try:
    FILE_ERRORS = (FileNotFoundError, OSError)
except NameError:
    FILE_ERRORS = (OSError,)


VALIDATOR = v.spec_validator(values.SPECS,
                             key=lambda k: lambda obj: obj.get(k))


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
        usage='\n    %(prog)s PATH\n    PATH | %(prog)s',
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
