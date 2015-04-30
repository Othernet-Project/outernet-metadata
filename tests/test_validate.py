"""
Tests for outernet_metaget()validate.validate() function

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import itertools

import outernet_metadata.validate as mod


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
    # V(False),
    # V('foo', invalid=True),
    V('', invalid=True),
    V(remove=True),
]


META_VALUES = {
    'title': [
        V('foo'),
        V('', invalid=True),
        # V(None, invalid=True),
        # V(remove=True, invalid=True),
    ],
    'url': [
        V('http://example.com/'),
        # V('https://example.com/'),
        # V('http://123.456.789.012/'),
        # V('http://example.com:8080/'),
        # V('outernet://foo.bar/'),
        # V('ftp://example.com/'),
        # V('ftps://example.com/'),
        # V('foo', invalid=True),
        # V('outernet://foo/', invalid=True),
        V('', invalid=True),
        # V(None, invalid=True),
        # V(remove=True, invalid=True),
    ],
    'timestamp': [
        V('2015-04-29 13:22:00 UTC'),
        # V('2015-04-29', invalid=True),
        V('', invalid=True),
        # V(None, invalid=True),
        # V(remove=True, invalid=True),
    ],
    'broadcast': [
        V('2015-04-29'),
        V('$BROADCAST'),
        V('', invalid=True),
        # V(None, invalid=True),
        # V(remove=True, invalid=True),
    ],
    'license': [
        V('CC-BY'),
        # V('CC-BY-ND'),
        # V('CC-BY-NC'),
        # V('CC-BY-ND-NC'),
        # V('CC-BY-SA'),
        # V('CC-BY-NC-SA'),
        # V('GFDL'),
        # V('OPL'),
        # V('OCL'),
        # V('ADL'),
        # V('FAL'),
        # V('PD'),
        # V('OF'),
        # V('ARL'),
        # V('ON'),
        V('foo', invalid=True),
        # V('', invalid=True),
        # V(None, invalid=True),
        # V(remove=True, invalid=True),
    ],
    'images': [
        V(3),
        # V('foo', invalid=True),
        V('', invalid=True),
        V(remove=True),
    ],
    'language': [
        # V(''),
        # V('en'),
        V('pt_BR'),
        # V('pr_br'),
        # V('pt-br'),
        # V('sr_Latn'),
        # V('sr-Latn'),
        V('foo', invalid=True),
        # V('foo_bar', invalid=True),
        # V('foo-bar', invalid=True),
        V(remove=True),
    ],
    'index': [
        # V(''),
        V('index.html'),
        # V('foo/index.html'),
        # V('foo/'),
        V('/index.html', invalid=True),
        # V('/foo', invalid=True),
        # V('/foo/index.html', invalid=True),
        V(remove=True),
    ],
    'keywords': [
        # V(''),
        V('foo,bar,baz'),
        V(remove=True),
    ],
    'archive': [
        # V(''),
        V('core'),
        V(remove=True),
    ],
    'partner': [
        # V('', must=lambda this, data: data.get('publisher') == ''),
        V('foo', must=lambda this, data: data.get('publisher') == this),
        # V('bar', must=lambda this, data: data.get('publisher') == this),
        V(remove=True, must=lambda this, data: 'publisher' not in data),
    ],
    'publisher': [
        # V('', must=lambda this, data: data.get('partner') == ''),
        V('foo', must=lambda this, data: data.get('partner') == this),
        # V('bar', must=lambda this, data: data.get('partner') == this),
        V(remove=True, must=lambda this, data: 'partner' not in data),
    ],
    'multipage': optional_bool_vals,
    'is_partner': optional_bool_vals,
    'is_sponsored': optional_bool_vals,
    'keep_formatting': optional_bool_vals,
}


def metadata_fixtures():
    keys = sorted(META_VALUES.keys())  # using sorted for predictable tests
    pairs = [[(k, v) for v in META_VALUES[k]] for k in keys]
    combinations = itertools.product(*pairs)
    for c in combinations:
        data = {}
        xf = False
        musts = []
        for k, v in c:
            if v.invalid:
                xf = True
            if v.must:
                musts.append((v.val, v.must))
            if v.remove:
                continue
            data[k] = v.val
        for v, must in musts:
            xf = xf or not must(v, data)
        yield data, xf


def test_validation():
    for data, exp_failure in metadata_fixtures():
        if exp_failure:
            assert mod.validate(data) != {}
        else:
            assert mod.validate(data) == {}
