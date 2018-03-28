from setuptools import setup, find_packages
import os

def get_packages(dnames):
    dirs = []
    for dname in dnames:
        for root, subdirs, files in os.walk(dname):
            root = os.path.relpath(root, dname)
            if root != '.':
                dirs.append(os.path.join(dname, root.replace(os.sep, '.')))
    return dirs

setup(
    name = "zensols.zotsite",
    packages = get_packages(['zensols', 'resources']),
    package_data={'': ['*.html', '*.js', '*.css', '*.map', '*.svg', 'glyphicons*']},
    version = '0.1',
    description = 'This project attempts to export a local Zotero library to a usable HTML website.',
    author = 'Paul Landes',
    author_email = 'landes@mailc.net',
    url = 'https://github.com/plandes/zotsite',
    download_url = 'https://github.com/plandes/zotsite/releases/download/v0.0.1/zensols.zotsite-0.1-py3-none-any.whl',
    keywords = ['tooling'],
    classifiers = [],
    entry_points={
        'console_scripts': [
            'zotsite=zensols.zotsite.cli:main'
        ]
    }
)
