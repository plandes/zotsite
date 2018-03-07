from setuptools import setup, find_packages

setup(
    name = "zensols.zotsite",
    packages = ['zensols', 'zensols.zotsite'],
    version = '0.1',
    description = 'This project attempts to export a local Zotero library to a usable HTML website.',
    author = 'Paul Landes}',
    author_email = 'landesatmailcdtnet',
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
