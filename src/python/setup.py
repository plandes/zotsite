from pathlib import Path
from zensols.pybuild import SetupUtil

su = SetupUtil(
    setup_path=Path(__file__).parent.absolute(),
    name="zensols.zotsite",
    package_names=['zensols', 'resources'],
    # package_data={'': ['*.html', '*.js', '*.css', '*.map', '*.svg']},
    package_data={'': ['*.conf', '*.json', '*.yml']},
    description='This project exports your local Zotero library to a usable HTML website.',
    user='plandes',
    project='zotsite',
    keywords=['tooling'],
    # has_entry_points=False,
).setup()
