#!/usr/bin/env python2
# encoding: utf-8

# programmed by: Kiss Sándor Ádám
# kisssandoradam@gmail.com
# idea and a lots of help: Dr. Szathmáry László
# Project started on 2013. december 13 midnight
# University of Debrecen


"""
This script generates index.html files to every directory and subdirectory
starting from the specified directory. Every html file consist of a table
with the following columns:
icon file_name last_modification_time file_size description

It is designed to look like the output of apache web server.
"""

import os
import re
import utils
import config
import argparse
from time import gmtime, strftime
from jinja2 import Environment, FileSystemLoader


TEMPLATE_ENVIRONMENT = Environment(autoescape=False,
                                   loader=FileSystemLoader('templates'),
                                   trim_blocks=False)

def create_ipynb_link(filename):
    link = 'http://nbviewer.ipython.org/urls/'
    if config.GITHUB_IO_BASE_URL.startswith('https://'):
        link = link + config.GITHUB_IO_BASE_URL[8:]
    elif config.GITHUB_IO_BASE_URL.startswith('http://'):
        link = link + config.GITHUB_IO_BASE_URL[7:]
    pattern = "Public_github.io"
    findex = filename.find(pattern)
    link = link + filename[findex+len(pattern):]
    return link


def get_open_url(filename):
    link = []

    if os.path.isfile(filename):
        ext = os.path.splitext(filename)[1]
        if ext == '.ipynb' :
            link.append(create_ipynb_link(filename))
            link.append('nbview')
    else:
        link.append('')
        link.append('')

    return link


def sizeof_fmt(filesize_in_bytes):
    """Converts file size to human readable format."""

    num = float(filesize_in_bytes)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if num < 1024.0 and x == 'bytes':
            return int(num)
        elif num < 1024.0:
            return "{0:.2f}&nbsp;{1}".format(num, x)
        num /= 1024.0


def get_icon_name(filename):
    """Returns the name of the icon that belongs to the file or directory."""

    if filename == "../index.html":
        return "back.gif"
    elif os.path.isdir(filename):
        return "folder.gif"
    else:
        for extension, icon in config.extensions.iteritems():
            # if the file extension is recognised return the correct icon
            match = re.search(extension + "$", filename)
            if match:
                return icon

    # unknown filename extension
    return "unknown.gif"


class Data(object):
    """Represents a file or a directory."""

    def __init__(self, name, dirpath):
        self.name = name
        self.dirpath = dirpath
        try:
            self.abspath = os.path.join(self.dirpath, self.name)
            self.date = strftime("%Y-%m-%d&nbsp;%H:%M", gmtime(60 * 60 + os.path.getmtime(self.abspath)))
            self.icon = get_icon_name(self.abspath)
            self.open = get_open_url(self.abspath)
        except OSError:
            self.abspath = dirpath
            self.date = ""
            self.size = "-"
            self.url = "../index.html"
            self.icon = get_icon_name(self.url)
            self.open = get_open_url(self.abspath)


    def __cmp__(self, other):
        """Compares instances by their names."""
        return cmp(self.name, other.name)


    def __str__(self):
        """Returns the absolute path of the file or directory."""
        return self.abspath


class Directory(Data):
    """Represents a parsed directory."""

    def __init__(self, dirname, dirpath):
        super(Directory, self).__init__(dirname, dirpath)
        self.size = "-"
        relpath = os.path.relpath(dirpath, dirpath)
        self.url = os.path.join(os.path.join(relpath, dirname), "index.html")


class File(Data):
    """Represents a parsed file."""

    def __init__(self, filename, dirpath):
        super(File, self).__init__(filename, dirpath)
        self.size = sizeof_fmt(os.path.getsize(self.abspath))
        self.url = filename


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def get_context(datas, root, current_directory, relpath):
    return {
        'datas' : datas,
        'root' : root,
        'current_directory' : current_directory,
        'font' : ( "monospace" if config.MONOSPACED_FONTS else "" ),
        'SHOW_SERVER_INFO' : config.SHOW_SERVER_INFO,
        'server_info' : config.SERVER_INFO,
        'index_of' : ("" if relpath == "." else relpath),
        'link_to_icons' : config.DROPBOX_LINK_TO_ICONS
    }


def create_index_html(path_to_starting_directory):
    """Creates an index.html file in every directory and subdirectory."""

    number_of_processed_files = 0
    number_of_processed_dirs = 0
    number_of_generated_index_htmls = 0

    for dirpath, dirnames, filenames in os.walk(path_to_starting_directory):
        if config.HIDE_HIDDEN_ENTRIES and os.path.basename(dirpath).startswith("."):
            continue

        if config.HIDE_INDEX_HTML_FILES:
            filenames = [item for item in filenames if not item == "index.html"]

        if config.HIDE_HIDDEN_ENTRIES:
            dirnames = [dirname for dirname in dirnames if not dirname.startswith(".")]
            filenames = [filename for filename in filenames if not filename.startswith(".")]

        dirnames = [dirname for dirname in dirnames if not dirname == "icons"]

        parent = [Data("Parent Directory", "../")]

        directories = [Directory(dirname, dirpath) for dirname in dirnames]
        directories.sort()
        number_of_processed_dirs += len(directories)

        files = [File(filename, dirpath) for filename in filenames]
        files.sort()
        number_of_processed_files += len(files)

        context = get_context(datas = parent + directories + files,
                              root = path_to_starting_directory,
                              current_directory = dirpath,
                              relpath = os.path.relpath(dirpath, path_to_starting_directory))

        html = render_template('template.html', context)

        file_2 = os.path.join(dirpath, "index.html")

        if os.path.exists(file_2):
            with open(file_2) as f:
                r_f = f.read()
                if not html == r_f:
                    with open(file_2, "w") as f2:
                        f2.write(html)
                        number_of_generated_index_htmls += 1
        else:
            with open(file_2, "w") as f2:
                f2.write(html)
                number_of_generated_index_htmls += 1

    total_processed_items = number_of_processed_dirs + number_of_processed_files
    print "Total processed files and directories: {count}".format(count = total_processed_items)
    print "Total index.html files generated: {count}".format(count = number_of_generated_index_htmls)


def main():
    print "Static HTML file browser for Dropbox"

    parser = argparse.ArgumentParser()

    parser.add_argument("location",
                        help="path to the Public folder of your Dropbox folder.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--install",
                       action="store_true",
                       help="prepares your Dropbox folder by copying icons to the specified directory.\
                             This directory can be set up in config.py configuration file.")
    group.add_argument("--clean",
                       action="store_true",
                       help="cleans your Dropbox directory by deleting index.html files.")

    args = parser.parse_args()

    if args.install:
        utils.install(args.location)
        exit(0)

    if args.clean:
        utils.cleanup(args.location)
        exit(0)

    create_index_html(args.location)


#############################################################################

if __name__ == "__main__":
    main()
