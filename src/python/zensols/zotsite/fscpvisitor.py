"""Contains a class to copy files from the package resource location to the
target website path.

"""
__author__ = 'Paul Landes'

import logging
import shutil
from pathlib import Path
from zensols.zotsite import Visitor, ItemMapper, Item, ZoteroObject

logger = logging.getLogger(__name__)


class FileSystemCopyVisitor(Visitor):
    """This class copies all Item objects to their destination.

    """
    def __init__(self, lib, out_dir, itemmapper: ItemMapper):
        """Initialize the visitor object.

        :param lib: the object graph returned from
                   ``DatabaseReader.get_library``.

        :param out_dir: the target directory to copy data

        :param itemmapper: used for file name substitution so the widget uses
                           the correct names (i.e. underscore substitution)

        """
        self.lib = lib
        self.out_path = Path(out_dir)
        self.itemmapper = itemmapper
        logger.debug(f'out_path: {self.out_path}')

    def enter_parent(self, parent: ZoteroObject):
        pass

    def visit_child(self, child: ZoteroObject):
        if isinstance(child, Item):
            logger.debug(f'child: {child.path}')
            if child.path is not None:
                src = child.path
                dst = Path(self.out_path, self.itemmapper.get_file_name(child))
                logger.debug(f'copy: {src} -> {dst}')
                parent = dst.parent
                if not dst.is_file():
                    if not parent.is_dir():
                        logger.debug(f'create: {parent}')
                        parent.mkdir(parents=True, exist_ok=True)
                    src, dst = str(src), str(dst)
                    logger.debug(f'shcopy: {src} -> {dst}')
                    shutil.copyfile(src, dst)
                    shutil.copystat(src, dst)

    def leave_parent(self, parent: ZoteroObject):
        pass
