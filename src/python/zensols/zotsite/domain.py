"""Contains domain and visitor (GoF pattern) classes.

"""
__author__ = 'Paul Landes'

from typing import Callable
import logging
from abc import ABC, abstractmethod
import re
from io import TextIOBase
from pathlib import Path
from zensols.cli import ApplicationError
from zensols.persist import persisted

logger = logging.getLogger(__name__)


class ZoteroApplicationError(ApplicationError):
    """Thrown for application errors meant to be reported by the command line.

    """
    pass


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
        super().__init__([])

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
        super().__init__(children)
        self.storage_pat = re.compile('^(?:storage|attachments):(.+)$')

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
    @persisted('_path')
    def path(self):
        abs_path = None
        path = self.sel['path']
        if path is not None:
            m = self.storage_pat.match(path)
            if m is None:
                # assume ZoteroFile is used
                abs_path = Path(path)
                if not abs_path.exists():
                    raise ValueError(f'unknown storage and not a file: {path}')
            else:
                pdir = self.sel['key']
                fpart = m.group(1)
                abs_path = self.lib.get_storage_path() / f'{pdir}/{fpart}'
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'pdir={pdir}, fpart={fpart}, abs={abs_path}')
        return abs_path

    def __format_zobj__(self):
        abs_path = self.path
        its = self.sel.copy()
        its.update({'name': self.name, 'abs_path': abs_path})
        return '{name} [{type}]{abs_path}'.format(**its)


class Container(ZoteroObject):
    """Container class holds items and sub-collections.

    """
    def __init__(self, items, collections):
        self.items = items
        self.collections = collections
        super().__init__(None)

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
        super().__init__(items, collections)

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
        super().__init__([], collections)
        for c in collections:
            self._init_child(c)

    def _init_child(self, parent):
        if isinstance(parent, Item):
            parent.lib = self
        for c in parent.children:
            self._init_child(c)

    def get_storage_path(self, fname=None):
        path = Path(self.data_dir, self.storage_dirname)
        if fname:
            path = Path(path, fname)
        return path

    def get_id(self):
        return 'l' + str(self.library_id)

    def attachment_resource(self, item):
        if item.type == 'attachment':
            return f'{self.storage_dirname}/{item.path}'

    @property
    def name(self):
        return 'lib'

    @property
    def title(self):
        if self.library_id == 1:
            return 'Personal Library'
        else:
            return 'Library'


class Visitor(ABC):
    """The visitor in the GoF *visitor pattern*.
    """
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
    """A visitor that prints items for debugging.

    """
    def __init__(self, writer: TextIOBase):
        self.writer = writer
        self.depth = 0

    def enter_parent(self, parent: ZoteroObject):
        self.writer.write(f"{' ' * (self.depth * 4)}{str(parent)} " +
                          f'({parent.__class__.__name__})\n')
        self.depth += 1

    def visit_child(self, child: ZoteroObject):
        pass

    def leave_parent(self, parent: ZoteroObject):
        self.depth -= 1


class Walker(ABC):
    """Iterates the Zotero data and calls the visitor for each node.

    """
    @abstractmethod
    def walk(self, parent: ZoteroObject, visitor: Visitor):
        """Recursively traverse the object graph."""
        pass


class UnsortedWalker(Walker):
    """Iterates through the Zotero visiting children in whatever order is
    provided by the database.

    """
    def walk(self, parent: ZoteroObject, visitor: Visitor):
        visitor.enter_parent(parent)
        for c in parent.children:
            visitor.visit_child(c)
            self.walk(c, visitor)
        visitor.leave_parent(parent)


class SortedWalker(Walker):
    """Iterates through the Zotero visiting children in sorted order.

    """
    def __init__(self, key_fn: Callable = None, reverse: bool = False):
        """Initialize.

        :param key_fn: a function/callable used to sort the data that takes a
                       single argument to access compared data, which defaults
                       to :function:`str`

        :param reverse: whether or not to reverse the visited results

        """
        if key_fn is None:
            self.key_fn = str
        else:
            self.key_fn = key_fn
        self.reverse = reverse

    def walk(self, parent: ZoteroObject, visitor: Visitor):
        visitor.enter_parent(parent)
        kids = sorted(parent.children, key=self.key_fn, reverse=self.reverse)
        for c in kids:
            visitor.visit_child(c)
            self.walk(c, visitor)
        visitor.leave_parent(parent)
