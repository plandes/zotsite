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

    def _prepare_creator(self, output_dir: Path):
        if output_dir is not None:
            self.site_creator.out_dir = output_dir
        if self.prune_pattern is not None:
            pat: re.Pattern = re.compile(self.prune_pattern)
            self.site_creator.prune_visitor.prune_pattern = pat

    def export(self, output_dir: Path = None):
        """Generate and export the Zotero website.

        :param output_dir: the directory to dump the site; default to
                           configuration file

        """
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'exporting site: {output_dir}')
        self._prepare_creator(output_dir)
        self.site_creator.export()

    def print_structure(self):
        """Print (sub)collections and papers in those collections as a tree."""
        self._prepare_creator(None)
        self.site_creator.print_structure()
