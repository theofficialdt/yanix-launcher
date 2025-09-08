# Yanix-Launcher
<img width="1000" height="1000" alt="yanix" src="https://github.com/user-attachments/assets/c033695c-6a80-4126-9531-87bb9cef1e1b" />


Yanix-Launcher is an independent, open-source launcher for Yandere Simulator, built specifically for Linux. This project is not affiliated with or supported by YandereDev in any way.

It runs the game using WINE (version 8.0 or higher is recommended). Depending on your setup, you might see a few graphical issues, but most major bugs were resolved in the Unity 6 build. Some letters may still appear glitched or not render properly — that's a problem with the game itself and needs to be fixed by YandereDev, not the launcher team.

Yanix is developed and tested for Linux.
A macOS version has already been optimized.
A Windows version is planned but not available yet.

If you’re experiencing issues like a white screen when launching the game (aka "White Screen of Death"), run the following command to fix it:

`winetricks dxvk`

If letters are missing or broken in-game, don’t bother switching to GE-Proton. Instead, run:

`winetricks corefonts # or allfonts`

These fixes target the core issues with how Yandere Simulator interacts with WINE and fonts.


Requirements

Before running Yanix-Launcher, make sure the following packages are installed:

PyQt5 – for the graphical interface

PyQtWebEngine – for embedded web content

requests – used for update checks and networking

WINE – to run the game

winetricks – for managing WINE components and tweaks


Installation

Ubuntu/Debian:
```
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine python3-requests wine winetricks
```

Arch Linux:
```
sudo pacman -S python-pyqt5 python-pyqtwebengine python-requests wine winetricks
```
Fedora:
```
sudo dnf install python3-qt5 python3-qt5-webengine python3-requests wine winetricks
```
