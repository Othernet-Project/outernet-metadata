"""
Tests for outernet_metadata.template module

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import pytest

import outernet_metadata.template as mod

from outernet_metadata.values import DEFAULTS


def test_generate_template():
    """
    Given no arguments, when calling generate_metadata(), then it returns
    metadata with defaults for optional keys and blanks for required keys,
    except for broadcast which should be equal to '$BROADCAST'.
    """
    required = ['title', 'url', 'timestamp', 'broadcast', 'license']
    ret = mod.generate_template()
    for k in required:
        if k == 'broadcast':
            assert ret[k] == '$BROADCAST'
        else:
            assert ret[k] == ''
    for k in ret.keys():
        if k not in required:
            assert ret[k] == DEFAULTS[k]


@pytest.mark.parametrize('kw', [
    ('title', 'Foo'),
    ('url', 'http://example.com/'),
    ('timestamp', '2015-04-29 15:22:00 UTC'),
    ('broadcast', '2015-04-29'),
    ('license', 'GFDL'),
    ('archive', 'ephemeral'),
    ('images', 12),
    ('index', 'foo.html'),
    ('is_partner', True),
    ('is_sponsored', True),
    ('keep_formatting', True),
    ('keywords', 'foo,bar'),
    ('language', 'pt_BR'),
    ('multipage', True),
    ('partner', 'ACME Inc'),
    ('publisher', 'ACME Inc'),
])
def test_generate_template_with_values(kw):
    """
    Given keyword arguments, when calling generate_metadata() with them, then
    the generated template will use the povided values for each key.
    """
    k, v = kw
    ret = mod.generate_template(**{k: v})
    assert ret[k] == v


def test_generate_template_ignored_keywords():
    """
    Given a keyword that does not appear in specs, when calling
    generate_metadata() with a keyword argument that is named after that
    keyword, then the keyword does not get added to the template.
    """
    ret = mod.generate_template(foo='bar')
    assert 'foo' not in ret
