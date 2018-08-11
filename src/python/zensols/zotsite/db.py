import logging
import os
import sqlite3
from zensols.zotsite.domain import Collection, Library, Item, Note

logger = logging.getLogger('zensols.zotsite.db')


class DatabaseReader(object):
    """
    Database access to Zotero store.
    """
    def __init__(self, data_dir, library_id=1):
        logger.debug('data dir: %s' % data_dir)
        self.data_dir = data_dir
        self.library_id = library_id

    def _collection_sql(self, whparams):
        return """
select c.collectionId c_id, ci.itemId c_iid, c.parentCollectionId c_pid, c.collectionName c_name
    from collections c
    left join collectionItems ci on c.collectionId = ci.collectionId
    where c.libraryId = %(library_id)s and
          c.collectionName like '%(coll_name)s'
""" % whparams

    def _item_sql(self, whparams):
        return """
select c.collectionId c_id, c.parentCollectionId c_pid, c.collectionName c_name,
       it.itemId i_id, ia.parentItemId i_pid, it.key, iy.typeName type,
       ia.contentType content_type, ia.path,
       itn.title n_title, itn.parentItemId n_pid
  from items it, itemTypes iy
      left join itemAttachments ia on it.itemId = ia.itemId
      left join collectionItems ci on ci.itemId = it.itemId
      left join collections c on c.collectionId = ci.collectionId
      left join itemNotes itn on it.itemId = itn.itemId
  where it.itemTypeId = iy.itemTypeId and
      it.itemId not in (select itemId from deletedItems)
  order by ci.orderIndex;
""" % whparams

    def _item_meta_sql(self, whparams):
        return """
select f.fieldName name, iv.value
  from items i, itemTypes it, itemData id, itemDataValues iv, fields f
  where i.itemTypeId = it.itemTypeId and
      i.itemId = id.itemId and
      id.valueId = iv.valueId and
      id.fieldId = f.fieldId and
      i.itemId = %(item_id)s and
      i.itemId not in (select itemId from deletedItems)""" % whparams

    def get_connection(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        db_file = os.path.join(self.data_dir, 'zotero.sqlite')
        logger.info('reading SQLite file: %s' % db_file)
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        return conn

    def _get_item_meta(self, item, conn, whparams):
        whparams['item_id'] = item['i_id']
        meta = {}
        for row in conn.execute(self._item_meta_sql(whparams)):
            meta[row['name']] = row['value']
        return meta

    def _select_items(self, conn, name_pat='%'):
        logger.debug('data_dir: %s' % self.data_dir)
        wparams = {'library_id': self.library_id}
        logger.debug('wparams: %s' % wparams)
        items = {}
        for item in conn.execute(self._item_sql(wparams)):
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
                meta = self._get_item_meta(item, conn, wparams)
                item['meta'] = meta
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

    def _select_collections(self, conn, name_pat='%'):
        logger.debug('data_dir: %s' % self.data_dir)
        wparams = {'library_id': self.library_id, 'coll_name': name_pat}
        logger.debug('wparams: %s' % wparams)
        colls = {}
        for row in conn.execute(self._collection_sql(wparams)):
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
        return list(filter(lambda x: x['c_pid'] is None and x['c_id'],
                           colls.values()))

    def _create_item(self, item):
        children = list(map(lambda x: self._create_item(x), item['subs']))
        if item['n_title']:
            item = Note(item)
        else:
            item = Item(item, children)
        return item

    def _create_collection(self, coll, by_cid):
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

    def _create_library(self, colls, items):
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
        return Library(self.data_dir, self.library_id, fcolls)

    def get_library(self):
        conn = self.get_connection()
        try:
            colls = self._select_collections(conn)
            items = self._select_items(conn)
            lib = self._create_library(colls, items)
        finally:
            conn.close()
        return lib
