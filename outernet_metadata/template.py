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
import hashlib
import datetime

import validators

from . import values
from . import inpututil

PY3 = sys.version_info >= (3, 0, 0)
if PY3:
    FILE_OPTS = {'encoding': 'utf8'}
else:
    FILE_OPTS = {}

JSON_OPTS = {'indent': 4, 'sort_keys': True}


def generate_template(**kwargs):
    """ Generate metadta template dict from given kwargs

    Keyword arguments that are passed will be added to the generated template
    only if they are named as valid keys. In all other cases, they are simply
    disregarded.

    For all required key, an empty string will be used as key value. This
    results in invalid metadata, but since the purpose of this function is to
    generate a template, no validation is performed. It is expected that the
    caller will perform any necessary validation.

    For optional keys, default values are provided as per the specification_.

    .. _specification: http://j.mp/outernet-metadata
    """
    data = {}
    for k in values.REQUIRED:
        data[k] = kwargs.get(k, '')
    for k, v in values.DEFAULTS.items():
        data[k] = kwargs.get(k, v)
    data['broadcast'] = data['broadcast'] or '$BROADCAST'
    return data


def ask_title():
    """ Get content title from user input """
    print()
    return inpututil.get_input(
        'title', validators.nonempty, help="""
        Title of the content will appear in the Outernet's content lists.
        """)


def ask_url():
    """ Gets URL from user input """
    print()
    return inpututil.get_input(
        'URL', validators.url, help="""
        URL of the content package is required in order to generate the package
        template. This URL may be a valid web URL if the content comes from the
        web, or an URL in the following form: outernet://name.com/path
        where "name" is any name of your choosing that contains only
        alphanumeric characetrs (a-z, 0-9) and "path" is an arbitrary path
        specific to your content (e.g., /my-awesome-content), and it needs to
        contain only alphanumeric characters, dashes and underscores.
        """)


def ask_keywords():
    """ Gets comma-separate keywords from user input """
    print()
    validator = validators.optional(validators.match(values.COMMASEP_RE))
    ret = inpututil.get_input(
        'keywords (optional)', validator, help="""
        Keywords are used when searching and classifying content. Keywords
        cannot contain commas, and multiple keywords are supplied separated by
        commas. For example: medical,medicine,farming,plant,biology
        """)
    kws = [s.strip() for s in ret.split(',')]
    return ','.join([s for s in kws if s])


def ask_language():
    print()
    validator = validators.optional(validators.match(values.LOCALE_RE))
    return inpututil.get_input(
        'language (optional)', validator, help="""
        Content language is specified standard ISO 639-1 locale codes. For
        example: pt_BR. You will find a list of locale codes at:

        http://loc.gov/standards/iso639-2/php/code_list.php

        Language is optional, but it allows users to search content in specific
        language, so it is recommended to set it.
        """)


def ask_publisher():
    """ Get content attribution """
    print()
    return inpututil.get_input(
        'publisher (optional)', validators.optional, help="""
        Enter the name of a person or an entity that published this content.
        You may leave this blank if not applicable.
        """)


def ask_license():
    print()
    menu, choices = inpututil.menu(values.LICENSE_NAMES)
    choices = [str(c) for c in choices]
    ret = inpututil.get_input(
        'license', validators.isin(choices), help="""
        Please choose one of the following:
        {}
        """.format(menu), wrap=False)
    return values.LICENSES[int(ret) - 1]


def ask_timestamp():
    print()
    validator = validators.optional(validators.timestamp(values.TS_FMT[:-4]))
    ret = inpututil.get_input(
        'timestamp [current time]', validator, help="""
        Timestamp usually refers to the time when content was packaged. The
        timestamp should be in UTC and in the following format: YYYY-MM-DD
        HH:MM:SS. You may leave this blank to use the current time.
        """)
    if not ret:
        return datetime.datetime.utcnow().strftime(values.TS_FMT)
    else:
        return ret + ' UTC'


def ask_archive():
    print()
    return inpututil.get_input(
        'archive [community]', validators.optional, help="""
        Archives are sections of the Outernet library. If you are not sure
        which archive this content belongs to, contact Outernet staff or leave
        blank.
        """) or 'community'


def ask_index():
    print()
    validator = validators.optional(validators.match(values.RELPATH_RE))
    return inpututil.get_input(
        'index (optional)', validator, help="""
        Index points to the file that should seve as main page of the content.
        It should be a relative path relative to the top level path of the
        content package. If left blank, index.html is assumed.
        """) or 'index.html'


def ask_multipage():
    print()
    menu, choices = inpututil.menu(['yes', 'no'])
    validator = validators.optional(validators.isin(choices))
    return inpututil.get_input(
        'multipage? [no]', validator, help="""
        If you content consists of multiple interlinked pages, select "yes".
        Multipage content must use relative paths to reference pages and assets
        within the package. Using absolute paths will have unintended
        side-effects and usually result in "Page not found" errors.

        {}
        """.format(menu)) == 1


def guide():
    data = {}
    data['title'] = ask_title()
    data['publisher'] = data['partner'] = ask_publisher()
    data['url'] = ask_url()
    data['keywords'] = ask_keywords()
    data['archive'] = ask_archive()
    data['language'] = ask_language()
    data['license'] = ask_license()
    data['timestamp'] = ask_timestamp()
    data['index'] = ask_index()
    data['multipage'] = ask_multipage()
    data['is_sponsored'] = False
    data['is_partner'] = False
    return data


def md5(s):
    """ Returns MD5 hexdigest for given string """
    h = hashlib.md5()
    h.update(s.encode('utf8'))
    return h.hexdigest()


def main():
    import os
    import argparse

    from .argutil import getparser

    parser = getparser('Generate metadata template')
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--out', '-o', metavar='PATH', default=None,
                        type=argparse.FileType('w', **FILE_OPTS),
                        help='write just the metadata to a file')
    output.add_argument('--package', '-p', action='store_true',
                        help='create a package template')
    parser.add_argument('--guided', '-g', action='store_true',
                        help='guided metadata creation')
    args = parser.parse_args()

    if args.guided:
        meta = generate_template(**guide())
    else:
        meta = generate_template()

    if args.out:
        json.dump(meta, args.out, **JSON_OPTS)
    elif args.package:
        url = meta['url'] or ask_url()
        meta['url'] = url
        id = md5(url)
        os.makedirs(id)
        with open(os.path.join(id, 'info.json'), 'w', **FILE_OPTS) as f:
            json.dump(meta, f, **JSON_OPTS)
    else:
        print(json.dumps(meta, **JSON_OPTS))


if __name__ == '__main__':
    main()
