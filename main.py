"""
Entry point. Run with:  python3 main.py  (from inside this folder)
"""

import tkinter as tk

try:
    # Works when run as part of the package (e.g. `python3 -m tower_of_hanoi.main`)
    from .app import TowerOfHanoi
except ImportError:
    # Works when this file is executed directly (e.g. `python3 main.py` from
    # inside the tower_of_hanoi/ folder). Python automatically adds this
    # file's own folder to sys.path in that case, so a plain import works.
    from app import TowerOfHanoi


def main():
    root = tk.Tk()
    TowerOfHanoi(root, num_disks=5)
    root.mainloop()


if __name__ == "__main__":
    main()
