=======================
Content packaging HOWTO
=======================

Outernet content packages are ZIP files that have a specific layout and a
metadata file. The outernet-metadata package provides tools for laying out the
directory structure and creating the metadata file. Creating a ZIP file from
that is a simple matter of zipping up everything.

Gathering content
=================

We won't go into details of how to obtain or create content as there are many
different tools and techniques and each are optimized for different scenarios.
Some general notes are:

- All links inside the content package must be relative
- There must be a single page that serves as home

Relative links
--------------

Let's say we have the following folder structure::

    package/
      |--foo/
      |   |--bar/
      |   |   |--bar.html
      |   |   \--bar.png
      |   \-foo.html
      \--index.html

The ``package`` folder contains an ``index.html`` file. We say the
``index.html`` is at the top-level or root of the package. The ``package``
folder also contains ``foo`` subfolder, and it contains ``bar`` subfolder and
``foo.html``. Finally, ``bar`` folder contains two files ``bar.png`` and
``bar.html``.

Now, if we want to link to ``bar.png`` from ``index.html``, we would use this
code::

    <img src="foo/bar/bar.png">

Or if we want to link to ``foo.html`` from ``index.html``, we would do
something like this::

    <a href="foo/foo.html">Foo</a>

Linking back to ``index.html`` from ``foo.html`` is done by using double-dots
to reference the parent folder::

    <a href="../index.html">Home</a>

For multiple levels of parent folders, we just add more double-dot-slash
combinations. For instance, if we want to link to ``index.html`` from
``bar.html``, we can do it like this::

    <a href="../../index.html">Home</a>

What we can't do is refer to the package root as just ``/``.

Home page
---------

Each package, regardless of whether it only contains a single HTML or multiple
HTML files, needs a home page. This is the first page that gets loaded when
user opens the content in Librarian.

The simplest way to take care of this is to make your homepage ``index.html``
at the top-level folder of your package.

We will talk more about it later, but for now remember that you need one, and
what you called it.

The metadata
============

Metadata is used to identify and classify your content inside Librarian. To
generate the metadata file, you can use the ``metagen`` command that was
installed by this package. 

There are several ways to use ``metagen``. Simplest (but not easiest) is to
simply run it, and it generates the metadata that you can copy and paste into
the editor and edit. Slightly more complex is the guided mode, in which you are
asked series of questions. We recommend you use the guided mode as it offers
more information on what each of the metadata fields does.

Before you begin, a note about URLs. Each URL maps to a unique ID for the
content, and you cannot use the same URL for different content. For content
that originates from the Internet, this is not a problem, as they normally have
unique URLs. For content that you created yourself and will exist only on
Outernet, this is a problem, because you have to make up a new URL each time.
To prevent clashes between URLs, use this convention::

    outernet://my-personal-site.com/

The part that says 'my-personal-site.com' is like a domain name on the Internet
(like 'google.com'). In fact, if you own a site on the web, you can use that
as your Outernet domain. Don't use 'http://' for content that only lives on
Outernet, though.

    outernet://my-personal-site.com/my-awesome-content
    outernet://my-personal-site.com/more-awesome-content

Now that we got that out of the way, open your command console (Command Prompt, 
terminal, etc) and type::

    metagen -p -g

Now read the explanations and type in the appropriate values.

When you are done, you will end up with a folder that has a cryptic name (for
the technical reader, it's an MD5 hash of the URL) like
``3bd97bbcb5a13980be4b7ed301b46810``. Inside this folder, you will find a
single ``index.json`` file. This file contains the metadata in JSON_ format.

Full introduction to JSON is outside the scope of this document, but here's a
light tour:

Field names (also known as keys) are always enclosed in double quotes. So is
any text. Field names and their values are separated by a colon. For example::

    "title": "My awesome article"

Dates always have this format: "YYYY-MM-DD". For instance, May 12, 2014 is
written as "2014-05-12" (don't forget the 0 in single-digit months). They are
also double-quoted::

    "broadcast": "2014-05-12"

Timestamps are in this format: "YYYY-MMM-DD HH:MM:SS UTC". UTC, a.k.a.
universal time is a time zone that isn't really time zone. It is convenient
because it allows easy translation to any other time zone. If you want to know
what time in your time zone is in UTC, you can use convertors_ to do that.
Hours are in 24-hour format.

Like dates, the timestamps must be double-quoted. For instance::

    "timestamp": "2015-05-12 13:04:12 UTC"

Some values are expressed as truth statements: something is true or false. In
this case, we simply say true or false, without double-quotes. For example::

    "multipage": false

Numbers also do not need to be quoted::

    "images": 10

When you are happy with your metadata, it's time to package things up.

Adding files
============

Put your content in the folder where the ``info.json`` is located.

Perceptive reader may have spotted the "images" field in the metadta. This is
the number of image files in your content. This package provides a script that
counts the images and updates the metadata. The command is ``imgcount``.

If the name of the cryptic folder is '3bd97bbcb5a13980be4b7ed301b46810' you
run this command like so::

    imgcount -u 3bd97bbcb5a13980be4b7ed301b46810

In most command consoles, you'll find that typing just a few characters from
the beginning of the folder name and then pressing Tab key will complete the
name for you.

The command should tell you something like::

    images found: 41
    updated metadata: 3bd97bbcb5a13980be4b7ed301b46810/info.json

You can open ``info.json`` now to verify that it has indeed updated the image
count.

Zipping it up
=============

The content is now ready for zipping. Use your favorite ZIP archiver and pack
it. Make sure the name of the file is the same as the cryptic folder name. So,
if your folder is named '3bd97bbcb5a13980be4b7ed301b46810', then your zip file
should be that plus '.zip': '3bd97bbcb5a13980be4b7ed301b46810.zip'.

That's it
=========

This concludes the content packaging task.

.. _JSON: http://json.org/
.. _convertors: http://www.timezoneconverter.com/cgi-bin/tzc.tzc
