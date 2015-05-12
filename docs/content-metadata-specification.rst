==============================
Content Metadata Specification
==============================

This document describes the content metadata (or just metadata) specification
that is used by content packaged for Outernet broadcast.

STATUS: stable, draft

CURRENT VERSION: v0.5

.. contents:: Table of Contents

Basic format
============

The metadata must be in valid JSON format. There are no requirements as to the
order of keys, indentation, etc. Non-standard keys are allowed, but none of the
Outernet software MUST NOT rely on non-standard keys.

File encoding
=============

When stored as a file, the metadata MUST be encoded using UTF-8.

Filename
========

When stored as a file inside a content zipball, the file is named 
``info.json``.

Keys
====

Keys are either required or optional. Optional keys may be completely omitted
and a default value is assumed. For backwards-compatibility purposes, keys MUST
NOT be renamed in newer specs. If a key needs to change its function, a new key
MUST be provided, and the old key MUST be given a sane default that would
satisfy older versions of software.

Some keys may be labelled as DEPRECATED. These keys are still in used according
to the specification but are planned for removal. The specification outlines
the deprecation plan for any such keys.

Some key may be labelled as FUTURE. These keys apply to all **new** content,
but legacy content is not required to have them. The specification outlines
intended software behavior with regards to both new and legacy content, and
provides a migration plan. 

Required keys
=============

title (string)
--------------

Human-readable content title.

Example::

    "Maize - Wikipedia, the free encyclopedia"

url (string)
------------

Web URL of the content source or a fictive URL for content that has no
web-based URL. It must be a RFC1738_ URL. 

Example::

    "https://en.wikipedia.org/wiki/Maize"

timestamp (string)
------------------

Time when content was fetched from source or packed (in case of custom content
packages). It must be in UTC, and the exact format is 
``'%Y-%m-%d %H:%M:%S UTC'``.

Example::

    "2015-02-25 15:00:02 UTC"

broadcast (string) **FUTURE**
-----------------------------

Date when content was put on air. Software performing the upload MUST add this
key immediately before upload as a last step after performing any other
time-consuming operations. Value must be in UTC and the exact format is
``'%Y-%m-%d'``.

Software MUST provide a default value for legacy content, and MUST accept this
key as authoritative when encountered.

Finalization date for this key is 2015 Jun 1. After this date, no content is
allowed to air without this key.

Example::

    "2015-02-25"

license (string)
----------------

Content license code. See `license codes`_ for supported values.

Software SHOULD display license information next to other metadata in the user
interface.

Example::

    "CC-BY"

Optional keys
=============

images (integer)
----------------

Number of images included in the content package.

Default::

    0

Example::

    4

language (string)
-----------------

Content language. This should be a standard locale code. Although the default
value is empty string, software may use some value as its internal default
where appropriate or where detection is possible. Software MUST make the best
effort of parse the locale code regardless of possible formatting issues (e.g.,
capitalization, non-standard separators, etc).

Default::

    ""

Example::

    "pt-BR"

multipage (boolean)
-------------------

Contents consists of multiple pages organized in a website-like structure.
Software MAY allow browsing inside the content that is marked by this metadata.

Default::

    false

Example::

    true

index (string)
--------------

Location of the file that represents the index (entry point). This value MUST
be a valid path inside the content package, and MUST use forward slashes
regardless of the platform on which content is packaged. There are no
restrictions as to the number of path components or their length, but both
packaging and rendering software SHOULD consider limitations imposed by package
container formats, target platform filesystems, and similar.

Software MUST honor the index file location when presenting the initial view of
the content.

Default::

    "index.html"

Example::

    "foo/bar.html"

keywords (string)
-----------------

List of comma-separated keywords. The keywords SHOULD BE in the document's
native language. Software MUST treat keywords case-insensitively. Whitespace
around comma MUST be ignored.

Software MAY use the keywords to facilitate searches.

Default::

    ""

Example::

    "science,farming,fertilizers,john,stanley"

archive (string)
----------------

Name of the archive to which a piece of content belongs. Any value is valid,
but only  'core' has significance, and commonly used values are 'core' and
'ephemeral'. 'curated' is also used in some places, though not in the Outernet
broadcast. The client software MAY treat the default value in any way they
like.

Default::

    "core"

Example::

    "curated"

partner (string) **DEPRECATED**
-------------------------------

Name of content partner or sponsor.

Obsoleted by publisher key. Software SHOULD prefer publisher over this key, and
treat this key as an alias until it is completely phased out. If both are found
in the same metadata they MUST have the same value.

Default::

    ""

Example::

    "Project Gutenberg"

publisher (string)
------------------

Name of the content publisher.
Obsoletes the partner key. Clients SHOULD prefer this over partner. If both are
found in the same metadata they MUST have the same value.

Software SHOULD display attribution information next to other content metadata
in user interfaces.

Software MAY use the publisher name to facilitate searching.

Default::

    ""

Example::

    "Project Gutenberg"

is_partner (boolean)
--------------------

Whether content is from a content partner.

Default::

    false

Example::

    true

is_sponsored (boolean)
----------------------

Whether content is sponsored.

Default::

    false

Example::

    true

keep_formatting (boolean)
-------------------------

Whether software displaying content should keep the original appearance.
Intended use of this flag is to prevent client software from interfering with
otherwise well-constructed stylesheets in the content.

Software MUST NOT modify content appearance when this flag is encountered and
its value is ``true``. Software MAY modify the content appearance when it
interferes with it's own, but only to the extent of preventing such
interference.

Default::

    false

Example::

    true

replaces (string)
=================

Content ID of another piece of content that this content replaces. Value of
this key should be a 32-digit hex number that identifies a piece of content.

Software MUST treat the content that is being replaced as older version of the
content with this key, and modify any references to the replaced content to
point to the replacing content.

Default::
    
    ""

Example::

    "0339a5006863ef2be9cf9bb7cc234292"

Obsolete keys
=============

The following keys have been removed from the current specification. They are
included here for completeness but should otherwise not be used.

Software MAY parse and use removed keys for backwards compatiblity when and
only when they do not interfere with current keys.

domain (string)
---------------

FQDN of the content source (usually the FQDN portion of url value. Must be a
valid FQDN.

Example::

    "en.wikipedia.org"

Changelog
=========

v0.5
----

- Added replaces key

v0.4
----

- Switching from semver to major-minor scheme

v0.3.3
------

- Explicitly specify required file encoding

v0.3.2
------

- Added broadcast FUTURE key

v0.3.1
------

- Added note on handling removed keys
- Software not required to special-case mutlipage
- Additional behavior notes to: license, publisher, keep_formatting

v0.3
----

- Adds publisher key
- Deprecates partner key
- Removes two-letter locale restriction
- Adds multipage key
- Adds index key

v0.2
----

- Removed domain key

v0.1.2
------

- Restricts language key to two-letter codes only
- Adds keywords key

v0.1.1
------

- Adds language key

v0.1
----

- Initial version.

.. _RFC1738: http://www.ietf.org/rfc/rfc1738.txt
.. _license codes: license-codes.rst
