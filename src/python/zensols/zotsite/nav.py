from zensols.zotsite.domain import ZoteroObject, Item, Note, Collection

class NavCreateWalker(object):
    def __init__(self, lib, fscopier):
        self.lib = lib
        self.fscopier = fscopier
        self.root = {'nodes': []}
        self.parents = [self.root]

    @property
    def primary_roots(self):
        return self.root['nodes'][0]['nodes']

    def icon_name(self, node):
        if isinstance(node, Item):
            return {'computerProgram': 'floppy-disk',
                    'conferencePaper': 'file',
                    'journalArticle': 'file',
                    'attachment': 'paperclip',
                    'bookSection': 'book'}[node.type]
        elif isinstance(node, Note):
            return 'text-background'

    def create_node(self, item):
        node = {'text': item.title,
                'item-id': item.id,
                'nodes': []}
        icon = self.icon_name(item)
        if icon:
            node['icon'] = 'glyphicon glyphicon-{}'.format(icon)
        node['item_title'] = item.title
        node['item_type'] = item.type
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

    def visit_child(self, child):
        pass

    def leave_parent(self, parent):
        node = self.parents.pop()
        if len(node['nodes']) == 0:
            del node['nodes']
        else:
            node['selectable'] = False
