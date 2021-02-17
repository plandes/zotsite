"""Application configuration class.

"""
__author__ = 'Paul Landes'

from pathlib import Path
from zensols.config import ExtendedInterpolationEnvConfig


class AppConfig(ExtendedInterpolationEnvConfig):
    @property
    def data_dir(self):
        return self.get_option_path('data_dir').expanduser()

    def set_default(self, name: str, value: str, clobber: object = None):
        if clobber is not None:
            self.set_option(name, clobber, self.default_section)
        elif name not in self.options and value is not None:
            self.set_option(name, value, self.default_section)

    @classmethod
    def from_args(cls, config=None, data_dir: Path = None,
                  out_dir=None, name_pat: str = None):
        if config is None:
            self = cls()
            self._conf = self._create_config_parser()
            self.parser.add_section(self.default_section)
        else:
            self = config
        self.set_default('data_dir', '~/Zotero', data_dir)
        self.set_default('library_id', '1')
        self.set_default('match_children', 'False')
        self.set_default('file_mapping', 'item')
        self.set_default('id_mapping', 'none')
        self.set_default('out_dir', None, out_dir)
        self.set_default('name_pat', None, name_pat)
        self.set_default('sort', 'none')
        return self
