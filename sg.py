#!/usr/bin/env python

#    <one line to give the program's name and a brief idea of what it does.>
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

import markdown


LAYOUTS_DIR = '_layouts'
RESULT_DIR = '_site'
STATIC_DIR = '_static'

def prepare_site():
    """Prepare site generation."""
    # check if all needed files are available
    # clean RESULT_DIR
    shutil.rmtree(os.path.sep.join([os.curdir, RESULT_DIR]), True)


def generate_site():
    """Generate the dynamic part of the site."""
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
    shutil.copytree(os.path.sep.join([os.curdir, STATIC_DIR]),
            os.path.sep.join([os.curdir, RESULT_DIR]))


def save_page(path, txt):
    """Save the txt under the given filename."""
    # create directory if necessairy
    if not os.path.exists(os.path.dirname(path)):
        os.mkdir(os.path.dirname(path))
    fh = open(path, 'w')
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


def render_page(path):
    """Render page.

    It starts with the file under path, and processes it by pushing it through
    the processing pipeline. It returns a string.
    """
    fh = open(path, 'r')
    txt = "".join(fh.readlines())
    fh.close()

    fh = open(os.path.sep.join([LAYOUTS_DIR, 'default.html']), 'r')
    template = ''.join(fh.readlines())
    fh.close()

    # currently we only process markdown, other stuff can be added easyly
    txt = process_markdown(txt)
    txt = process_embed_content(template, txt)
    return txt


if __name__ == "__main__":
    prepare_site()
    copy_static_content()
    generate_site()

