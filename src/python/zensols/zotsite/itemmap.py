from abc import ABC, abstractmethod
import logging
import re
from zensols.zotsite import Item, Library

logger = logging.getLogger(__name__)


class ItemMapper(ABC):
    EXT_RE = re.compile(r'.+\.(.+)?$')

    def _item_to_ext(self, item: Item):
        m = self.EXT_RE.match(item.file_name)
        return f'.{m.group(1)}' if m is not None else ''

    @abstractmethod
    def get_resource_name(self, item: Item) -> str:
        pass

    @abstractmethod
    def get_file_name(self, item: Item) -> str:
        pass


class RegexItemMapper(ItemMapper):
    """Map by using regular expression replacements.

    """
    def __init__(self, lib: Library, fmatch_re=None, repl_re=None):
        self.lib = lib
        if fmatch_re is not None:
            self.fmatch_re = re.compile(fmatch_re)
        else:
            self.fmatch_re = None
        if repl_re is not None:
            self.repl_re = re.compile(repl_re)
        else:
            self.repl_re = None

    def _map(self, item: Item) -> str:
        """Return the regular expression matched/modified string of ``fname``.'

        """
        fname = self.lib.attachment_resource(item)
        if fname is not None:
            if self.fmatch_re and self.repl_re and self.fmatch_re.match(fname):
                fname = self.repl_re.sub('_', fname)
        return fname

    def get_resource_name(self, item: Item) -> str:
        return self._map(item)

    def get_file_name(self, item: Item) -> str:
        return self._map(item)


class IdItemMapper(ItemMapper):
    """Map by using ids.

    """
    def __init__(self, lib: Library, fmatch_re=None, repl_re=None):
        self.lib = lib
        if fmatch_re is not None:
            self.fmatch_re = re.compile(fmatch_re)
        else:
            self.fmatch_re = None
        if repl_re is not None:
            self.repl_re = re.compile(repl_re)
        else:
            self.repl_re = None

    def _map(self, item: Item) -> str:
        """Return the regular expression matched/modified string of ``fname``.'

        """
        if item.type == 'attachment' and item.file_name is not None:
            ext = self._item_to_ext(item)
            return f'{self.lib.storage_dirname}/{item.id}{ext}'

    def get_resource_name(self, item: Item) -> str:
        return self._map(item)

    def get_file_name(self, item: Item) -> str:
        return self._map(item)
