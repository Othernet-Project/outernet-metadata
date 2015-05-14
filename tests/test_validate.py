"""
Tests for outernet_metaget()validate.validate() function

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import pytest

import itertools

import outernet_metadata.validator as mod


BASE_METADATA = {
    'title': 'Foo',
    'url': 'outernet://foo.bar/',
    'timestamp': '2015-04-29 13:22:00 UTC',
    'broadcast': '2015-04-29',
    'license': 'CC-BY',
    'archive': 'core',
    'images': 0,
    'index': 'index.html',
    'is_partner': False,
    'is_sponsored': False,
    'keep_formatting': False,
    'keywords': '',
    'language': '',
    'multipage': False,
    'partner': 'foo',
    'publisher': 'foo',
    'replaces': '6a5afe56ad3d69f2c5a715deda4e32c9',
}


class V:
    def __init__(self, val=None, invalid=False, remove=False, must=None):
        self.val = val
        self.invalid = invalid
        self.remove = remove
        self.must = must

    def __repr__(self):
        return 'V(%r)' % self.val


optional_bool_vals = [
    V(True),
    V(False),
    V('foo', invalid=True),
    V('', invalid=True),
    V(remove=True),
]


META_VALUES = {
    'title': [
        V('foo'),
        V('', invalid=True),
        V(None, invalid=True),
        V(remove=True, invalid=True),
    ],
    'url': [
        V('http://example.com/'),
        V('https://example.com/'),
        V('http://123.456.789.012/'),
        V('http://example.com:8080/'),
        V('outernet://foo.bar/'),
        V('ftp://example.com/'),
        V('ftps://example.com/'),
        V('foo', invalid=True),
        V('outernet://foo/', invalid=True),
        V('', invalid=True),
        V(None, invalid=True),
        V(remove=True, invalid=True),
    ],
    'timestamp': [
        V('2015-04-29 13:22:00 UTC'),
        V('2015-04-29', invalid=True),
        V('', invalid=True),
        V(None, invalid=True),
        V(remove=True, invalid=True),
    ],
    'broadcast': [
        V('2015-04-29'),
        V('$BROADCAST'),
        V('', invalid=True),
        V(None, invalid=True),
        V(remove=True, invalid=True),
    ],
    'license': [
        V('CC-BY'),
        V('CC-BY-ND'),
        V('CC-BY-NC'),
        V('CC-BY-ND-NC'),
        V('CC-BY-SA'),
        V('CC-BY-NC-SA'),
        V('GFDL'),
        V('OPL'),
        V('OCL'),
        V('ADL'),
        V('FAL'),
        V('PD'),
        V('OF'),
        V('ARL'),
        V('ON'),
        V('foo', invalid=True),
        V('', invalid=True),
        V(None, invalid=True),
        V(remove=True, invalid=True),
    ],
    'images': [
        V(3),
        V('foo', invalid=True),
        V('', invalid=True),
        V(remove=True),
    ],
    'language': [
        V(''),
        V('en'),
        V('pt_BR'),
        V('pr_br'),
        V('pt-br'),
        V('sr_Latn'),
        V('sr-Latn'),
        V('foo', invalid=True),
        V('foo_bar', invalid=True),
        V('foo-bar', invalid=True),
        V(remove=True),
    ],
    'index': [
        V(''),
        V('index.html'),
        V('foo/index.html'),
        V('foo/', invalid=True),
        V('/index.html', invalid=True),
        V('/foo', invalid=True),
        V('/foo/index.html', invalid=True),
        V(remove=True),
    ],
    'keywords': [
        V(''),
        V('foo,bar,baz'),
        V(remove=True),
    ],
    'archive': [
        V(''),
        V('core'),
        V(remove=True),
    ],
    'partner': [
        V('', invalid=True),
        V('foo'),
        V('bar', invalid=True),
        V(remove=True),
    ],
    'publisher': [
        V('', invalid=True),
        V('foo'),
        V('bar', invalid=True),
        V(remove=True),
    ],
    'replaces': [
        V('6A5AFE56AD3D69F2C5A715DEDA4E32C9'),
        V(''),
        V('foo', invalid=True),
        V(remove=True),
    ],
    'multipage': optional_bool_vals,
    'is_partner': optional_bool_vals,
    'is_sponsored': optional_bool_vals,
    'keep_formatting': optional_bool_vals,
}


def metadata_fixtures():
    keys = sorted(META_VALUES.keys())  # using sorted for predictable tests
    pairs = [[(k, v) for v in META_VALUES[k]] for k in keys]
    for k, v in itertools.chain(*pairs):
        data = BASE_METADATA.copy()
        if v.remove:
            del data[k]
        else:
            data[k] = v.val
        if v.invalid:
            data = pytest.mark.xfail(data)
        yield data


@pytest.mark.parametrize('data', metadata_fixtures())
def test_validation(data):
    assert mod.validate(data) == {}
