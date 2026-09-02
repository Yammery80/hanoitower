"""
Main game class: combines the dialogs, rendering, and game-logic mixins
into a single TowerOfHanoi object. Splitting the responsibilities into
separate files does not change any behavior — every mixin operates on
the same `self`, exactly as if all the methods lived in one class.
"""

try:
    # Works when imported as part of the package (e.g. `from tower_of_hanoi import TowerOfHanoi`)
    from .dialogs import DialogsMixin
    from .rendering import RenderingMixin
    from .game_logic import GameLogicMixin
    from . import constants as C
except ImportError:
    # Works when this file's folder is run directly (e.g. `python main.py`
    # from inside the tower_of_hanoi/ folder) — Python automatically adds
    # that folder to sys.path, so the sibling modules import by plain name.
    from dialogs import DialogsMixin
    from rendering import RenderingMixin
    from game_logic import GameLogicMixin
    import constants as C


class TowerOfHanoi(DialogsMixin, RenderingMixin, GameLogicMixin):
    # ---------- Visual settings (kept here for backwards-compatible access
    # via self.CANVAS_WIDTH, etc., mirrored from constants.py) ----------
    CANVAS_WIDTH = C.CANVAS_WIDTH
    CANVAS_HEIGHT = C.CANVAS_HEIGHT
    DISK_HEIGHT = C.DISK_HEIGHT
    BASE_HEIGHT = C.BASE_HEIGHT
    DISK_COLORS = C.DISK_COLORS

    def __init__(self, root, num_disks=5):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.root.resizable(False, False)
        self.root.configure(bg=C.BG_MAIN)

        self.num_disks = num_disks
        self.towers = [[], [], []]  # lists of disk sizes, last item is the top disk
        self.tower_names = ["A", "B", "C"]
        self.selection = None  # index of the selected tower (0,1,2) or None
        self.moves = 0
        self.start_time = None
        self.game_active = True
        self.solving = False

        self._create_widgets()
        self.restart(num_disks)
