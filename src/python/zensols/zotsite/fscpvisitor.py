"""Contains a class to copy files from the package resource location to the
target website path.

"""
__author__ = 'Paul Landes'

import logging
import shutil
from pathlib import Path
from . import Visitor, ItemMapper, Item, ZoteroObject, Library

logger = logging.getLogger(__name__)


class FileSystemCopyVisitor(Visitor):
    """This class copies all Item objects to their destination.

    """
    def __init__(self, lib: Library, out_dir: Path, robust: bool,
                 itemmapper: ItemMapper):
        """Initialize the visitor object.

        :param lib: the object graph returned from
                   ``DatabaseReader.get_library``.

        :param out_dir: the target directory to copy data

        :param robust: whether to raise an exception on file system errors

        :param itemmapper: used for file name substitution so the widget uses
                           the correct names (i.e. underscore substitution)

        """
        self._out_path = out_dir
        self._robust = robust
        self._itemmapper = itemmapper
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f'out_path: {self._out_path}')

    def enter_parent(self, parent: ZoteroObject):
        pass

    def visit_child(self, child: ZoteroObject):
        if isinstance(child, Item):
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'child: {child.path}')
            if child.path is not None:
                src: Path = child.path
                dst = self._out_path / self._itemmapper.get_file_name(child)
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f'copy: {src} -> {dst}')
                parent = dst.parent
                if not dst.is_file():
                    if not parent.is_dir():
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug(f'create: {parent}')
                        parent.mkdir(parents=True, exist_ok=True)
                    src, dst = str(src), str(dst)
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug(f'shcopy: {src} -> {dst}')
                    try:
                        shutil.copyfile(src, dst)
                        shutil.copystat(src, dst)
                    except OSError as e:
                        if self._robust:
                            logger.error(f'could not copy {src} to {dst}: {e}')
                        else:
                            raise e

    def leave_parent(self, parent: ZoteroObject):
        pass
