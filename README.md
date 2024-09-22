# Zotsite: A Zotero Export Utility

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.10][python310-badge]][python310-link]
[![Python 3.11][python311-badge]][python311-link]
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

The library is typically used from the command line to create websites, but it
can also be used as an API from Python.


### Command Line

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

If your library is not in the default `~/zotero` directory you will need to
change that path by making a zotsite.conf config file.  This will create the
html files in the directory `./zotsite`:

```bash
zotsite export --collection zotsite.conf
```

A mapping of BetterBibtex citation keys to Zotero's database unique *item keys*
can be useful to scripts:
```bash
zotsite citekey -k all
```

The tool also provides a means of finding where papers are by *item key*:
```bash
zotsite docpath -k all
```

See [usage](doc/usage.md) for more information.  Command line usage as provided
with the `--help` option.


### API

The API provides access to a Python object that creates the website, can
resolve BetterBibtex citation keys to Zotero unique identifier *item keys* and
provide paths of item attachments (such as papers).

The following example come from [this working script](example/showpaper.py).

```python
>>> from typing import Dict, Any
>>> from pathlib import Path
>>> from zensols.zotsite import Resource, ApplicationFactory
# get the resource facade objects, which provides access to create the site,
# citation and path lookup methods
>>> resource: Resource = ApplicationFactory.get_resource()
# get a mapping from <library ID>_<item key> to entry dictionaries
>>> entries: Dict[str, Dict[str, Any]] = resource.cite_db.entries
# get a mapping from item key (sans library ID) to the attachment path
>>> paths: Dict[str, Path] = resource.zotero_db.item_paths
# create BetterBibtex citation key to item key mapping
>>> bib2item: Dict[str, str] = dict(map(
...     lambda e: (e['citationKey'], e['itemKey']),
...     entries.values()))
# get the item key from the citation key
>>> itemKey: str = bib2item['landesCALAMRComponentALignment2024']
# get the path using the Zotero DB item key
>>> paper_path: Path = paths[itemKey]
>>> print(paper_path)
# display the paper (needs 'pip install zensols.rend')
>>> from zensols.rend import ApplicationFactory as RendAppFactory
>>> RendAppFactory.get_browser_manager()(paper_path)
```


### Configuration File

Either an environment variable `ZOTSITERC` must be set or a `-c` configuration
option must be given and point to a file to customize how the program works.
See the test [configuration file] for an example and inline comments for more
detail on how and what can be configured.


## Screenshot

Also see the [live demo].

![Screenshot][screenshot]


## Ubuntu and Linux Systems with Python 3.5 or Previous Version

Please [read this issue](https://github.com/plandes/zotsite/issues/4) if you
are installing a Ubuntu or any Linux system with Python 3.5 or previous
version.


## Attribution

This software uses:
* Python 3
* [jQuery] version 3
* [DataTables] version 1.12
* [Bootstrap] version 4
* [Tree View] for Bootstrap
* [Popper] for tooltips
* [Copy to Clipboard] function


## Todo

* Make the site portion a proper Javascript site.  Right now, all the `min`s
  are added in the distribution to same directory as
  the [main navigation/content](resources/site/src/js/zotero.js) file.
* Use something like zotxt to make this work with a plugin rather than directly
  against the SQLite DB.


## Zotero Plugin Listing

This is listed as a [plugin] on the Zotero site.


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## Community

Please star this repository and let me know how and where you use this API.
Contributions as pull requests, feedback and any input is welcome.


## License

[MIT License](LICENSE.md)

Copyright (c) 2019 - 2023 Paul Landes


<!-- links -->
[pypi]: https://pypi.org/project/zensols.zotsite/
[pypi-link]: https://pypi.python.org/pypi/zensols.zotsite
[pypi-badge]: https://img.shields.io/pypi/v/zensols.zotsite.svg
[python310-badge]: https://img.shields.io/badge/python-3.10-blue.svg
[python310-link]: https://www.python.org/downloads/release/python-3100
[python311-badge]: https://img.shields.io/badge/python-3.11-blue.svg
[python311-link]: https://www.python.org/downloads/release/python-3110
[build-badge]: https://github.com/plandes/zotsite/workflows/CI/badge.svg
[build-link]: https://github.com/plandes/zotsite/actions
[gitter-link]: https://gitter.im/zoterosite/zotsite
[gitter-badge]: https://badges.gitter.im/zoterosite/gitter.png

[live demo]: https://plandes.github.io/zotsite/demo/index.html
[screenshot]: https://raw.githubusercontent.com/plandes/zotsite/master/doc/snapshot.png

[Zotero]: https://www.zotero.org
[jQuery]: https://jquery.com
[DataTables]: https://datatables.net
[Bootstrap]: https://getbootstrap.com
[Tree View]: https://github.com/jonmiles/bootstrap-treeview
[Popper]: https://popper.js.org
[plugin]: https://www.zotero.org/support/plugins#website_integration
[Copy to Clipboard]: https://ourcodeworld.com/articles/read/143/how-to-copy-text-to-clipboard-with-javascript-easily
[BetterBibtex]: https://github.com/retorquere/zotero-better-bibtex
[configuration file]: test-resources/zotsite.conf
[Python regular expression]: https://docs.python.org/3/library/re.html
