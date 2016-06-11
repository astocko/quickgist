#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""quickgist

quickgist is a command line tool for creating gists. Files may be piped in
or specified on the command line. Please define an environment variable
GIST_TOKEN with your GitHub personal access token.

export GIST_TOKEN="YOUR_TOKEN_HERE"

Example:
    $ quickgist file.txt
    $ quickgist -d "some files" file.txt src/*.py
    $ cat foo | quickgist -f foo.txt
"""
from __future__ import print_function
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import atexit
from collections import OrderedDict
from glob import glob
import json
import os
import sys

from orderedset import OrderedSet
import requests
from six import iteritems

__version__ = "0.1.2"


def _exit_handler():
    pass


def _shorten_url(url):
    res = requests.post('https://git.io', data={'url': url})
    if res.status_code != 201:
        sys.exit("Error shortening " + url)

    return res.headers['Location']


def _post_gist(gist_token, gist_json):
    auth = {'Authorization': 'token ' + gist_token}

    res = requests.post('https://api.github.com/gists',
                        headers=auth, data=gist_json)

    if res.status_code != 201:
        sys.exit("Error posting gist: " + res.text)

    content = json.loads(res.content.decode('utf-8'))
    return content['html_url']


def _create_gist(gist_token, description, public, files):
    gist = {"description": description,
            "public": public,
            "files": {}
            }

    for key, value in iteritems(files):
        gist['files'][key] = {'content': value}

    return _post_gist(gist_token, json.dumps(gist))


def _get_args():
    parser = ArgumentParser(prog='quickgist',
                            description='quickgist is a simple command line '
                                        'tool for creating gists.',
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('sources', nargs='*',
                        help='gist content sources, ex: test.txt, '
                             'test1.txt test2.txt, test/*.txt')
    parser.add_argument('-f', type=str, default='',
                        help='gist filename, only used for stdin '
                             'or to override single input filename')
    parser.add_argument('-d', type=str, default='', help='gist description')
    parser.add_argument('-p', default=False, action='store_true',
                        help='private gist')
    parser.add_argument('-l', default=False, action='store_true',
                        help='long url, will not shorten')
    parser.add_argument('-nl', default=False, action='store_true',
                        help='suppress newline after url, good for xclip')
    parser.add_argument('-v', action='version', version='%(prog)s ' +
                                                        __version__)
    parser.epilog = """Examples:
    $ quickgist file.txt
    $ quickgist -d "some files" file.txt src/*.py
    $ cat foo | quickgist -f foo.txt

Notes:
    Please define an environment variable GIST_TOKEN with your
    GitHub personal access token.

    $ export GIST_TOKEN="YOUR_TOKEN_HERE"
    """

    return parser.parse_args()


def _process(args):
    gist_token = ""
    try:
        gist_token = os.environ['GIST_TOKEN']
    except KeyError:
        sys.exit("Error: please set $GIST_TOKEN to your GitHub personal "
                 "access token.")

    file_map = OrderedDict()

    if args.sources:
        files = [glob(filename) for filename in args.sources]
        files = [fn for file_list in files for fn in file_list]
        files = OrderedSet([fn for fn in files if os.path.isfile(fn)])

        if not files:
            sys.exit("Error: The sources you specified are invalid.")

        for fpath in files:
            with open(fpath, 'r') as file_data:
                filename = os.path.basename(fpath)
                contents = file_data.read()
                if contents:
                    file_map[filename] = contents
    else:
        contents = sys.stdin.read()
        if not contents:
            sys.exit("Error: The source file you specified is empty.")
        file_map[args.f] = contents

    if file_map:
        return _create_gist(gist_token, args.d, not args.p, file_map)
    else:
        sys.exit("Error: The source file(s) you specified is empty.")


def _quickgist():
    atexit.register(_exit_handler)
    args = _get_args()
    try:
        url = _process(args)

        if not args.l:
            url = _shorten_url(url)

        if args.nl:
            sys.stdout.write(url)
        else:
            print(url)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    _quickgist()
