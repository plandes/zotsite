import logging
import re
from zensols.zotsite import (
    Walker,
    Library,
    Collection,
)

logger = logging.getLogger('zensols.zotsite.fswalk')


class PruneWalker(Walker):
    """This class copies all Item objects to their destination.

    """

    def __init__(self, name_pat):
        """Initialize the walker object.

        :param lib: the object graph returned from
        ``DatabaseReader.get_library``.
        :param data_dir: the directory where the Zotero storage directory is
        :param out_dir: the target directory to copy data
        :param fscopier: used for file name substitution so the widget uses the
        correct names (i.e. underscore substitution)

        """
        self.name_pat = re.compile(name_pat)
        self.matched_coll = None
        self.keep = []

    def enter_parent(self, parent):
        if isinstance(parent, Collection):
            logger.debug('entering: {}'.format(parent))
            if self.matched_coll is None and self.name_pat.match(parent.name):
                logger.debug('found: {}'.format(parent.name))
                self.matched_coll = parent
                self.keep.append(parent)

    def leave_parent(self, parent):
        logger.debug('leaving: {}'.format(parent))
        if isinstance(parent, Collection):
            if self.matched_coll is not None and self.matched_coll == parent:
                logger.debug('leaving: {}'.format(self.matched_coll))
                self.matched_coll = None
        elif isinstance(parent, Library):
            logger.debug('leaving library {} and setting collections: {}'.
                         format(parent, self.keep))
            parent.items = ()
            parent.collections = self.keep
