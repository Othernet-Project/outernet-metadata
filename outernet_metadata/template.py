#!/usr/bin/env python

"""
Validate metadata

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

from . import values


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
    return data
