"""A class that prunes collections based on a regular expression.

"""
__author__ = 'Paul Landes'

from typing import Union
from dataclasses import dataclass, field
import logging
import re
from zensols.zotsite import Visitor, Library, Collection, ZoteroObject, Item

logger = logging.getLogger(__name__)


@dataclass
class PruneVisitor(Visitor):
    """This that filters out ``Collection`` instances based on a regular
    expression.  Optionally, ``Item`` level nodes are *included* if based on
    ``match_children``.

    """
    prune_pattern: Union[re.Pattern, str] = field(default=None)
    """A regular expression used to filter ``Collection`` nodes."""

    match_children: bool = field(default=False)
    """if ``True``, then also match ``Item`` level nodes."""

    def __post_init__(self):
        if isinstance(self.prune_pattern, str):
            self.prune_pattern = re.compile(self.prune_pattern)
        self._matched_coll = None
        self._keep = []
        self._keep_ids = set()

    @property
    def should_walk(self) -> bool:
        return self.prune_pattern is not None

    def _add_child_item_ids(self, parent: ZoteroObject):
        self._keep_ids.add(parent.id)
        for child in parent.children:
            self._add_child_item_ids(child)

    def _add(self, node: ZoteroObject):
        # we descent parents first so, as long as we check first we won't
        # duplicate on Item level nodes
        if node.id not in self._keep_ids:
            self._add_child_item_ids(node)
            self._keep.append(node)

    def enter_parent(self, parent: ZoteroObject):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'entering: {parent} ({parent.__class__.__name__})')
        if isinstance(parent, Collection):
            if self._matched_coll is None and \
               self.prune_pattern.match(parent.name):
                logger.debug(f'found: {parent.name}')
                self._matched_coll = parent
                self._add(parent)

    def visit_child(self, child: ZoteroObject):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'visiting: {child}')
        if isinstance(child, Item) and \
           self.match_children and \
           self._matched_coll is None and \
           self.prune_pattern.match(child.name):
            self._add(child)

    def leave_parent(self, parent: ZoteroObject):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'leaving: {format(parent)}')
        if isinstance(parent, Collection):
            if self._matched_coll == parent:
                logger.debug(f'leaving: {self._matched_coll}')
                self._matched_coll = None
        elif isinstance(parent, Library):
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'leaving lib {parent}, setting col: {self._keep}')
            parent.items = ()
            parent.collections = self._keep
