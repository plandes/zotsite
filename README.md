# Zotsite

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.7][python37-badge]][python37-link]
[![Python 3.8][python38-badge]][python38-link]
[![Python 3.9][python39-badge]][python39-link]
[![Build Status][build-badge]][build-link]
[![Gitter chat][gitter-badge]][gitter-link]

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


## Usage

The command line program has two modes: show configuration (a good first step)
and to create the web site.  You can see what the program is parsing from your
[Zotero] library:

```bash
zotsite print
```

To create the stand-alone site, run the program (without the angle brackets):

```bash
zotsite export -o <sitedir>
```

See [usage](doc/usage.md) for more information.


## Ubuntu and Linux Systems with Python 3.5 or Previous Version

Please [read this issue](https://github.com/plandes/zotsite/issues/4) if you
are installing a Ubuntu or any Linux system with Python 3.5 or previous
version.


## Command Line Help

Command line usage as provided with the `--help` option:

```sql
Usage: zotsite <list|export|print|tmp> [options]

Options:
--version             show program's version number and exit
-h, --help            show this help message and exit
-w NUMBER, --whine=NUMBER
add verbosity to logging
-c FILE, --config=FILE
configuration file
Actions:
export  Export
-o, --outputdir <string>  ./zotsite  the directory to output the website
--collection <string>                regular expression pattern to match collections

print   Print structure
--collection <string>                regular expression pattern to match collections
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
  the [main navigation/content](src/site/js/zotero.js) file.
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

Copyright (c) 2020 Paul Landes


<!-- links -->
[build-link]: https://github.com/plandes/zotsite/actions
[build-badge]: https://github.com/plandes/zotsite/workflows/CI/badge.svg
[gitter-link]: https://gitter.im/zoterosite/zotsite
[gitter-badge]: https://badges.gitter.im/zoterosite/gitter.png

[pypi]: https://pypi.org/project/zensols.zotsite/
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

[pypi-badge]: https://img.shields.io/pypi/v/zensols.zotsite.svg
[pypi-link]: https://pypi.python.org/pypi/zensols.zotsite
[python37-badge]: https://img.shields.io/badge/python-3.7-blue.svg
[python37-link]: https://www.python.org/downloads/release/python-370
[python38-badge]: https://img.shields.io/badge/python-3.8-blue.svg
[python38-link]: https://www.python.org/downloads/release/python-380
[python39-badge]: https://img.shields.io/badge/python-3.9-blue.svg
[python39-link]: https://www.python.org/downloads/release/python-390
