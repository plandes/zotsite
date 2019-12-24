from pathlib import Path
from zensols.pybuild import SetupUtil

su = SetupUtil(
    setup_path=Path(__file__).parent.absolute(),
    package_names=['zensols', 'resources'],
    name='zensols.zotsite',
    user='plandes',
    project='zotsite',
    package_data={'': ['*.html', '*.js', '*.css', '*.map', '*.svg', 'glyphicons*']},
    description='This project attempts to export a local Zotero library to a usable HTML website.',
    keywords=['academic', 'web', 'website', 'research'],
)

su.setup()
