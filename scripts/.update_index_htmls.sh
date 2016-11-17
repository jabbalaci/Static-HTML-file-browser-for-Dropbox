#!/usr/bin/env bash

# I use this script to generate the static HTML files.
# Put it in the root of the directory that you want to sync
# with github.io and execute it there.

HERE=`/bin/pwd`
cd /home/jabba/Dropbox/python/Static-HTML-file-browser-for-Dropbox
./program.py "$@" $HERE
