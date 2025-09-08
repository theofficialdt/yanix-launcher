# Yanix-Launcher (PyQt6)

<img width="1280" height="1280" alt="9 Sem Título_20250905172924" src="https://github.com/user-attachments/assets/29fd87b1-5d22-4040-ad70-e024b0405046" />


**Yanix-Launcher** is an independent, open‑source launcher for **Yandere Simulator**, built for **Linux**. This project is **not** affiliated with or endorsed by **YandereDev**.

Yanix runs the game through **WINE** (we recommend **WINE 8.0+**). Depending on your setup you might see a few graphical quirks, but most major issues were resolved in the Unity 6 build. If some characters look broken or don’t render, that’s a **game-side** problem for YandereDev to fix — not the launcher.

* **Primary platform:** Linux
* **macOS:** optimized build exists
* **Windows:** planned, not available yet

---

## Quick Fixes (Common Issues)

**White screen on launch (aka “White Screen of Death”)**

```bash
winetricks dxvk
```

**Missing/broken letters in‑game** – don’t switch to GE‑Proton; instead install fonts:

```bash
winetricks corefonts   # or: winetricks allfonts
```

These target how Yandere Simulator interacts with WINE and system fonts.

---

## Requirements

Before running Yanix-Launcher, make sure these are installed:

* **PyQt6** – UI toolkit
* **PyQt6-WebEngine** – embedded web content
* **requests** – update checks & networking
* **WINE** – runs the game
* **winetricks** – manages WINE components/tweaks

> If your distro doesn’t provide the packages below, you can also install via `pip`:
>
> ```bash
> python -m pip install PyQt6 PyQt6-WebEngine requests --break-system-packages
> ```

---

## Installation

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine python3-requests wine winetricks
```

### Arch Linux

```bash
sudo pacman -S python-pyqt6 python-pyqt6-webengine python-requests wine winetricks
```

### Fedora

```bash
sudo dnf install python3-pyqt6 python3-pyqt6-webengine python3-requests wine winetricks
```

---

## Notes

* WINE **8.0 or newer** is recommended.
* Yanix focuses on **Linux** first. macOS builds are tuned; Windows is planned.
* Graphics/text glitches are generally **game** issues, not Yanix-Launcher bugs.

---

## License & Credits

* Yanix-Launcher is open source and independent.
* Yandere Simulator © YandereDev. All trademarks belong to their respective owners.
