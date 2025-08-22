"""A class that replaces item IDs with BetterBibtex IDs

"""
__author__ = 'Paul Landes'

from typing import Dict, Any
import logging
from pathlib import Path
import sqlite3
from zensols.persist import persisted
from zensols.zotsite import ZoteroObject, Item, Visitor, Library

logger = logging.getLogger(__name__)


class BetterBibtexMapper(object):
    """Read the BetterBibtex database and create a mapping from item DB ids to
    citation keys.

    """
    def __init__(self, lib: Library):
        self.lib = lib

    @property
    @persisted('_mapping')
    def mapping(self) -> Dict[str, Any]:
        path: Path = self.lib.data_dir / 'better-bibtex.sqlite'
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'reading bibtex DB at {path}')
        conn = sqlite3.connect(':memory:')
        conn.execute('ATTACH DATABASE ? AS betterbibtex', (str(path),))
        try:
            return dict(conn.execute(
                """\
select itemID, citationKey
        from betterbibtex.`citationkey`
        where libraryID = ?""",
                [self.lib.library_id]))
        finally:
            conn.close()


class BetterBibtexVisitor(Visitor):
    """Use the ``BetterBibtexMapper`` to change the keys in mapped items to the
    respective citation keys.

    """
    def __init__(self, lib: Library):
        self.mapper = BetterBibtexMapper(lib)

    def enter_parent(self, parent: ZoteroObject):
        pass

    def visit_child(self, child: ZoteroObject):
        if isinstance(child, Item):
            dbid = child.get_db_id()
            bbid = self.mapper.mapping.get(dbid)
            if bbid is not None:
                child.set_id(bbid)
                child.metadata['citationKey'] = bbid

    def leave_parent(self, parent: ZoteroObject):
        pass
