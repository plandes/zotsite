"""This project exports your local Zotero library to a usable HTML website.

"""
__author__ = 'Paul Landes'

from typing import Iterable, Dict, Any
from dataclasses import dataclass, field
import re
import logging
import sys
import json
from pathlib import Path
from zensols.config import ConfigFactory
from . import ZoteroApplicationError, SiteCreator, ZoteroDatabase, CiteDatabase

logger = logging.getLogger(__name__)


@dataclass
class Resource(object):
    """Zotsite first class objects.

    """
    zotero_db: ZoteroDatabase = field()
    """The database access object."""

    cite_db: CiteDatabase = field()
    """Maps Zotero keys to BetterBibtex citekeys."""

    site_creator: SiteCreator = field()
    """Creates the Zotero content web site."""


@dataclass
class _Application(object):
    resource: Resource = field()
    """Zotsite first class objects."""

    def _get_keys(self, key: str, default: Iterable[str]) -> Iterable[str]:
        if key is None:
            keys = map(lambda s: s.strip(), sys.stdin.readlines())
        elif key == 'all':
            keys = default
        else:
            keys = [key]
        return keys

    def _format(self, format: str, entry: Dict[str, str]):
        if format == 'json':
            return json.dumps(entry)
        else:
            return format.format(**entry)


@dataclass
class ExportApplication(_Application):
    """This project exports your local Zotero library to a usable HTML website.

    """
    prune_pattern: str = field(default=None)
    """A regular expression used to filter ``Collection`` nodes."""

    @property
    def site_creator(self) -> SiteCreator:
        return self.resource.site_creator

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
class QueryApplication(_Application):
    """Query the Zotero database.

    """
    def find_path(self, format: str = None, key: str = None):
        """Output paths with default ``{itemKey}={path}`` for ``format``.

        :param format: the format of the output or ``json`` for all fields

        :param key: key in format ``<library ID>_<item key>``, standard input
                    if not given, or ``all`` for every entry

        """
        def strip_lib_id(s: str) -> str:
            m: re.Match = lib_id_regex.match(s)
            if m is None:
                raise ZoteroApplicationError(f'Bad item key format: {key}')
            lib_id: int = int(m.group(1))
            if lib_id != cur_lib_id:
                raise ZoteroApplicationError(
                    f'Mismatch of configured library ({cur_lib_id}) ' +
                    f'and requested in key: {lib_id}')
            return re.sub(lib_id_rm_regex, '', s)

        cur_lib_id: int = self.resource.zotero_db.library_id
        lib_id_regex: re.Pattern = re.compile(r'^(\d+)_.+')
        lib_id_rm_regex: re.Pattern = re.compile(r'^\d+_')
        paths: Dict[str, str] = self.resource.zotero_db.item_paths
        format = '{itemKey}={path}' if format is None else format
        dkeys: Iterable[str] = map(lambda k: f'{cur_lib_id}_{k}', paths.keys())
        for key in map(strip_lib_id, self._get_keys(key, dkeys)):
            if key not in paths:
                raise ZoteroApplicationError(
                    f'No item: {key} in Zotero database')
            entry: Dict[str, Any] = {
                'libraryID': cur_lib_id,
                'itemKey': key,
                'path': str(paths[key])}
            print(self._format(format, entry))


@dataclass
class CiteApplication(_Application):
    """Map Zotero keys to BetterBibtex citekeys.

    """
    def citekey(self, format: str = None, key: str = None):
        """Look up a citation key and print out BetterBibtex field(s) with
        default ``{itemKey}={citationKey}`` for ``format``.

        :param key: key in format ``<library ID>_<item key>``, standard input
                    if not given, or ``all`` for every entry

        :param format: the format of the output or ``json`` for all fields

        """
        entries: Dict[str, Dict[str, Any]] = self.resource.cite_db.entries
        format = '{itemKey}={citationKey}' if format is None else format
        for key in self._get_keys(key, entries.keys()):
            if key not in entries:
                raise ZoteroApplicationError(
                    f"No such entry: '{key}' in BetterBibtex database")
            entry: Dict[str, Any] = entries[key]
            print(self._format(format, entry))


@dataclass
class PrototypeApplication(object):
    CLI_META = {'is_usage_visible': False}

    config_factory: ConfigFactory = field()

    def proto(self):
        self.config_factory('qapp').find_path(key='all')
