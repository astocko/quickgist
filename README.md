# quickgist

quickgist is a simple command line tool for creating gists. Files can be
specified as the sources argument or piped in via stdin. URLs are
automatically shortened with git.io.

## Install

### pypi
    pip install quickgist

### source
    git clone https://github.com/astocko/quickgist.git
    cd quickgist
    python setup.py install

## Usage

```
usage: quickgist [-h] [-f F] [-d D] [-p] [-l] [-nl] [sources [sources ...]]

quickgist is a simple command line tool for creating gists.

positional arguments:
  sources     gist content sources, ex: test.txt, test1.txt test2.txt,
              test/*.txt

optional arguments:
  -h, --help  show this help message and exit
  -f F        gist filename, only used for stdin or to override single input
              filename
  -d D        gist description
  -p          private gist
  -l          long url, will not shorten
  -nl         suppress newline after url, good for xclip
```

## Examples

    $ quickgist file.txt
    $ quickgist -d "some files" file.txt src/*.py
    $ cat foo | quickgist -f foo.txt
    $ xclip -sel c -o | quickgist
    $ quickgist -nl -d "markdown" *.md | xclip -sel c

## Notes
Please define an environment variable GIST_TOKEN with your GitHub
personal access token.

    $ export GIST_TOKEN="YOUR_TOKEN_HERE"

