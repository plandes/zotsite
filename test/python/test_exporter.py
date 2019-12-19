import logging
import unittest
from zensols.zotsite import SiteCreator, AppConfig

logger = logging.getLogger('zensols.zotsite.test')


class TestSiteExporter(unittest.TestCase):
    def test_site_exporter(self):
        config = AppConfig.from_args(out_dir='target')
        exporter = SiteCreator(config)
        # todo: at least one test

