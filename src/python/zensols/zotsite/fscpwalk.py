import logging
import shutil
from pathlib import Path
from zensols.zotsite import (
    Walker,
    PatternFsCopier,
    Item,
)

logger = logging.getLogger('zensols.zotsite.fswalk')


class FileSystemCopyWalker(Walker):
    """This class copies all Item objects to their destination.

    """
    def __init__(self, lib, data_dir, out_dir, fscopier: PatternFsCopier):
        """Initialize the walker object.

        :param lib: the object graph returned from
        ``DatabaseReader.get_library``.
        :param data_dir: the directory where the Zotero storage directory is
        :param out_dir: the target directory to copy data
        :param fscopier: used for file name substitution so the widget uses the
        correct names (i.e. underscore substitution)

        """
        self.lib = lib
        self.data_path = Path(data_dir)
        self.out_path = Path(out_dir)
        self.fscopier = fscopier

    def visit_child(self, child):
        if isinstance(child, Item):
            fname = child.file_name
            if fname is not None:
                src = Path(self.data_path, fname)
                dst = Path(self.out_path, self.fscopier.update_file(fname))
                parent = dst.parent
                if not dst.is_file():
                    if not parent.is_dir():
                        logger.debug('creating directory: {}'.format(parent))
                        parent.mkdir(mode=0o0755, parents=True, exist_ok=True)
                    logger.debug('copying {} -> {}'.format(src, dst))
                    shutil.copy(str(src), str(dst))
