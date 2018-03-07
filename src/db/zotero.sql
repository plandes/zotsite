select * from libraries;

select * from collections;

select * from collectionRelations;

select * from collectionItems;

select * from fulltextItems;

select * from items;

select * from itemTypes;

select * from itemAttachments;

select * from itemData;

select * from itemDataValues;

select * from itemRelations;

select * from itemNotes;

select * from creators;

select * from fields;

select * from feedItems;

select * from feeds;

select * from fieldsCombined;

select * from baseFieldMappings;

-- collection items
select *
  from collectionItems ci, collections c
  where c.collectionId = ci.collectionId
  order by ci.orderIndex;

-- item data
select f.fieldName as key, iv.value
  from items i, itemTypes it, itemData id, itemDataValues iv, fields f
  where i.itemTypeId = it.itemTypeId and
      i.itemId = id.itemId and
      id.valueId = iv.valueId and
      id.fieldId = f.fieldId and i.itemId = 2;

-- item attachements (i.e. the papers, sites etc)
select it.itemId, ia.parentItemId, it.key, iy.typeName, ia.contentType, ia.path, ci.collectionId, c.collectionName, c.parentCollectionId
  from items it, itemTypes iy
      left join itemAttachments ia on it.itemId = ia.itemId
      left join collectionItems ci on ci.itemId = it.itemId
      left join collections c on c.collectionId = ci.collectionId
  where it.itemTypeId = iy.itemTypeId
  order by ci.orderIndex;

-- item attachements all
select *
  from items it, itemTypes iy
      left join itemAttachments ia on it.itemId = ia.itemId
      left join collectionItems ci on ci.itemId = it.itemId
      left join collections c on c.collectionId = ci.collectionId
      left join itemNotes itn on it.itemId = itn.itemId
  where it.itemTypeId = iy.itemTypeId
  order by ci.orderIndex;

-- temp
select c.collectionId c_id, c.parentCollectionId c_pid, c.collectionName c_name
    from collections c
    where c.libraryId = 1;
