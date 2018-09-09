import re
import logging
from zensols.zotsite import (
    Walker,
    PatternFsCopier,
    Item,
    Note,
)

logger = logging.getLogger('zensols.zotsite.nav')


class NavCreateWalker(Walker):
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
                  'webpage': 'bookmark'}

    def __init__(self, lib, fscopier: PatternFsCopier):
        """Initialize the walker object.

        :param lib: the object graph returned from
        ``DatabaseReader.get_library``.
        :param fscopier: used for file name substitution so the widget uses the
        correct names (i.e. underscore substitution)

        """
        self.lib = lib
        self.fscopier = fscopier
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
                icon_name = 'unchecked'
        elif isinstance(node, Note):
            icon_name = 'text-background'
        return icon_name

    def create_node(self, item):
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
        if isinstance(item, Item):
            meta = item.metadata
            mdarr = []
            if meta:
                for k, v in meta.items():
                    mdarr.append([k, v])
                node['metadata'] = mdarr
                res = self.lib.attachment_resource(item)
                if res:
                    res = self.fscopier.update_file(res)
                    node['resource'] = res
        return node

    def enter_parent(self, parent):
        new_par = self.create_node(parent)
        cur_par = self.parents[-1]
        cur_par['nodes'].append(new_par)
        self.parents.append(new_par)

    def leave_parent(self, parent):
        node = self.parents.pop()
        if len(node['nodes']) == 0:
            del node['nodes']
        else:
            node['selectable'] = False
