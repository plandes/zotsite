# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased]


## [0.3.5] - 2021-03-16
### Changed
- Switch from travis to github workflows.
- Upgrade to [zensols.util] 1.4.1.


## [0.3.4] - 2020-12-09
### Added
- Sphinx documentation, which includes API docs.
### Changed
- Upgrade to [zensols.util] 1.3.0.


## [0.3.3] - 2020-04-25
### Changed
- Upgrade to [zensols.util] 1.2.0.

### Removed
- Drop support for Python 3.6.

### Added
- Added icons for thesis, patents and blog posts.
- Added option to sort items in the tree navigation.


## [0.3.2] - 2020-01-03
### Added
- Compatibility with [ZotFile].  Specifically, now storage locations are used
  verbatim if 1) no `storage:` is found in the resource name and 2) if the
  resource is a file found on the OS.


## [0.3.1] - 2019-12-24
### Changed
- Fixed export error: `No such file or directory: 'resources/src'`.


## [0.3.0] - 2019-12-20
### Added
- Collections filtering using regular expressions is now fully supported.
- Ability to link directly to any item in the hierarchy.
- Link button that copies the current page URL to the clipboard.
- Added [BetterBibtex] references for easy linking to the site with citation
  keys.
- HTML (i.e. snapshots) are now visible in the pane PDFs are displayed.
- Short files to reduce character/file system conflicts.
- Clear button to reset the interface.
- Added creators (authors) to metadata pane.

### Changed
- Beautification of the metadata keys in the item table view.
- Changed default naming to use short files.
- Simpler command line by moving configuration to the configuration file.
- Refactored: cleaned up class structure and graph iteration OO class patterns.
- Retrofit new actioncli features.
- Move to more advanced configparser, which uses new notation (example:
  `$(HOME)s` -> `${HOME}`).
- Metadata is sorted.


## [0.2.3] - 2018-09-08
### Added
- Feature to export collections based on an regular expression match on name.

### Changes
- Notes now have full note text with Zotero CSS, so it looks as it does in the
  desktop app.  Note titles have the text from the note title instead of just
  `Note`.


## [0.2.2] - 2018-08-31
### Added
- Get version from pkg resources.


## [0.2.1] - 2018-08-11
### Changed
- Fixed pip wheel dependency auto install.
- New python build.


## [0.2.0] - 2018-08-10
### Added
- More icons for more resource types
- Added example site.

### Changed
- Fix new item type for which there is no icon.
- Fix include trash doc.
- Move to three dimension version numbering


## [0.0.1] - 2018-03-07
### Added
- Initial version


[Unreleased]: https://github.com/plandes/zotsite/compare/v0.3.5...HEAD
[0.3.5]: https://github.com/plandes/zotsite/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/plandes/zotsite/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/plandes/zotsite/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/plandes/zotsite/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/plandes/zotsite/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/plandes/zotsite/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/plandes/zotsite/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/plandes/zotsite/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/plandes/zotsite/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/plandes/zotsite/compare/v0.1...v0.2.0

<!-- links -->
[BetterBibtex]: https://github.com/retorquere/zotero-better-bibtex
[ZotFile]: http://zotfile.com
[zensols.util]: https://github.com/plandes/util
