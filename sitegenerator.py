#!/usr/bin/env python


import sys
import os
import shutil

import markdown


LAYOUTS_DIR = '_layouts'
RESULT_DIR = '_site'


def is_directory_valid(directory):
    """Test if current directory is usable."""
    # Currently we only test for an existing LAYOUTS_DIR
    if not os.path.exists(os.path.sep.join([directory, LAYOUTS_DIR])):
        return False
    return True


def prepare_directory(directory):
    """Prepares directory."""
    # create empty RESULT_DIR
    result_d = os.path.sep.join([directory, RESULT_DIR])
    if os.path.exists(result_d):
        shutil.rmtree(result_d)
    os.mkdir(result_d)
    # create all other directories not starting with _ in RESULT_DIR
    for file_or_dir in os.listdir(directory):
        if not file_or_dir.startswith('_'):
            src = os.path.sep.join([directory, file_or_dir])
            dst = os.path.sep.join([directory, RESULT_DIR, file_or_dir])
            if os.path.isdir(src):
                cp = shutil.copytree
            else:
                cp = shutil.copy2
            cp(src, dst)


def generate_content(directory):
    """Generate the site."""
    df = open(os.path.sep.join([directory, LAYOUTS_DIR, 'default.html']), 'r')
    layout = "".join(df.readlines())
    df.close()
    for root, dirs, files in os.walk(directory):
        if root.startswith(os.path.sep.join([directory, '_'])):
            continue
        for f in files:
            if f.split('.')[-1] in SUPPORTED_MARKUP:
                f_path = os.path.sep.join([root, f])
                html = generate_site(f_path)
                html = layout % {'content' : html, 'title' : "footitle"}
                dst_path = _src_to_destpath(f_path, directory)
                dst_file = _src_to_destfile(f_path)
                fh = open(os.path.sep.join([dst_path, dst_file]), 'w')
                fh.write(html)
                fh.close()


def _src_to_destpath(src_path, directory):
    src_path = os.path.dirname(src_path)
    src_path = os.path.abspath(src_path)
    directory = os.path.abspath(directory)
    i = len(directory)
    return os.path.sep.join([src_path[:i], RESULT_DIR, src_path[i:]])


def _src_to_destfile(filename):
    filename = os.path.basename(filename)
    i = filename.rfind('.')
    return filename[:i] + '.html'

def generate_site(f):
    """Genererate html from markup in file f (returns a string)."""
    # Currently we assume everythin is markdown
    fh = open(f, 'r')
    markup = "".join(fh.readlines())
    fh.close()
    html = markdown.markdown(markup)
    return html


def main():
    if not is_directory_valid(os.curdir):
        return 1
    prepare_directory(os.curdir)
    generate_content(os.curdir)

    return 0


if __name__ == "__main__":
    sys.exit(main())

