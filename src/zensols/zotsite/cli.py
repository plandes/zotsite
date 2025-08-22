"""Command line entry point to the application.

"""
__author__ = 'Paul Landes'

from typing import List, Any, Dict
import sys
from zensols.config import ConfigFactory
from zensols.cli import ActionResult, CliHarness
from zensols.cli import ApplicationFactory as CliApplicationFactory
from . import Resource


class ApplicationFactory(CliApplicationFactory):
    def __init__(self, *args, **kwargs):
        kwargs['package_resource'] = 'zensols.zotsite'
        super().__init__(*args, **kwargs)

    @classmethod
    def _get_config_factory(cls, name: str) -> ConfigFactory:
        """Return the application context."""
        harness: CliHarness = cls.create_harness()
        fac: ConfigFactory = harness.get_config_factory()
        return fac(name)

    @classmethod
    def get_resource(cls) -> Resource:
        """Contains programatic resources (citation) queries and the website
        creation.

        """
        return cls._get_config_factory('zs_resource')


def main(args: List[str] = sys.argv, **kwargs: Dict[str, Any]) -> ActionResult:
    harness: CliHarness = ApplicationFactory.create_harness(relocate=False)
    harness.invoke(args, **kwargs)
