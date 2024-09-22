--@meta {desc: 'Zotero DB Access', date: '2024-09-18'}


-- name=select_collections
select c.collectionId c_id, ci.itemId c_iid,
        c.parentCollectionId c_pid, c.collectionName c_name
    from collections c
    left join collectionItems ci on c.collectionId = ci.collectionId
    where c.libraryId = ? and
          c.collectionName like ?

-- name=select_items_attachments
select c.collectionId c_id, c.parentCollectionId c_pid, c.collectionName c_name,
       it.itemId i_id, ia.parentItemId i_pid, it.key, iy.typeName type,
       ia.contentType content_type, ia.path,
       itn.title n_title, itn.note n_note, itn.parentItemId n_pid
  from items it, itemTypes iy
       left join itemAttachments ia on it.itemId = ia.itemId
       left join collectionItems ci on ci.itemId = it.itemId
       left join collections c on c.collectionId = ci.collectionId
       left join itemNotes itn on it.itemId = itn.itemId
  where it.itemTypeId = iy.itemTypeId and
        it.itemId not in (select itemId from deletedItems)
  order by ci.orderIndex;

-- name=select_item_metadata
select f.fieldName name, iv.value
  from items i, itemTypes it, itemData id, itemDataValues iv, fields f
  where i.itemTypeId = it.itemTypeId and
        i.itemId = id.itemId and
        id.valueId = iv.valueId and
        id.fieldId = f.fieldId and
        i.itemId = ? and
        i.itemId not in (select itemId from deletedItems);

-- name=select_item_creators
select c.firstName, c.lastName
  from itemCreators ic, creators c
  where ic.creatorID = c.creatorID and
        ic.itemID = ?
  order by ic.orderIndex;
