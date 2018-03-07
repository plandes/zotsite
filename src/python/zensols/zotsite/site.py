import logging, os, json, shutil
from zensols.zotsite.db import DatabaseReader
from zensols.zotsite.domain import ZoteroObject
from zensols.zotsite.nav import NavCreateWalker
from zensols.zotsite.cptree import PatternFsCopier

logger = logging.getLogger('zensols.zotsite.site')

class SiteExporter(object):
    """
    Create the Zotero content web site.
    """
    def __init__(self, data_dir=None, out_dir=None, library_id=1, config=None):
        logger.debug('data dir: %s, out_dir: %s, config=<%s>' % (data_dir, out_dir, config))
        if data_dir == None:
            home_dir = os.environ['HOME']
            data_dir = os.path.join(home_dir, 'Zotero')
        self.out_dir = out_dir
        self.db = DatabaseReader(data_dir, library_id)

    def print_structure(self):
        lib = self.db.get_library()
        ZoteroObject.print_zotero_object(lib)

    def _create_tree_data(self):
        lib = self.lib
        fscopier = self.fscopier
        js_dir = os.path.join(self.out_dir, 'js')
        nav_file = os.path.join(js_dir, 'zotero-tree-data.js')
        logger.info('creating js nav tree: {}'.format(nav_file))
        walker = NavCreateWalker(lib, fscopier)
        ZoteroObject.walk(lib, walker)
        with open(nav_file, 'w') as f:
            f.write("var tree =\n")
            f.write(json.dumps(walker.primary_roots, indent=2))

    def _copy_storage(self):
        lib = self.lib
        fscopier = self.fscopier
        src = lib.get_storage_path()
        dst = os.path.join(self.out_dir, 'storage')
        logger.info('copying storage {} -> {}'.format(src, dst))
        if os.path.exists(dst):
            logger.warn('storage directory already exists--skipping: {}'.format(dst))
        else:
            fscopier.copytree(src, dst)

    def export(self):
        db = self.db
        self.lib = self.db.get_library()
        self.fscopier = PatternFsCopier('.*\.pdf$', '[ ]', '_')
        self._create_tree_data()
        self._copy_storage()
