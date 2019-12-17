import logging
import sys
import unittest
from zensols.zotsite import SiteExporter

logger = logging.getLogger('zensols.zotsite.test')
logging.basicConfig(level=logging.DEBUG)


class TestSiteExporter(unittest.TestCase):
    def test_site_exporter(self):
        exporter = SiteExporter()
        #self.assertEqual(should_be, msg)


def main(args=sys.argv[1:]):
    unittest.main()


if __name__ == '__main__':
    main()
