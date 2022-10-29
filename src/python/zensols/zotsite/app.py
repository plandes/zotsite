"""This project exports your local Zotero library to a usable HTML website.

"""
__author__ = 'Paul Landes'

from dataclasses import dataclass, field
import re
import logging
from pathlib import Path
from . import SiteCreator

logger = logging.getLogger(__name__)


@dataclass
class Application(object):
    """This project exports your local Zotero library to a usable HTML website.

    """
    site_creator: SiteCreator = field()
    """Creates the Zotero content web site."""

    prune_pattern: str = field(default=None)
    """A regular expression used to filter ``Collection`` nodes."""

    def _prepare_creator(self, output_dir: Path) -> Path:
        if output_dir is not None:
            self.site_creator.out_dir = output_dir
        else:
            output_dir = self.site_creator.out_dir
        if self.prune_pattern is not None:
            pat: re.Pattern = re.compile(self.prune_pattern)
            self.site_creator.prune_visitor.prune_pattern = pat
        return output_dir

    def _show(self, index_file: Path):
        from zensols.cli import CliHarness
        from zensols.showfile import ApplicationFactory, Application
        harness: CliHarness = ApplicationFactory.create_harness()
        app: Application = harness.get_instance('config')
        logger.info(f'showing {index_file}')
        app.show(index_file)

    def export(self, output_dir: Path = None, show: bool = False):
        """Generate and export the Zotero website.

        :param output_dir: the directory to dump the site; default to
                           configuration file

        :param show: whether to browse to the created site (needs ``pip install
                     zensols.showfile``)

        """
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'exporting site: {output_dir}')
        output_dir = self._prepare_creator(output_dir)
        self.site_creator.export()
        if show:
            self._show(output_dir / 'index.html')

    def print_structure(self):
        """Print (sub)collections and papers in those collections as a tree."""
        self._prepare_creator(None)
        self.site_creator.print_structure()
