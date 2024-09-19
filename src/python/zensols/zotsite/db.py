"""Data access objects to the Zotero SQLite database.

"""
__author__ = 'Paul Landes'

from typing import Tuple, List, Dict, Any, Union, Optional
from dataclasses import dataclass, field
import logging
from pathlib import Path
from zensols.db import DbPersister
from . import Collection, Library, Item, Note, Name

logger = logging.getLogger(__name__)


@dataclass
class ZoteroDatabase(object):
    """Provides access to data from the Zotero database.

    """
    _persister: DbPersister = field()
    """The persister used to get the data."""

    _data_dir: Path = field()
    """The path to the ``zotero.sqlite`` database file."""

    _collection_like: str = field()
    """The SQL pattern to match against subcollection names."""

    _library_id: int = field()
    """The DB ide of the library to export."""

    def _select(self, name: str, *params) -> Tuple[Dict[str, Any], ...]:
        return self._persister.execute_by_name(
            name=f'select_{name}',
            params=params,
            row_factory='dict')

    def _select_collections(self) -> Tuple[Dict[str, Any], ...]:
        """Return items from the database.

        :param conn: the DB connection

        """
        colls: Dict[str, Any] = {}
        rows: Tuple[Dict[str, Any], ...] = \
            self._select('collections', self._library_id, self._collection_like)
        row: Dict[str, Any]
        for row in rows:
            row['subs'] = []
            colls[row['c_id']] = row
        for coll in colls.values():
            c_pid = coll['c_pid']
            if c_pid not in colls:
                coll['c_pid'] = None
                c_pid = None
            if c_pid:
                par = colls[c_pid]
                par['subs'].append(coll)
        return tuple(filter(lambda x: x['c_pid'] is None and x['c_id'],
                            colls.values()))

    def _get_item_meta(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Return the item metadata from the database.

        :param item: the item to fetch data for

        """
        meta: Dict[str, Any] = {}
        row: Dict[str, Any]
        for row in self._select('item_metadata', item['i_id']):
            meta[row['name']] = row['value']
        return meta

    def _get_item_creators(self, item: Dict[str, Any]) -> \
            Optional[Tuple[Name, ...]]:
        """Return the item metadata from the database.

        :param item: the item to fetch data for

        """
        creators: List[Name] = []
        row: Dict[str, Any]
        for row in self._select('item_creators', item['i_id']):
            name = Name(row['firstName'], row['lastName'])
            creators.append(name)
        if len(creators) > 0:
            return tuple(creators)

    def _select_items(self):
        """Return items from the database.

        :param conn: the DB connection

        """
        items: Dict[str, Any] = {}
        item: Dict[str, Any]
        for item in self._select('items_attachments'):
            item['subs'] = []
            if not item['i_pid'] and not item['c_pid']:
                item['i_pid'] = item['n_pid']
            iid = item['i_id']
            if iid in items:
                items[iid].append(item)
            else:
                items[iid] = [item]
        for itemlst in items.values():
            for item in itemlst:
                meta = self._get_item_meta(item)
                item['meta'] = meta
                creators = self._get_item_creators(item)
                item['creators'] = creators
        for itemlst in items.values():
            for item in itemlst:
                i_pid = item['i_pid']
                if i_pid in items:
                    for par in items[i_pid]:
                        par['subs'].append(item)
        flst = []
        for itemlst in items.values():
            flst.extend(itemlst)
        return flst

    def _create_item(self, item: Dict[str, Any]) -> Union[Item, Note]:
        """Return a domain object that represents an item (i.e. PDF attachement,
        link, note etc).

        """
        children = tuple(map(lambda x: self._create_item(x), item['subs']))
        if item['type'] == 'note':
            item = Note(item)
        else:
            item = Item(item, children)
        return item

    def _create_collection(self, coll: Dict[str, Any], by_cid: Dict[str, int]):
        """Return a domain object that represents a Zotero DB (sub)collection.

        :param by_cid: parent to child collection IDs

        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('processing: {} ({}, {})'.
                         format(coll['c_name'], coll['c_id'], coll['c_iid']))
        cid = coll['c_id']
        items = []
        if cid in by_cid:
            toadd = by_cid[cid]
            items.extend(toadd)
            logger.debug('children items: %d' % len(toadd))
        children = list(map(lambda x: self._create_collection(x, by_cid),
                            coll['subs']))
        items = list(map(lambda x: self._create_item(x), items))
        return Collection(coll, items, children)

    def _create_library(self, colls, items) -> Library:
        """Return a domain object that represents a Zotero DB (sub)collection.

        :param conn: the DB connection

        :param by_cid: parent to child collection IDs

        """
        by_cid = {}
        for i in items:
            cid = i['c_id']
            if cid:
                if cid in by_cid:
                    cid_lst = by_cid[cid]
                else:
                    cid_lst = []
                    by_cid[cid] = cid_lst
                cid_lst.append(i)
        fcolls = []
        for coll in colls:
            fcoll = self._create_collection(coll, by_cid)
            fcolls.append(fcoll)
        return Library(self._data_dir, self._library_id, fcolls)

    def get_library(self) -> Library:
        """Get an object graph representing the data in the Zotero database.

        """
        try:
            colls = self._select_collections()
            items = self._select_items()
            return self._create_library(colls, items)
        finally:
            # deallocate pooled connection (configured in ``obj.conf``)
            self._persister.conn_manager.dispose_all()
