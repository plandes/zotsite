"""Generates the the static HTML pages that make up the Zotero exported website.

"""
__author__ = 'Paul Landes'

from typing import Dict
from dataclasses import dataclass, field
import logging
import sys
import json
from pathlib import Path
from io import TextIOBase
import shutil
from zensols.config import Settings, ConfigFactory
from zensols.persist import persisted
from zensols.zotsite import (
    ZoteroApplicationError, DatabaseReader, RegexItemMapper, IdItemMapper,
    Library, Walker,
    NavCreateVisitor, FileSystemCopyVisitor, PruneVisitor, PrintVisitor,
    BetterBibtexVisitor,
)

logger = logging.getLogger(__name__)


@dataclass
class SiteCreator(object):
    """Creates the Zotero content web site.

    """
    config_factory: ConfigFactory = field()
    """The configuration factory used to create the :class:`.Walker` instance.

    """
    package: Settings = field()
    """Containes this Python package information used to create the site
    metadata.

    """
    site_resource: Path = field()
    """The (resource) path the static site files."""

    db: DatabaseReader = field()
    """The database access object."""

    prune_visitor: PruneVisitor = field()
    """A visitor that prunes collections based on a regular expression."""

    sort_walkers: Settings = field()
    """A mapping of name to a :class:`.Walker` instance definition configuration
    section.

    """
    sort: str = field(default='none')
    """whether or not to sort items, either: ``none`` or ``case`` (non-case
    might be added later).

    """
    id_mapping: bool = field(default='none')
    """How to generate unique identifiers for URLS, either ``none``, or
    `betterbib``.

    """
    file_mapping: str = field(default='item')
    """Whether to use unique item IDs for the file names or the full PDF file
    name; either: ``item`` or ``long``

    """
    out_dir: Path = field(default=None)
    """The default output directory to store the collection."""

    @property
    @persisted('_walker')
    def walker(self) -> Walker:
        walker_class_name = self.sort_walkers.get(self.sort)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'using walker: {walker_class_name}')
        if walker_class_name is None:
            raise ZoteroApplicationError(
                f'Configuration error: no such walker: {self.sort}')
        return self.config_factory(walker_class_name)

    @property
    @persisted('_library')
    def library(self) -> Library:
        lib: Library = self.db.get_library()
        if self.prune_visitor.should_walk:
            self.walker.walk(lib, self.prune_visitor)
        if self.id_mapping == 'none':
            pass
        elif self.id_mapping == 'betterbib':
            visitor = BetterBibtexVisitor(lib)
            self.walker.walk(lib, visitor)
        else:
            raise ZoteroApplicationError(
                f'Unknown ID mapping: {self.id_mapping}')
        return lib

    @property
    @persisted('_item_mapper')
    def item_mapper(self):
        if self.file_mapping == 'long':
            mapper = RegexItemMapper(self.library, r'.*\.pdf$', '[ ]')
        elif self.file_mapping == 'item':
            mapper = IdItemMapper(self.library)
        else:
            raise ZoteroApplicationError(
                f'Unknown file mapping: {self.file_mapping}')
        return mapper

    def print_structure(self, writer: TextIOBase = sys.stdout):
        """Print (sub)collections and papers in those collections as a tree."""
        self.walker.walk(self.library, PrintVisitor(writer))

    def _write_meta(self, path: Path):
        """Write version and other metadata to the website, which is used during
        rending of the site.

        """
        meta: Dict[str, str] = {'version': self.package.version or '<none>',
                                'project_name': self.package.name or '<none>'}
        js: str = f'var zoteroMeta = {json.dumps(meta)};'
        with open(path, 'w') as f:
            f.write(js)

    def _create_tree_data(self):
        """Create the table of contents/tree info used by the navigation widget.

        """
        js_dir: Path = self.out_dir / 'js'
        nav_file: Path = js_dir / 'zotero-tree-data.js'
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'creating js nav tree: {nav_file}')
        visitor = NavCreateVisitor(self.library, self.item_mapper)
        self.walker.walk(self.library, visitor)
        with open(nav_file, 'w') as f:
            f.write("var tree =\n")
            f.write(json.dumps(visitor.primary_roots, indent=2))
        meta_file = Path(js_dir, 'zotero-meta.js')
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'creating js metadata: {meta_file}')
        self._write_meta(meta_file)

    def _copy_storage(self):
        """Copy the storage contents, which is the location of the PDF (and other)
        documents that will be rendered in the site GUI.

        """
        dst = self.out_dir
        fsvisitor = FileSystemCopyVisitor(self.library, dst, self.item_mapper)
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'copying storage to {dst}')
        self.walker.walk(self.library, fsvisitor)

    def _copy_static_res(self, src: Path, dst: Path):
        """Copy static resources from the distribution package.

        :param src: the source package directory
        :param dst: the destination on the file system

        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'copy: {src} -> {dst}')
        dst.mkdir(parents=True, exist_ok=True)
        for res in src.iterdir():
            res = res.name
            src_file = src / res
            dst_file = dst / res
            if src_file.is_dir():
                self._copy_static_res(src_file, dst_file)
            else:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'copy: {src_file} -> {dst_file}')
                shutil.copyfile(src_file, dst_file)

    def _copy_static(self):
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'copying static data -> {self.out_dir}')
        res: Path = self.site_resource
        if not res.exists():
            raise ZoteroApplicationError(
                f'Missing resource directory {res}')
        for rpath in res.iterdir():
            self._copy_static_res(rpath, self.out_dir)

    def export(self):
        """Entry point method to export (create) the website.

        """
        self._copy_static()
        self._create_tree_data()
        self._copy_storage()

    def tmp(self):
        print(self.package)
