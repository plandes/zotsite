import logging
import unittest
from zensols.zotsite import SiteCreator, AppConfig

logger = logging.getLogger('zensols.zotsite.test')
logging.basicConfig(level=logging.DEBUG)


class TestSiteExporter(unittest.TestCase):
    def test_site_exporter(self):
        config = AppConfig.from_args(out_dir='target')
        exporter = SiteCreator(config)
        #self.assertEqual(should_be, msg)
