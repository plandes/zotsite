#!/usr/bin/env python

"""An example to find and optionally display a paper (attachment) using the
``zotsite`` programatic API.

"""
__author__ = 'Paul Landes'

from typing import Dict, Any
import sys
import logging
from pathlib import Path
from zensols.zotsite import Resource, ApplicationFactory

logger = logging.getLogger(__name__)


def show_paper(citationKey: str):
    """Get a file path location to a paper

    :param citationKey: the BetterBibtex citation key of the paper

    """
    # get the resource facade objects, which provides access to create the site,
    # citation and path lookup methods
    resource: Resource = ApplicationFactory.get_resource()
    # get a mapping from <library ID>_<item key> to entry dictionaries
    entries: Dict[str, Dict[str, Any]] = resource.cite_db.entries
    # get a mapping from item key (sans library ID) to the attachment path
    paths: Dict[str, Path] = resource.zotero_db.item_paths
    # create BetterBibtex citation key to item key mapping
    bib2item: Dict[str, str] = dict(map(
        lambda e: (e['citationKey'], e['itemKey']),
        entries.values()))
    # get the item key from the citation key
    itemKey: str = bib2item[citationKey]
    # get the path using the Zotero DB item key
    paper_path: Path = paths[itemKey]
    # print and try to render it in a browser (if we can)
    print(f'found item {itemKey} at {paper_path}')
    try:
        from zensols.rend import Browser
        from zensols.rend import ApplicationFactory as RendAppFactory
        browser: Browser = RendAppFactory.get_browser_manager()
        browser(paper_path)
    except Exception as e:
        logger.warning(f"could not show, try 'pip install zensols.rend': {e}")


def main(prog: str):
    if len(sys.argv) <= 1:
        print(f'usage: {prog} <better bibtex key>')
        sys.exit(1)
    citationKey: str = sys.argv[1]
    logger.info(f'finding paper with better bibtex citationKey: {citationKey}')
    show_paper(citationKey)


if (__name__ == '__main__'):
    prog: str = Path(sys.argv[0]).name
    logging.basicConfig(level=logging.WARNING,
                        format=f'{prog}: %(levelname)s: %(message)s')
    logger.setLevel(logging.INFO)
    main(prog)
