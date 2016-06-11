#!/usr/bin/env python
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
from collections import OrderedDict
from glob import glob
import json
import os
import sys

from orderedset import OrderedSet
import requests
from six import iteritems

GIST_TOKEN = os.environ['GIST_TOKEN']


def _shorten_url(url):
    res = requests.post('https://git.io', data={'url': url})
    if res.status_code != 201:
        sys.exit("Error shortening " + url)

    return res.headers['Location']


def _post_gist(gist_json):
    auth = {'Authorization': 'token ' + GIST_TOKEN}

    res = requests.post('https://api.github.com/gists',
                        headers=auth, data=gist_json)

    if res.status_code != 201:
        sys.exit("Error posting gist: " + res.text)

    content = json.loads(res.content)
    return _shorten_url(content['html_url'])


def _create_gist(description, public, files):
    gist = {"description": description,
            "public": public,
            "files": {}
            }

    for key, value in iteritems(files):
        gist['files'][key] = {'content': value}

    return _post_gist(json.dumps(gist))


def _get_args():
    parser = ArgumentParser(prog='quickgist',
                            description='quick gist posting tool',
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('sources', nargs='*',
                        help='gist content sources, ex: test.txt, '
                             'test1.txt test2.txt, test/*.txt')
    parser.add_argument('-f', type=str, default='',
                        help='gist filename, only used for stdin '
                             'or to override single input filename')
    parser.add_argument('-d', type=str, default='', help='gist description')
    parser.add_argument('-p', type=bool, default=False, help='private gist')
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


def _quickgist():
    args = _get_args()
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
        print(_create_gist(args.d, not args.p, file_map))
    else:
        sys.exit("Error: The source file(s) you specified is empty.")


if __name__ == "__main__":
    _quickgist()
