from abc import ABC, abstractmethod
import re
import os


class ZoteroObject(ABC):
    """Represents any collection, item etc. Zotero data object.

    """
    def __init__(self, children):
        self._children = children

    @property
    def children(self):
        return self._children

    @abstractmethod
    def get_id(self):
        pass

    @property
    def id(self):
        return self.get_id()

    def __str__(self):
        return '{} ({})'.format(self.__format_zobj__(), self.id)

    def __repr__(self):
        return self.__str__()

    def __format_zobj__(self):
        return self.name

    @property
    def title(self):
        return self.name

    @property
    def note(self):
        if hasattr(self, 'sel') and 'n_note' in self.sel:
            return self.sel['n_note']

    def short_title(self, str_len):
        """Return the short name of this object."""
        lstr = self.title
        return (lstr[:str_len] + '...') if len(lstr) > str_len else lstr

    @property
    def type(self):
        """Return the type this item is."""
        if hasattr(self, 'sel') and 'type' in self.sel:
            return self.sel['type']


class Note(ZoteroObject):
    """Represents a note Zotero data object.

    """
    def __init__(self, sel):
        self.sel = sel
        super(Note, self).__init__([])

    def get_id(self):
        return 'n' + str(self.sel['i_id'])

    @property
    def title(self):
        return self.sel['n_title']

    @property
    def name(self):
        return '<{}> [note]'.format(self.title)


class Name(object):
    def __init__(self, first: str, last: str):
        self.first = first
        self.last = last

    def __str__(self):
        return f'{self.first} {self.last}'

    def __repr__(self):
        return self.__str__()


class Item(ZoteroObject):
    """Represents an attachement object, like PDFs, site links etc.

    """
    def __init__(self, sel, children):
        self.sel = sel
        super(Item, self).__init__(children)
        self.storage_pat = re.compile('^storage:(.+)$')

    def get_db_id(self):
        return self.sel['i_id']

    def get_id(self):
        if not hasattr(self, '_id'):
            self._id = 'i' + str(self.get_db_id())
        return self._id

    def set_id(self, id):
        self._id = id

    @property
    def name(self):
        meta = self.sel['meta']
        name = 'none'
        for k in 'shortTitle title publicationTitle'.split(' '):
            if k in meta:
                name = meta[k]
                break
        return name

    @property
    def metadata(self):
        return self.sel.get('meta')

    @property
    def creators(self) -> (list, Name):
        return self.sel.get('creators')

    @property
    def file_name(self):
        path = self.sel['path']
        fname = None
        if path:
            pdir = self.sel['key']
            m = self.storage_pat.match(path)
            if m:
                fname = m.group(1)
            else:
                fname = path
            fname = '{}/{}'.format(pdir, fname)
        return fname

    def __format_zobj__(self):
        fname = self.file_name
        if fname:
            fname = ': ' + fname
        else:
            fname = ''
        its = self.sel.copy()
        its.update({'name': self.name, 'fname': fname})
        return '{name} [{type}]{fname}'.format(**its)


class Container(ZoteroObject):
    """Container class holds items and sub-collections.

    """
    def __init__(self, items, collections):
        self.items = items
        self.collections = collections
        super(Container, self).__init__(None)

    @property
    def children(self):
        ret = []
        ret.extend(self.collections)
        ret.extend(self.items)
        return ret


class Collection(Container):
    """Represents a (sub)collection, which is a container for other collections and
    items.

    """
    def __init__(self, sel, items, collections):
        self.sel = sel
        super(Collection, self).__init__(items, collections)

    def get_id(self):
        return 'c{},i{}'.format(self.sel['c_id'], self.sel['c_iid'])

    @property
    def name(self):
        return self.sel['c_name']


class Library(Container):
    """Represents the top level object that contains the root level collections.

    """
    def __init__(self, data_dir, library_id, collections):
        self.data_dir = data_dir
        self.library_id = library_id
        self.storage_dirname = 'storage'
        super(Library, self).__init__([], collections)

    def get_storage_path(self, fname=None):
        path = os.path.join(self.data_dir, self.storage_dirname)
        if fname:
            path = os.path.join(path, fname)
        return path

    def get_id(self):
        return 'l' + str(self.library_id)

    def attachment_resource(self, item):
        if item.type == 'attachment':
            return f'{self.storage_dirname}/{item.file_name}'

    @property
    def name(self):
        return 'lib'.format(self.library_id)

    @property
    def title(self):
        if self.library_id == 1:
            return 'Personal Library'
        else:
            return 'Library'


class Visitor(ABC):
    @abstractmethod
    def enter_parent(self, parent: ZoteroObject):
        """Template method for traversing down/into a node."""
        pass

    @abstractmethod
    def visit_child(self, child: ZoteroObject):
        """Template method for visiting a node."""
        pass

    @abstractmethod
    def leave_parent(self, parent: ZoteroObject):
        """Template method for traversing up/out of a node."""
        pass


class PrintVisitor(Visitor):
    def __init__(self):
        self.depth = 0

    def enter_parent(self, parent: ZoteroObject):
        print(f"{' ' * (self.depth * 4)}{str(parent)} " +
              f'({parent.__class__.__name__})')
        self.depth += 1

    def visit_child(self, child: ZoteroObject):
        pass

    def leave_parent(self, parent: ZoteroObject):
        self.depth -= 1


class Walker(object):
    def walk(self, parent, visitor: Visitor):
        """Recursively traverse the object graph."""
        visitor.enter_parent(parent)
        for c in parent.children:
            visitor.visit_child(c)
            self.walk(c, visitor)
        visitor.leave_parent(parent)
