# Autobackupper for Backpack Hero

## Why

The savegames of Backpack Hero sometimes gets corrupted. This program is meant to fix that. It starts the game and checks for any modifications in the savegame folder. If there are new savegame files present, it will zip them up to a backup folder. They can then be extracted back to the savegame folder. The save files of interest are:

- bphStoryModeOverworld\*.sav The village that you're building
- bphStoryModeMetaData\*.sav Probably tells whether you are in the dungeon or in the village
- bphStoryModeRun\*.sav Your place and stuff in the dungeon

## Requirements

- 7zip
- Python
- Backpack Hero

Download "64-bit Windows x64" 7zip from here: https://7-zip.org/download.html<br>
Download the latest Python from here: https://www.python.org/downloads/

## How to install

Copy the file autobackup_backpack_hero.py to anywhere in your computer. I suggest the folder where the game was installed. Then run:

*python -m pip install --upgrade pip*<br>
*pip install watchdog*<br>
*pip install pypiwin32*<br>

## How to configure

Edit the lines 15 and 16 in the file autobackup_backpack_hero.py to point to your 7zip and game install executables.

## How to run

*python autobackup_backpack_hero.py*
