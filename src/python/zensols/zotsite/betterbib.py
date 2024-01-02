"""A class that replaces item IDs with BetterBibtex IDs

"""
__author__ = 'Paul Landes'

from typing import Dict, Any
import logging
import json
import sqlite3
from zensols.persist import persisted
from zensols.zotsite import ZoteroObject, Item, Visitor, Library

logger = logging.getLogger(__name__)


class BetterBibtexMapper(object):
    """Read the BetterBibtex database and create a mapping from item DB ids to
    citation keys.

    """
    def __init__(self, lib: Library):
        lib_id = lib.library_id
        path = lib.data_dir / 'better-bibtex.sqlite'
        logger.info(f'reading bibtex DB at {path}')
        conn = sqlite3.connect(':memory:')
        conn.execute('ATTACH DATABASE ? AS betterbibtex', (str(path),))
        try:
            rows = tuple(conn.execute("""select itemID, citationKey from betterbibtex.`citationkey` where libraryID = ?""", (int(lib_id),)))
            self.data = rows
        finally:
            conn.close()
    @property
    @persisted('_mapping')
    def mapping(self) -> Dict[str, Any]:
        return {x[0]: x[1] for x in self.data}

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
