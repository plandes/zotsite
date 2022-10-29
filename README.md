# Zotsite: A Zotero Export Utility

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.9][python39-badge]][python39-link]
[![Python 3.10][python310-badge]][python310-link]
[![Build Status][build-badge]][build-link]

This project exports your local [Zotero] library to a usable HTML website.
This generated website has the following features:

* Easily access your papers, site snapshots, notes from a navigation tree.
* Provides metadata from collections and attachments (i.e. referenes etc).
* Display PDF papers and website snapshot (the latter as framed).
* Search function dynamically narrows down the papers you're looking for.
* Embed links to a specific collection, article, item, note etc.
* Export only a portion of your collection with regular expressions using the
  collection name.
* [BetterBibtex] integration.
* Snazzy look and feel from the latest [Bootstrap] CSS/Javascript library.


## Documentation

See the [full documentation](https://plandes.github.io/zotsite/index.html).


## Obtaining

The easist way to install the command line program is via the `pip` installer:
```bash
pip3 install zensols.zotsite
```

Binaries are also available on [pypi].


## Process

The tool does the following:

1. Exports the meta data (directory structure, references, notes, etc) from
   your [Zotero] library.  On MacOS, this is done by querying the file system
   SQLite DB files.
2. Copies a static site that enables traversal of the exported data.
3. Copies your [Zotero] stored papers, snapshot (sites) etc.
4. Generates a navigation tree to easily find your papers/content.


## Sample Site Demonstration

See the [live demo], which provides a variety of resources found in my own
library.  *Note:* To my knowledge, all of these resources are free to
distribute and violate no laws.  If I've missed one,
please [create an issue](CONTRIBUTING.md).

## Requirements

[BetterBibtex] plugin for Zotero.


## Usage

The command line program has two modes: show configuration (a good first step)
and to create the web site.  You can see what the program is parsing from your
[Zotero] library:

```bash
zotsite print
```

To create the stand-alone site, run the program (without the angle brackets):

```bash
zotsite export
```

If your library is not in the default $HOME/zotero directory you will need to change that path by making a zotsite.conf config file:

```bash
zotsite export -c zotsite.conf
```

This will create the html files in the directory ./zotsite

See [usage](doc/usage.md) for more information.


### Configuration File

Either an environment variable `ZOTSITERC` must be set or a `-c` configuration
option must be given and point to a file to customize how the program works.
See the test [configuration file] for an example and inline comments for more
detail on how and what can be configured.


## Ubuntu and Linux Systems with Python 3.5 or Previous Version

Please [read this issue](https://github.com/plandes/zotsite/issues/4) if you
are installing a Ubuntu or any Linux system with Python 3.5 or previous
version.


## Command Line Help

Command line usage as provided with the `--help` option:

```bash
Usage: zotsite [list|export|print] [options]:

This project exports your local Zotero library to a usable HTML website.

Options:
  -h, --help                       show this help message and exit
  --version                        show the program version and exit
  --level X                        the level to set the application logger,
                                   X is one of: debug, err, info, warn
  -c, --config FILE                the path to the configuration file

Actions:
list                               list all actions and help
  --lstfmt <json|name|text>  text  the output format for the action listing

export (default)                   generate and export the zotero website
  --collection REGEX               a regular expression used to filter "collection" nodes
  -o, --outputdir DIR              the directory to dump the site; default to configuration file

print                              print (sub)collections and papers in those collections as a tree
  --collection REGEX               a regular expression used to filter "collection" nodes
```


## Attribution

This software uses:
* Python 3
* [Bootstrap] version 4
* [Tree View] for Bootstrap
* [Popper] for tooltips
* [Copy to Clipboard] function


## Screenshot

Also see the [live demo].

![Screenshot](doc/snapshot.png?raw=true "Zotero Screenshot")


## Todo

* Make the site portion a proper Javascript site.  Right now, all the `min`s
  are added in the distribution to same directory as
  the [main navigation/content](resources/site/src/js/zotero.js) file.
* Add functionality to the disabled *View* button that drills down in a paper
  and finds a PDF or site to view withouth the user having to do this.
* Use something like zotxt to make this work with a plugin rather than directly
  against the SQLite DB.


## Zotero Plugin Listing

This is listed as a [plugin] on the Zotero site.


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## License

[MIT License](LICENSE.md)

Copyright (c) 2020 - 2022 Paul Landes


<!-- links -->
[pypi]: https://pypi.org/project/zensols.zotsite/
[pypi-link]: https://pypi.python.org/pypi/zensols.zotsite
[pypi-badge]: https://img.shields.io/pypi/v/zensols.zotsite.svg
[python39-badge]: https://img.shields.io/badge/python-3.9-blue.svg
[python39-link]: https://www.python.org/downloads/release/python-390
[python310-badge]: https://img.shields.io/badge/python-3.10-blue.svg
[python310-link]: https://www.python.org/downloads/release/python-310
[build-badge]: https://github.com/plandes/zotsite/workflows/CI/badge.svg
[build-link]: https://github.com/plandes/zotsite/actions
[gitter-link]: https://gitter.im/zoterosite/zotsite
[gitter-badge]: https://badges.gitter.im/zoterosite/gitter.png

[live demo]: https://plandes.github.io/zotsite/demo/index.html

[Zotero]: https://www.zotero.org
[Bootstrap]: https://getbootstrap.com
[Tree View]: https://github.com/jonmiles/bootstrap-treeview
[Popper]: https://popper.js.org
[plugin]: https://www.zotero.org/support/plugins#website_integration
[Copy to Clipboard]: https://ourcodeworld.com/articles/read/143/how-to-copy-text-to-clipboard-with-javascript-easily
[BetterBibtex]: https://github.com/retorquere/zotero-better-bibtex
[configuration file]: test-resources/zotsite.conf
[Python regular expression]: https://docs.python.org/3/library/re.html
