#!/usr/bin/env python

#    sg.py -- small, static website generator
#    Copyright (C) 2010  Bastian Venthur
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import shutil
import string
import codecs
import re
import logging

import markdown


LAYOUTS_DIR = '_layouts'
RESULT_DIR = '_site'
STATIC_DIR = '_static'

DEFAULT_LAYOUT = os.path.sep.join([LAYOUTS_DIR, 'default.html'])
DEFAULT_LAYOUT_HTML = """
<html>
    <head></head>
    <body>$content</body>
</html>
"""


def prepare_site():
    """Prepare site generation."""
    logging.info("Checking if all needed dirs and files are available.")
    # check if all needed dirs and files are available
    for directory in LAYOUTS_DIR, STATIC_DIR:
        if not os.path.exists(directory):
            logging.warning("Directory '%s' does not exist, creating it." % directory)
            os.mkdir(directory)
    if not os.path.exists(DEFAULT_LAYOUT):
        logging.warning("File '%s' does not exist, creating it." % DEFAULT_LAYOUT)
        filehandle = open(DEFAULT_LAYOUT, 'w')
        filehandle.write(DEFAULT_LAYOUT_HTML)
        filehandle.close()
    # clean RESULT_DIR
    shutil.rmtree(os.path.sep.join([os.curdir, RESULT_DIR]), True)


def generate_site():
    """Generate the dynamic part of the site."""
    logging.info("Generating Site.")
    for root, dirs, files in os.walk(os.curdir):
        # ignore directories starting with _
        if root.startswith(os.path.sep.join([os.curdir, '_'])):
            continue
        for f in files:
            if f.endswith(".markdown"):
                path = os.path.sep.join([root, f])
                html = render_page(path)
                filename = path.replace(".markdown", ".html")
                save_page(dest_path(filename), html)


def copy_static_content():
    """Copy the static content to RESULT_DIR."""
    logging.info("Copying static content.")
    shutil.copytree(os.path.sep.join([os.curdir, STATIC_DIR]),
            os.path.sep.join([os.curdir, RESULT_DIR]))


def save_page(path, txt):
    """Save the txt under the given filename."""
    # create directory if necessairy
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    fh = codecs.open(path, 'w', 'utf-8')
    fh.write(txt)
    fh.close()


def dest_path(path):
    """Convert the destination path from the given path."""
    base_dir = os.path.abspath(os.curdir)
    path = os.path.abspath(path)
    if not path.startswith(base_dir):
        raise Exception("Path not in base_dir.")
    path = path[len(base_dir):]
    return os.path.sep.join([base_dir, RESULT_DIR, path])


def process_markdown(txt):
    """Convert given txt to html using markdown."""
    html = markdown.markdown(txt)
    return html


def process_embed_content(template, content):
    """Embedd content into html template."""
    txt = string.Template(template)
    html = txt.safe_substitute({'content' : content})
    return html


def process_embed_meta(template, content):
    """Embedd meta info into html template."""
    txt = string.Template(template)
    html = txt.safe_substitute(content)
    return html


def get_meta(txt):
    """Parse meta information from text if available and return as dict.

    meta information is a block imbedded in "---\n" lines having the format: 

        key: value

    both are treated as strings the value starts after the ": " end ends with
    the newline.
    """
    SEP = '---\n'
    meta = dict()
    if txt.count(SEP) > 1 and txt.startswith(SEP):
        stuff = txt[len(SEP):txt.find(SEP, 1)]
        txt = txt[txt.find((SEP), 1)+len(SEP):]
        for i in stuff.splitlines():
            if i.count(':') > 0:
                key, value = i.split(':', 1)
                value = value.strip()
                meta[key] = value
    return meta, txt


def check_unused_variables(txt):
    """Search for unused $foo variables and print a warning."""
    template = '\\$[_a-z][_a-z0=9]*'
    f = re.findall(template, txt)
    if len(f) > 0:
        logging.warning("Unconsumed variables in template found: %s" % f)


def render_page(path):
    """Render page.

    It starts with the file under path, and processes it by pushing it through
    the processing pipeline. It returns a string.
    """
    logging.debug("Rendering %s" % path)
    fh = codecs.open(path, 'r', 'utf-8')
    txt = "".join(fh.readlines())
    fh.close()

    fh = codecs.open(DEFAULT_LAYOUT, 'r', 'utf-8')
    template = ''.join(fh.readlines())
    fh.close()

    # get meta information
    meta, txt = get_meta(txt)

    # currently we only process markdown, other stuff can be added easyly
    txt = process_markdown(txt)
    txt = process_embed_content(template, txt)
    txt = process_embed_meta(txt, meta)
    check_unused_variables(txt)
    return txt


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s\t%(message)s")
    prepare_site()
    copy_static_content()
    generate_site()

