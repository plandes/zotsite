import logging
import re
from zensols.zotsite import (
    Visitor,
    ItemMapper,
    Item,
    Note,
    ZoteroObject,
)

logger = logging.getLogger(__name__)


class NavCreateVisitor(Visitor):
    """This class creates the data structure used by the Javascript navigation
    widget in the created website.

    """
    ITEM_ICONS = {'computerProgram': 'floppy-disk',
                  'conferencePaper': 'pencil',
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

    def __init__(self, lib, itemmapper: ItemMapper):
        """Initialize the visitor object.

        :param lib: the object graph returned from
        ``DatabaseReader.get_library``.
        :param itemmapper: used for file name substitution so the widget uses the
        correct names (i.e. underscore substitution)

        """
        self.lib = lib
        self.itemmapper = itemmapper
        self.root = {'nodes': []}
        self.parents = [self.root]

    @property
    def primary_roots(self):
        "Return the (root level) collections."
        return self.root['nodes'][0]['nodes']

    def icon_name(self, node):
        "Return the name of the icon name for ``node``."
        icon_name = None
        if isinstance(node, Item):
            if node.type in self.ITEM_ICONS:
                icon_name = self.ITEM_ICONS[node.type]
            else:
                # :(
                logger.warning(f'such icon found for {node.type}')
                icon_name = 'unchecked'
        elif isinstance(node, Note):
            icon_name = 'text-background'
        return icon_name

    def _munge_meta_key(self, name: str):
        if name in self.CAPS_META_KEYS:
            name = name.upper()
        elif not name.isupper():
            parts = re.split(self.UPPER, name)
            parts = filter(lambda s: len(s) > 0, parts)
            parts = map(lambda s: s.capitalize(), parts)
            name = ' '.join(parts)
        return name

    def _node_metadata(self, item: Item):
        meta = item.metadata
        if meta is not None:
            mdarr = []
            for k, v in meta.items():
                k = self._munge_meta_key(k)
                mdarr.append((k, v))
            return mdarr

    def _find_child_resource(self, item: Item, pat: re.Pattern):
        res = tuple(filter(lambda p: p is not None and pat.match(p),
                           map(lambda c: self.itemmapper.get_resource_name(c),
                               item.children)))
        if len(res) == 1:
            return res[0]

    def _find_child_name(self, item: Item, pat: re.Pattern):
        res = tuple(filter(lambda p: p is not None and pat.match(p),
                           map(lambda c: c.name, item.children)))
        if len(res) > 0:
            for c in item.children:
                if c.name == res[0]:
                    return self.itemmapper.get_resource_name(c)

    def create_node(self, item: Item):
        "Create a node for an item."
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
                res = self.itemmapper.get_resource_name(item)
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
        new_par = self.create_node(parent)
        cur_par = self.parents[-1]
        cur_par['nodes'].append(new_par)
        self.parents.append(new_par)

    def visit_child(self, child: ZoteroObject):
        pass

    def leave_parent(self, parent: ZoteroObject):
        node = self.parents.pop()
        if len(node['nodes']) == 0:
            del node['nodes']
        else:
            node['selectable'] = False
