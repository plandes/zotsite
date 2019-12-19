import logging
import re
from zensols.zotsite import (
    Visitor,
    Library,
    Collection,
    ZoteroObject,
    Item,
)

logger = logging.getLogger(__name__)


class PruneVisitor(Visitor):
    """This that filters out ``Collection`` instances based on a regular
    expression.  Optionally, ``Item`` level nodes are *included* if based on
    ``match_children``.

    """

    def __init__(self, name_pat: str, match_children: bool):
        """Initialize the visitor object.

        :param name_pat: a regular expression used to filter nodes
        :param match_children: if ``True``, then also match ``Item`` level
                               nodes

        """
        self.name_pat = re.compile(name_pat)
        self.match_children = match_children
        self.matched_coll = None
        self.keep = []
        self.keep_ids = set()
        self.last_parent_coll = None

    def _add_child_item_ids(self, parent: ZoteroObject):
        self.keep_ids.add(parent.id)
        for child in parent.children:
            self._add_child_item_ids(child)

    def _add(self, node: ZoteroObject):
        # we descent parents first so, as long as we check first we won't
        # duplicate on Item level nodes
        if node.id not in self.keep_ids:
            #self.keep_ids.add(node.id)
            self._add_child_item_ids(node)
            self.keep.append(node)

    def enter_parent(self, parent: ZoteroObject):
        logger.debug(f'entering: {parent} ({parent.__class__.__name__})')
        if isinstance(parent, Collection):
            if self.matched_coll is None and self.name_pat.match(parent.name):
                logger.debug(f'found: {parent.name}')
                self.matched_coll = parent
                self._add(parent)

    def visit_child(self, child: ZoteroObject):
        logger.debug(f'visiting: {child}')
        if isinstance(child, Item) and \
           self.match_children and \
           self.matched_coll is None and \
           self.name_pat.match(child.name):
            self._add(child)

    def leave_parent(self, parent: ZoteroObject):
        logger.debug(f'leaving: {format(parent)}')
        if isinstance(parent, Collection):
            if self.matched_coll == parent:
                logger.debug(f'leaving: {self.matched_coll}')
                self.matched_coll = None
        elif isinstance(parent, Library):
            logger.debug(f'leaving library {parent} and setting collections: {self.keep}')
            parent.items = ()
            parent.collections = self.keep
