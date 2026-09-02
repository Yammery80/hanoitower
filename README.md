# 🗼 Tower of Hanoi

An interactive, dynamic Tower of Hanoi game built in Python with `tkinter`.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

## 📋 Requirements

- **Python 3.7 or higher**
- **tkinter** (included by default in most Python installations)

No extra libraries (`pip install`) are needed — the game only uses Python's standard library.

### Check that you have tkinter

On some Linux distributions, `tkinter` doesn't come pre-installed. Check with:

```bash
python3 -m tkinter
```

If a small test window pops up, you're good to go. If it errors out, install it for your system:

| System | Command |
|---|---|
| **Windows** | Included by default with the official installer from python.org |
| **macOS** | Included with Python from python.org (not always with the Homebrew build) |
| **Ubuntu / Debian** | `sudo apt install python3-tk` |
| **Fedora** | `sudo dnf install python3-tkinter` |
| **Arch Linux** | `sudo pacman -S tk` |

## 📥 Installation

1. Download the whole `tower_of_hanoi/` folder (all the files listed in [Project structure](#-project-structure) below).
2. Place the folder anywhere on your computer, keeping all files together inside it.
3. That's it — no build step or extra install needed.

## 📁 Project structure

The game is split into several files inside the `tower_of_hanoi/` folder, each with a single responsibility:

```
tower_of_hanoi/
├── __init__.py       # Makes the folder an importable package
├── main.py           # Entry point — run this to play
├── app.py            # Main TowerOfHanoi class, combines all the pieces below
├── constants.py       # Colors and board dimensions
├── game_logic.py       # Game rules: moves, undo, win check, auto-solve
├── rendering.py       # Builds the UI and draws the board on the canvas
└── dialogs.py       # Custom modal dialogs (victory screen, disk-count selector)
```

All files must stay together in the same folder for imports to work.

## ▶️ How to run the game

Open a terminal (or command prompt), navigate **into** the `tower_of_hanoi/` folder, and run:

```bash
cd tower_of_hanoi
python3 main.py
```

Alternatively, from the folder that *contains* `tower_of_hanoi/`, you can run it as a module:

```bash
python3 -m tower_of_hanoi.main
```

> On Windows, if `python3` doesn't work, try `python` instead.

## 🎮 How to play

1. Click a tower to **select** its top disk (it highlights in yellow).
2. Click another tower to **move it** there.
3. **Goal:** move the entire stack of disks from Tower A to Tower C, using Tower B as a helper — never placing a bigger disk on top of a smaller one.

### Available controls

| Button | Function |
|---|---|
| 🔄 **Restart** | Starts the current game over |
| 🔢 **Change # of disks** | Choose between 3 and 8 disks with a slider |
| 🤖 **Auto-solve** | The computer solves the puzzle step by step (demo mode) |
| ↩️ **Undo** | Reverts the last move |

The game tracks your **moves** and **elapsed time**, and shows you the minimum number of moves possible (2ⁿ − 1). If you match the minimum, you get a perfect score! 🏆

## 🛠️ Troubleshooting

- **"No module named tkinter"** → install tkinter following the table above and try again.
- **"No module named 'tower_of_hanoi'" or import errors** → make sure you kept all the files together inside the `tower_of_hanoi/` folder, and that you're running the command from the right location (see [How to run the game](#%EF%B8%8F-how-to-run-the-game) above).
- **The window looks too small/large** → the window size is fixed by design; this can vary with your screen's scaling settings.
- **Nothing happens when I click** → make sure you're clicking inside the tower area (the dark canvas), not on the buttons.

## 📄 License

Free to use, modify, and share.
