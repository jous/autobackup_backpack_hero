# Autobackupper for Backpack Hero

## Requirements:

- 7zip
- python
- backpack hero

Download "64-bit Windows x64" 7zip from here: https://7-zip.org/download.html
Download the latest Python from here: https://www.python.org/downloads/

## How to install

Copy the file autobackup_backpack_hero.py to anywhere in your computer. I suggest the folder where the game was installed. Then run 

**python -m pip install --upgrade pip**
**pip install watchdog**
**pip install pypiwin32**

## How to configure

edit lines 15 and 16 in the file autobackup_backpack_hero.py to point to your 7zip and game install executables.

## How to run

python autobackup_backpack_hero.py
