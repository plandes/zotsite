import logging
import unittest
from io import StringIO
from zensols.zotsite import SiteCreator, AppConfig

logger = logging.getLogger('zensols.zotsite.test')


class TestSiteExporter(unittest.TestCase):
    def test_exporter(self):
        config = AppConfig.from_args(
            AppConfig('test-resources/zotsite.conf'),
            out_dir='target')
        exporter = SiteCreator(config)
        if 0:
            sio = StringIO()
            exporter.print_structure(sio)
            self.assertTrue(len(sio.getvalue() > 0))
