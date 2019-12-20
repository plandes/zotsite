import logging
from pathlib import Path
import json
import sqlite3
from zensols.actioncli import persisted
from zensols.zotsite import (
    ZoteroObject,
    Item,
    Visitor,
    Library,
)

logger = logging.getLogger(__name__)


class BetterBibtexMapper(object):
    """Read the BetterBibtex database and create a mapping from item DB ids to
    citation keys.

    """
    def __init__(self, lib: Library):
        self.lib = lib

    @property
    def data(self):
        path = self.lib.data_dir / 'better-bibtex.sqlite'
        logger.info(f'reading bibtex DB at {path}')
        conn = sqlite3.connect(path)
        try:
            rows = tuple(conn.execute("""select * from `better-bibtex`"""))
            assert len(rows) == 3
            rows = tuple(filter(lambda r: r[0] == 'better-bibtex.citekey', rows))
            assert len(rows) == 1
            jstr = rows[0][1]
            return json.loads(jstr)
        finally:
            conn.close()

    @property
    @persisted('_mapping')
    def mapping(self):
        lib_id = self.lib.library_id
        data = self.data['data']
        data = filter(lambda x: x['libraryID'] == lib_id, data)
        return {x['itemID']: x['citekey'] for x in data}

    def tmp(self):
        from pprint import pprint
        pprint(self.mapping)


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
