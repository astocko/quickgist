# quickgist

quickgist is a simple command line tool for creating gists. Files can be
specified as the sources argument or piped in via stdin. URLs are
automatically shortened with git.io.

```
usage: quickgist [-h] [-f F] [-d D] [-p P] [sources [sources ...]]

quick gist posting tool

positional arguments:
  sources     gist content sources, ex: test.txt, test1.txt test2.txt,
              test/*.txt

optional arguments:
  -h, --help  show this help message and exit
  -f F        gist filename, only used for stdin or to override single input
              filename
  -d D        gist description
  -p P        private gist
```

Examples:

    $ quickgist file.txt
    $ quickgist -d "some files" file.txt src/*.py
    $ cat foo | quickgist -f foo.txt
    $ xclip -sel c -o | quickgist
    $ quickgist -d "markdown" *.md | xclip -sel c

Notes:
    Please define an environment variable GIST_TOKEN with your
    GitHub personal access token.

    $ export GIST_TOKEN="YOUR_TOKEN_HERE"
