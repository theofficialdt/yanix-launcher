# Yanix-Launcher 
<img width="1280" height="1280" alt="9 Sem Título_20250905172924" src="https://github.com/user-attachments/assets/29fd87b1-5d22-4040-ad70-e024b0405046" />


**Yanix-Launcher** is an independent, open‑source launcher for **Yandere Simulator**, built for **Linux**. This project is **not** affiliated with or endorsed by **YandereDev**.

Yanix runs the game through **WINE** (we recommend **WINE 8.0+**). Depending on your setup you might see a few graphical quirks, but most major issues were resolved in the Unity 6 build. If some characters look broken or don’t render, that’s a **game-side** problem for YandereDev to fix — not the launcher.

* **Primary platform:** Linux
* **macOS:** Not Supported.
* **Windows:** 50% - Pad mode don't runs natively.

System Requirements
-------------------

Linux:
- Intel i5 8th Gen / Ryzen 4000 Series (except 5 and 3)
- 12 GB RAM
- 3 GB Free Disk Space
- 4 GB VRAM/GTT

Mac:
- M1 / Intel i7 8th Gen / Hackintosh (run with Rosetta2 for Apple Silicon)
- 12 GB RAM
- 3 GB Free Disk Space
- 4 GB VRAM/GTT

Installation
------------

Ubuntu / Debian:
```
sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine python3-requests wine winetricks
```
Arch Linux:
```
sudo pacman -S python-pyqt6 python-pyqt6-webengine python-requests wine winetricks
```
Fedora:
```
sudo dnf install python3-pyqt6 python3-pyqt6-webengine python3-requests wine winetricks

```
Optional Dependencies
---------------------

These are optional but recommended for enhanced functionality:
```
pip install pygame pypresence
```
- pygame — for "Pad Mode"
- pypresence — for Discord Rich Presence integration


## Notes

* WINE **8.0 or newer** is recommended.
* Graphics/text glitches are generally **game** issues, not Yanix-Launcher bugs.

---

## License & Credits

* Yanix-Launcher is open source and independent.
* Yandere Simulator © YandereDev. All trademarks belong to their respective owners.
