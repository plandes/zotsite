import logging
import shutil
from pathlib import Path
from zensols.zotsite import (
    Visitor,
    ItemMapper,
    Item,
    ZoteroObject,
)

logger = logging.getLogger(__name__)


class FileSystemCopyVisitor(Visitor):
    """This class copies all Item objects to their destination.

    """
    def __init__(self, lib, out_dir, itemmapper: ItemMapper):
        """Initialize the visitor object.

        :param lib: the object graph returned from
                   ``DatabaseReader.get_library``.
        :param out_dir: the target directory to copy data
        :param itemmapper: used for file name substitution so the widget uses the
                             correct names (i.e. underscore substitution)

        """
        self.lib = lib
        self.data_path = Path(lib.get_storage_path())
        self.out_path = Path(out_dir)
        self.itemmapper = itemmapper

    def enter_parent(self, parent: ZoteroObject):
        pass

    def visit_child(self, child: ZoteroObject):
        if isinstance(child, Item):
            if child.file_name is not None:
                src = Path(self.data_path, child.file_name)
                dst = Path(self.out_path, self.itemmapper.get_file_name(child))
                parent = dst.parent
                if not dst.is_file():
                    if not parent.is_dir():
                        logger.debug('create: {}'.format(parent))
                        parent.mkdir(parents=True, exist_ok=True)
                    logger.debug('copy: {} -> {}'.format(src, dst))
                    shutil.copy(str(src), str(dst))

    def leave_parent(self, parent: ZoteroObject):
        pass
