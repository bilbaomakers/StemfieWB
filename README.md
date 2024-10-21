# Stemfie Workbench

[![license][license_badge]][license]
[![FreeCAD Addon Manager][AddonMgr_badge]][AddonMgr]
[![GitHub Tag][tag_bagde]][tag]

[FreeCAD][FreeCAD] workbench for the [STEMFIE][STEMFIE] construction system.

## Installation

### Automatic Installation

The recommended way to install Stemfie is via FreeCAD's
[Addon Manager](https://wiki.freecad.org/Std_AddonMgr) under
`Tools > Addon Manager` dropdown menu.

Search for **Stemfie** in the workbench category.

### Manual installation

The install path for FreeCAD modules depends on the operating system used.

To find where is the user's application data directory enter next command on
FreeCAD's Python console.

```python
App.getUserAppDataDir()
```

Examples on different OS

- Linux: `/home/user/.local/share/FreeCAD/Mod/`
- macOS: `/Users/user/Library/Preferences/FreeCAD/Mod/`
- Windows: `C:\Users\user\AppData\Roaming\FreeCAD\Mod\`

Use the CLI to enter the `Mod` directory and use Git to install Stemfie:

```shell
git clone https://github.com/bilbaomakers/StemfieWB
```

If you are updating the code, restarting FreeCAD is advised.

[license]: ./LICENSE
[license_badge]: <https://img.shields.io/github/license/bilbaomakers/StemfieWB>
[AddonMgr]: <https://github.com/FreeCAD/FreeCAD-addons>
[AddonMgr_badge]: <https://img.shields.io/badge/FreeCAD%20addon%20manager-available-brightgreen>
[tag]: <https://github.com/bilbaomakers/StemfieWB/releases>
[tag_bagde]: <https://img.shields.io/github/v/tag/bilbaomakers/StemfieWB>
[FreeCAD]: https://freecad.org
[STEMFIE]: https://stemfie.org/
