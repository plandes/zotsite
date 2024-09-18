"""Query Zotero collections metadata.

"""
__author__ = 'Paul Landes'

from typing import Tuple, Dict, Any
from dataclasses import dataclass, field
from sqlite3 import OperationalError
from zensols.db import DbPersister
from . import ZoteroApplicationError


@dataclass
class CiteDatabase(object):
    """Map Zotero keys to BetterBibtex citekeys.

    """
    _persister: DbPersister = field()
    """The persister used to get the data."""

    _sql: str = field()
    """The SQL used to query the BetterBibtex database."""

    @property
    def entries(self) -> Dict[str, Dict[str, Any]]:
        """Get all entries from the BetterBibtex database with
        <libraryID>_<itemKey> as keys and the dict entry as values.

        """
        def map_row(r: Tuple[Any, ...]) -> Tuple[str, Dict[str, Any]]:
            key = f'{r[0]}_{r[1]}'
            data = {'libraryID': r[0], 'itemKey': r[1], 'citationKey': r[2]}
            return key, data

        try:
            rows: Tuple[Tuple[str]] = self._persister.execute(self._sql)
        except OperationalError as e:
            raise ZoteroApplicationError(
                f'Could not access BetterBibtex database: {e}') from e
        return dict(map(map_row, rows))
