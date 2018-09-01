import logging
import os
import json
import shutil
import pkg_resources
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
        logger.debug('data dir: {}, out_dir: {}, config=<{}>'.
                     format(data_dir, out_dir, config))
        if data_dir is None:
            home_dir = os.environ['HOME']
            data_dir = os.path.join(home_dir, 'Zotero')
        self.out_dir = out_dir
        self.db = DatabaseReader(data_dir, library_id)
        self.config = config

    def print_structure(self):
        lib = self.db.get_library()
        ZoteroObject.print_zotero_object(lib)

    def _write_meta(self, fname):
        pkg = self.config.pkg
        meta = {'version': pkg.version,
                'project_name': pkg.project_name}
        js = 'var zoteroMeta = {};'.format(json.dumps(meta))
        with open(fname, 'w') as f:
            f.write(js)

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
        meta_file = os.path.join(js_dir, 'zotero-meta.js')
        logger.info('creating js metadata: {}'.format(meta_file))
        self._write_meta(meta_file)

    def _copy_storage(self):
        src = self.lib.get_storage_path()
        dst = os.path.join(self.out_dir, 'storage')
        logger.info('copying storage {} -> {}'.format(src, dst))
        if os.path.exists(dst):
            logger.warn('storage directory already exists--skipping: {}'.
                        format(dst))
        else:
            self.fscopier.copytree(src, dst)

    def _copy_static(self, src, dst):
        logger.info('copy: {} -> {}'.format(src, dst))
        if pkg_resources.resource_isdir(__name__, src):
            logger.debug('mkdir: {}'.format(dst))
            os.makedirs(dst, exist_ok=True)
        for res in pkg_resources.resource_listdir(__name__, src):
            dst_res = os.path.join(dst, os.path.basename(res))
            res = '/'.join([src, res])
            if pkg_resources.resource_isdir(__name__, res):
                self._copy_static(res, dst_res)
            else:
                in_stream = pkg_resources.resource_stream(__name__, res)
                logger.debug('copy file: {} -> {}'.format(res, dst_res))
                with open(dst_res, 'wb') as fout:
                    shutil.copyfileobj(in_stream, fout)

    def export(self):
        self.lib = self.db.get_library()
        self.fscopier = PatternFsCopier('.*\.pdf$', '[ ]', '_')
        self._copy_static('resources/site', self.out_dir)
        self._create_tree_data()
        self._copy_storage()
