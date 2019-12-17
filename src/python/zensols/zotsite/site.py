import logging
from pathlib import Path
import json
import shutil
from zensols.zotsite import (
    AppConfig,
    DatabaseReader,
    ZoteroObject,
    NavCreateWalker,
    PatternFsCopier,
    FileSystemCopyWalker,
    PruneWalker,
)

logger = logging.getLogger('zensols.zotsite.site')


class SiteCreator(object):
    """Create the Zotero content web site.

    """
    def __init__(self, config: AppConfig = None):
        cnf = config.populate()
        self.db = DatabaseReader(config.get_option_path('data_dir'),
                                 library_id=cnf.library_id)
        self.out_dir = config.get_option_path('out_dir')
        self.name_pat = config.get_option('name_pat', expect=False)
        self.config = config

    def _get_library(self):
        lib = self.db.get_library()
        if self.name_pat is not None:
            walker = PruneWalker(self.name_pat)
            ZoteroObject.walk(lib, walker)
        return lib

    def print_structure(self):
        """Print (sub)collections and papers in those collections as a tree.

        """
        lib = self._get_library()
        ZoteroObject.print_zotero_object(lib)

    def _write_meta(self, fname):
        """Write version and other metadata to the website, which is used during
        rending of the site.

        """
        if hasattr(self.config, 'pkg'):
            pkg = self.config.pkg
            meta = {'version': pkg.version,
                    'project_name': pkg.project_name}
        else:
            meta = {'version': '<none>',
                    'project_name': '<none>'}
        js = 'var zoteroMeta = {};'.format(json.dumps(meta))
        with open(fname, 'w') as f:
            f.write(js)

    def _create_tree_data(self):
        """Create the table of contents/tree info used by the navigation widget.

        """
        lib = self.lib
        fscopier = self.fscopier
        js_dir = self.out_dir / 'js'
        nav_file = js_dir / 'zotero-tree-data.js'
        logger.info('creating js nav tree: {}'.format(nav_file))
        walker = NavCreateWalker(lib, fscopier)
        ZoteroObject.walk(lib, walker)
        with open(nav_file, 'w') as f:
            f.write("var tree =\n")
            f.write(json.dumps(walker.primary_roots, indent=2))
        meta_file = Path(js_dir, 'zotero-meta.js')
        logger.info('creating js metadata: {}'.format(meta_file))
        self._write_meta(meta_file)

    def _copy_storage(self):
        """Copy the storage contents, which is the location of the PDF (and other)
        documents that will be rendered in the site GUI.

        """
        lib = self.db.get_library()
        src = self.lib.get_storage_path()
        dst = self.out_dir / 'storage'
        fswalker = FileSystemCopyWalker(lib, src, dst, self.fscopier)
        logger.info('copying storage {} -> {}'.format(src, dst))
        ZoteroObject.walk(lib, fswalker)

    def _copy_static_res(self, src: Path, dst: Path):
        """Copy static resources from the distribution package.

        :param src: the source package directory
        :param dst: the destination on the file system

        """
        logger.info(f'copy: {src} -> {dst}'.format(src, dst))
        dst.mkdir(parents=True, exist_ok=True)
        for res in src.iterdir():
            res = res.name
            src_file = src / res
            dst_file = dst / res
            if src_file.is_dir():
                self._copy_static_res(src_file, dst_file)
            else:
                logger.info(f'copy file: {src_file} -> {dst_file}')
                shutil.copyfile(src_file, dst_file)

    def _copy_static(self):
        for src in 'src lib'.split():
            src_dir = self.config.resource_filename(f'resources/{src}')
            self._copy_static_res(src_dir, self.out_dir)

    @staticmethod
    def _create_fscopier():
        return PatternFsCopier('.*\.pdf$', '[ ]')

    def export(self):
        """Entry point method to export (create) the website.

        """
        self.lib = self._get_library()
        self.fscopier = self._create_fscopier()
        self._copy_static()
        self._create_tree_data()
        self._copy_storage()

    def tmp(self):
        self.print_structure()
