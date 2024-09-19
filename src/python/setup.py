from pathlib import Path
from zensols.pybuild import SetupUtil

su = SetupUtil(
    setup_path=Path(__file__).parent.absolute(),
    name="zensols.zotsite",
    package_names=['zensols', 'resources'],
    package_data={'': ['*.conf', '*.yml', '*.sql', '*.html', '*.js', '*.css', '*.map', '*.svg', 'glyphicons*']},
    description='This project exports your local Zotero library to a usable HTML website.',
    user='plandes',
    project='zotsite',
    keywords=['tooling'],
).setup()
