# Changelog

## [0.3.0] - 2025-01-12

### Added

- Add new shaft
- Add Beam AGS TSH SYM ESS
- Add Brace STR SLT SQT ERR
- Add Spacer FRE
- Add Spacer FXD
- Add Spacer BUD FRE
- Add bevel and involute gears

### Changed

- **Breaking:** Migration of beams, braces and connectors code, old parts properties values are reset.
- Refine objects' shape, still can use simple shape
- Update translations

### Fixed

- Set limits on integer properties preventing entering bad data

## [0.2.4] - 2024-11-08

### Fixed

- Add SVG icons for beams and missing braces commands
- Fix error when there are no STEMFIE parts on the tree

## [0.2.3] - 2024-11-06

### Fixed

- Fix typo "Caudrado" -> "Cuadrado"
- Add SVG icons for some braces' commands

## [0.2.2] - 2024-11-05

### Fixed

- Fix some commands' names

## [0.2.1] - 2024-11-03

### Changed

- Use normal words on commands' tooltips, better suited for translation
- Update Spanish translation

## [0.2.0] - 2024-10-31

### Added

- Add parametric plates: 3 models
- Add parametric shaft: 1 model
- Upgrade workbench structure
- Update workbench icon
- Add `ViewProvider` class to assign icon to objects on the tree view
- Add translation support
- Add Spanish translation
- Objects get a random color when created
- Apply [black][black] formatting to code (the same is used on main FreeCAD)

### Fixed

- Use words on command tooltips instead of acronyms
- Add SVG icons for connectors' commands

## [0.1.0] - 2021-09-19

🌱 Initial release.

### Added

- Add parametric braces: 12 models
- Add parametric beams: 8 models
- Add parametric connectors: 5 models
- BOM command that lists used components on the console

[black]: https://github.com/psf/black
[0.1.0]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.1.0
[0.2.0]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.2.0
[0.2.1]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.2.1
[0.2.2]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.2.2
[0.2.3]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.2.3
[0.2.4]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.2.4
[0.3.0]: https://github.com/bilbaomakers/StemfieWB/releases/tag/0.3.0
