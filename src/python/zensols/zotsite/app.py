"""This project exports your local Zotero library to a usable HTML website.

"""
__author__ = 'Paul Landes'

from typing import Dict, Any
from dataclasses import dataclass, field
import re
import logging
import sys
import json
from pathlib import Path
from . import ZoteroApplicationError, SiteCreator, CiteDatabase

logger = logging.getLogger(__name__)


@dataclass
class ExportApplication(object):
    """This project exports your local Zotero library to a usable HTML website.

    """
    site_creator: SiteCreator = field()
    """Creates the Zotero content web site."""

    prune_pattern: str = field(default=None)
    """A regular expression used to filter ``Collection`` nodes."""

    def _prepare_creator(self, output_dir: Path) -> Path:
        if output_dir is not None:
            self.site_creator.out_dir = output_dir
        else:
            output_dir = self.site_creator.out_dir
        if self.prune_pattern is not None:
            pat: re.Pattern = re.compile(self.prune_pattern)
            self.site_creator.prune_visitor.prune_pattern = pat
        return output_dir

    def export(self, output_dir: Path = None):
        """Generate and export the Zotero website.

        :param output_dir: the directory to dump the site; default to
                           configuration file

        """
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'exporting site: {output_dir}')
        output_dir = self._prepare_creator(output_dir)
        self.site_creator.export()

    def print_structure(self):
        """Print (sub)collections and papers in those collections as a tree."""
        self._prepare_creator(None)
        self.site_creator.print_structure()


@dataclass
class CiteApplication(object):
    """Map Zotero keys to BetterBibtex citekeys.

    """
    db: CiteDatabase = field()
    """Maps Zotero keys to BetterBibtex citekeys."""

    def lookup(self, format: str = '{itemKey}={citationKey}', key: str = None):
        """Look up a citation key and print out BetterBibtex field(s).

        :param key: key in format ``<libraryID>_<citationKey>``, standard input
                    if not given, or ``all`` for every entry

        :param format: the format of the output or ``json`` for all fields

        """
        entries: Dict[str, Dict[str, Any]] = self.db.entries
        if key is None:
            keys = map(lambda s: s.strip(), sys.stdin.readlines())
        elif key == 'all':
            keys = entries.keys()
        else:
            keys = [key]
        for key in keys:
            if key not in entries:
                raise ZoteroApplicationError(
                    f"No such entry: '{key}' in BetterBibtex database")
            entry: Dict[str, Any] = entries[key]
            if format == 'json':
                print(json.dumps(entry))
            else:
                print(format.format(**entry))


@dataclass
class PrototypeApplication(object):
    CLI_META = {'is_usage_visible': False}

    export_app: ExportApplication = field()
    cite_app: CiteApplication = field()

    def proto(self):
        self.cite_app.lookup(key='all')
