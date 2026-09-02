"""
Core game logic: moves, undo, victory check, and the auto-solve algorithm.

GameLogicMixin is meant to be combined with the main game class via
multiple inheritance, so `self` here refers to the same instance that
holds `self.towers`, `self.canvas`, `self.root`, etc.
"""

import time

try:
    from . import constants as C
except ImportError:
    import constants as C


class GameLogicMixin:
    # ---------------------------------------------------------
    # Game state
    # ---------------------------------------------------------
    def restart(self, num_disks):
        self.num_disks = num_disks
        self.towers = [list(range(num_disks, 0, -1)), [], []]
        self.selection = None
        self.moves = 0
        self.history = []
        self.start_time = time.time()
        self.game_active = True
        self.solving = False
        self.victory_shown = False
        minimum = 2 ** num_disks - 1
        self.lbl_minimum.config(text=f"Minimum possible: {minimum} moves")
        self._update_info()
        self._draw()

    def _ask_num_disks(self):
        self._show_disk_selector()

    # ---------------------------------------------------------
    # Input handling
    # ---------------------------------------------------------
    def _click_canvas(self, event):
        if not self.game_active or self.solving:
            return

        clicked_tower = self._tower_from_click(event.x)
        if clicked_tower is None:
            return

        if self.selection is None:
            # Select the source tower (must have at least one disk)
            if self.towers[clicked_tower]:
                self.selection = clicked_tower
                self._draw()
        else:
            if clicked_tower == self.selection:
                # Clicked the same tower: deselect
                self.selection = None
                self._draw()
            else:
                self._move(self.selection, clicked_tower, record=True)
                self.selection = None

    def _tower_from_click(self, x):
        tower_width = C.CANVAS_WIDTH / 3
        index = int(x // tower_width)
        if 0 <= index <= 2:
            return index
        return None

    # ---------------------------------------------------------
    # Moves
    # ---------------------------------------------------------
    def _valid_move(self, source, destination):
        if not self.towers[source]:
            return False
        if self.towers[destination] and self.towers[destination][-1] < self.towers[source][-1]:
            return False
        return True

    def _move(self, source, destination, record=True):
        if not self._valid_move(source, destination):
            self._flash_error()
            return False

        disk = self.towers[source].pop()
        self.towers[destination].append(disk)
        self.moves += 1
        if record:
            self.history.append((source, destination))

        self._update_info()
        self._draw()
        self._check_victory()
        return True

    def _undo(self):
        if not self.history or self.solving:
            return
        source, destination = self.history.pop()
        # Revert: move the disk back from destination to source
        disk = self.towers[destination].pop()
        self.towers[source].append(disk)
        self.moves += 1
        self.selection = None
        self._update_info()
        self._draw()

    def _check_victory(self):
        if self.victory_shown:
            return
        if len(self.towers[2]) == self.num_disks:
            self.victory_shown = True
            self.game_active = False
            total_time = time.time() - self.start_time
            minimum = 2 ** self.num_disks - 1
            is_perfect = self.moves == minimum
            self._show_victory(self.moves, total_time, is_perfect)

    # ---------------------------------------------------------
    # Auto-solve (classic recursive algorithm)
    # ---------------------------------------------------------
    def _auto_solve(self):
        if self.solving:
            return
        self.restart(self.num_disks)
        self.solving = True
        self.game_active = False
        self.selection = None

        self._steps = []
        self._generate_steps(self.num_disks, 0, 2, 1)
        self._run_animated_steps()

    def _generate_steps(self, n, source, destination, auxiliary):
        if n == 0:
            return
        self._generate_steps(n - 1, source, auxiliary, destination)
        self._steps.append((source, destination))
        self._generate_steps(n - 1, auxiliary, destination, source)

    def _run_animated_steps(self):
        if not self._steps:
            self.solving = False
            self.game_active = True
            self._check_victory()
            return
        source, destination = self._steps.pop(0)
        self._move(source, destination, record=False)
        self.root.after(400, self._run_animated_steps)
