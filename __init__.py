"""
Tower of Hanoi - Interactive, dynamic game
================================================
Requires: Python 3 with tkinter (included in the standard Python installation).

How to play:
- Click a tower to select its top disk (it highlights in yellow).
- Click another tower to move it there (if the move is valid).
- Goal: move the whole stack of disks from Tower A to Tower C,
  using Tower B as a helper, never placing a bigger disk on a smaller one.
- You can change the number of disks, restart the game, or ask the
  computer to solve it automatically (demo mode).
"""

try:
    from .app import TowerOfHanoi
except ImportError:
    # Only needed if something ends up importing this __init__.py directly
    # without a proper package context (e.g. via sys.path tricks).
    from app import TowerOfHanoi

__all__ = ["TowerOfHanoi"]
