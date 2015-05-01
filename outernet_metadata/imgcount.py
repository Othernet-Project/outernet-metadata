#!/usr/bin/env python

"""
Count images in folders

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

import os
import sys
import json

PY3 = sys.version_info >= (3, 0, 0)
if PY3:
    FILE_OPTS = {'encoding': 'utf8'}
    FILE_ERRORS = (OSError, FileNotFoundError)
else:
    FILE_OPTS = {}
    FILE_ERRORS = (OSError)


def recursematch(path, exts=['.jpg', '.jpeg', '.png', '.gif', '.svg']):
    if os.path.isfile(path):
        if os.path.splitext(path)[1] in exts:
            return 1
        return 0

    sub = os.listdir(path)
    total_found = 0
    for s in sub:
        total_found += recursematch(os.path.join(path, s), exts)
    return total_found


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Calculate the number of images in a folder')
    parser.add_argument('path', metavar='PATH', nargs='?', default='.',
                        help='path to search for images (default is to search '
                        'inside curent directory)')
    parser.add_argument('--update', '-u', action='store_true',
                        help='update the info.json found at PATH/info.json')
    args = parser.parse_args()

    count = recursematch(args.path)
    print('images found: {}'.format(count))

    if args.update:
        path = os.path.join(args.path, 'info.json')
        try:
            with open(path, 'r', **FILE_OPTS) as f:
                data = json.load(f)
            data['images'] = count
            with open(path, 'w', **FILE_OPTS) as f:
                json.dump(data, f, indent=4, sort_keys=True)
        except FILE_ERRORS:
            print('{}: read/write error, cannot update metadata'.format(path),
                  file=sys.stderr)
            sys.exit(1)
        except ValueError:
            print('{}: metadta could not be decoded, check syntax',
                  file=sys.stderr)
            sys.exit(1)
        print('updated metadata: {}'.format(path))
