# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased]


### Added
- Collections filtering using regular expressions is now fully supported.
- Ability to link directly to any item in the hierarchy.
- Link button that copies the current page URL to the clipboard.
- Added [BetterBibtex] references for easy linking to the site with citation
  keys.
- HTML (i.e. snapshots) are now visible in the pane PDFs are displayed.
- Short files to reduce character/file system conflicts.
- Clear button to reset the interface.

### Changed
- Refactored: cleaned up class structure and graph iteration OO class patterns.
- Changed default naming to use short files.
- Retrofit new actioncli features.
- Simpler command line by moving configuration to the configuration file.
- Move to more advanced configparser, which uses new notation (example:
  `$(HOME)s` -> `${HOME}`).


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


[Unreleased]: https://github.com/plandes/zotsite/compare/v0.2.3...HEAD
[0.2.3]: https://github.com/plandes/zotsite/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/plandes/zotsite/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/plandes/zotsite/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/plandes/zotsite/compare/v0.1...v0.2.0

<!-- links -->
[BetterBibtex]: https://github.com/retorquere/zotero-better-bibtex
