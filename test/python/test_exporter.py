import logging
import unittest
from io import StringIO
from zensols.cli import CliHarness
from zensols.zotsite import Application, ApplicationFactory


if 0:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)


class TestSiteExporter(unittest.TestCase):
    def setUp(self):
        harn: CliHarness = ApplicationFactory.create_harness()
        self.app: Application = harn.get_instance(
            '-c test-resources/zotsite.conf --level=err')
        if self.app is None:
            raise ValueError('Could not create application')

    def test_exporter(self):
        exporter = self.app.site_creator
        if 0:
            sio = StringIO()
            exporter.print_structure(sio)
            self.assertTrue(len(sio.getvalue() > 0))
