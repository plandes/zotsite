"""Contains the class that generates the website navigation data structure.

"""
__author__ = 'Paul Landes'

from typing import List, Dict, Union, Any, Type, Optional
import logging
import re
from zensols.zotsite import (
    ZoteroApplicationError, Library, Visitor,
    ZoteroObject, ItemMapper, Item, Note,
)

logger = logging.getLogger(__name__)


class NavCreateVisitor(Visitor):
    """This class creates the data structure used by the Javascript navigation
    widget in the created website.

    """
    ITEM_ICONS = {'computerProgram': 'floppy-disk',
                  'conferencePaper': 'file',
                  'journalArticle': 'file',
                  'attachment': 'paperclip',
                  'bookSection': 'book',
                  'book': 'book',
                  'report': 'font',
                  'webpage': 'bookmark',
                  'thesis': 'education',
                  'patent': 'certificate',
                  'blogPost': 'pencil'}
    UPPER = re.compile(r'([A-Z][a-z]+)')
    PDF_EXT_REGEXP = re.compile(r'.*\.pdf$')
    PDF_FULL_REGEXP = re.compile(r'^.*Full\s*[tT]ext PDF')
    CAPS_META_KEYS = set('url'.split())

    def __init__(self, lib: Library, item_mapper: ItemMapper):
        """Initialize the visitor object.

        :param lib: the object graph returned from
                    ``DatabaseReader.get_library``.

        :param item_mapper: used for file name substitution so the widget uses
                            the correct names (i.e. underscore substitution)

        """
        self._item_mapper = item_mapper
        self._root = {'nodes': []}
        self._parents = [self._root]

    @classmethod
    def _sort_nodes(cls: Type, lst: List[Dict[str, Any]],
                    by: str = 'item_title'):
        """Sort the nodes in the root node.  The default is to sort by item
        title.

        """
        assert type(lst) == list
        lst.sort(key=lambda n: n[by])
        for n in lst:
            if 'nodes' in n:
                cls._sort_nodes(n['nodes'], by)

    @property
    def primary_roots(self) -> List[Dict[str, Any]]:
        """The (root level) collections."""
        node: Dict[str, Union[str, List]] = self._root['nodes'][0]
        if 'nodes' not in node:
            raise ZoteroApplicationError(
                'No collections found; maybe too restrictive collections ' +
                'regular expression?')
        target: List[Dict[str, Any]] = node['nodes']
        self._sort_nodes(target)
        return target

    def icon_name(self, node) -> str:
        """Return the name of the icon name for ``node``."""
        icon_name = None
        if isinstance(node, Item):
            if node.type in self.ITEM_ICONS:
                icon_name = self.ITEM_ICONS[node.type]
            else:
                # :(
                logger.warning(f'no such icon found for {node.type}')
                icon_name = 'unchecked'
        elif isinstance(node, Note):
            icon_name = 'text-background'
        return icon_name

    def _munge_meta_key(self, name: str) -> str:
        if name in self.CAPS_META_KEYS:
            name = name.upper()
        elif not name.isupper():
            parts = re.split(self.UPPER, name)
            parts = filter(lambda s: len(s) > 0, parts)
            parts = map(lambda s: s.capitalize(), parts)
            name = ' '.join(parts)
        return name

    def _node_metadata(self, item: Item) -> Optional[Dict[str, Any]]:
        meta = item.metadata
        if meta is not None:
            mdarr = []
            for k, v in meta.items():
                k = self._munge_meta_key(k)
                mdarr.append((k, v))
            return mdarr

    def _find_child_resource(self, item: Item, pat: re.Pattern):
        res = tuple(filter(lambda p: p is not None and pat.match(p),
                           map(lambda c: self._item_mapper.get_resource_name(c),
                               item.children)))
        if len(res) == 1:
            return res[0]

    def _find_child_name(self, item: Item, pat: re.Pattern):
        res = tuple(filter(lambda p: p is not None and pat.match(p),
                           map(lambda c: c.name, item.children)))
        if len(res) > 0:
            for c in item.children:
                if c.name == res[0]:
                    return self._item_mapper.get_resource_name(c)

    def _create_node(self, item: Item) -> Dict[str, Any]:
        """Create a node for an item."""
        node = {'text': item.title,
                'item-id': item.id,
                'nodes': []}
        icon = self.icon_name(item)
        if icon:
            node['icon'] = 'glyphicon glyphicon-{}'.format(icon)
        node['item_title'] = item.title
        node['item_type'] = item.type
        node['item_note'] = item.note
        node['node_type'] = item.__class__.__name__.lower()
        if isinstance(item, Item):
            meta = self._node_metadata(item)
            creators = item.creators
            if meta is not None:
                node['metadata'] = meta
                res = self._item_mapper.get_resource_name(item)
                if res is None:
                    res = self._find_child_resource(item, self.PDF_EXT_REGEXP)
                if res is None:
                    res = self._find_child_name(item, self.PDF_FULL_REGEXP)
                if res is not None:
                    node['resource'] = res
            if creators is not None:
                if meta is None:
                    meta = []
                    node['metadata'] = meta
                meta.append(('Creators', ', '.join(map(str, creators))))
            if meta is not None:
                meta.sort()
        return node

    def enter_parent(self, parent: ZoteroObject):
        new_par: Dict[str, Any] = self._create_node(parent)
        cur_par: Dict[str, List[Dict]] = self._parents[-1]
        cur_par['nodes'].append(new_par)
        self._parents.append(new_par)

    def visit_child(self, child: ZoteroObject):
        pass

    def leave_parent(self, parent: ZoteroObject):
        node = self._parents.pop()
        if len(node['nodes']) == 0:
            del node['nodes']
        else:
            node['selectable'] = False
