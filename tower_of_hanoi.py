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

import tkinter as tk
import time


class TowerOfHanoi:
    # ---------- Visual settings ----------
    CANVAS_WIDTH = 760
    CANVAS_HEIGHT = 420
    DISK_HEIGHT = 28
    BASE_HEIGHT = 20
    DISK_COLORS = [
        "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71",
        "#1abc9c", "#3498db", "#9b59b6", "#e84393",
        "#16a085", "#d35400",
    ]

    def __init__(self, root, num_disks=5):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e272e")

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

    # ---------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------
    def _create_widgets(self):
        title = tk.Label(
            self.root, text="🗼 Tower of Hanoi", font=("Helvetica", 22, "bold"),
            bg="#1e272e", fg="#f5f6fa"
        )
        title.pack(pady=(12, 0))

        subtitle = tk.Label(
            self.root,
            text="Click a tower to pick a disk, then click another to move it",
            font=("Helvetica", 11), bg="#1e272e", fg="#a4b0be"
        )
        subtitle.pack(pady=(0, 8))

        # Info bar
        info_frame = tk.Frame(self.root, bg="#1e272e")
        info_frame.pack(fill="x", padx=20)

        self.lbl_moves = tk.Label(
            info_frame, text="Moves: 0", font=("Helvetica", 13, "bold"),
            bg="#1e272e", fg="#f5f6fa"
        )
        self.lbl_moves.pack(side="left")

        self.lbl_minimum = tk.Label(
            info_frame, text="", font=("Helvetica", 13),
            bg="#1e272e", fg="#a4b0be"
        )
        self.lbl_minimum.pack(side="left", padx=20)

        self.lbl_time = tk.Label(
            info_frame, text="Time: 0.0s", font=("Helvetica", 13, "bold"),
            bg="#1e272e", fg="#f5f6fa"
        )
        self.lbl_time.pack(side="right")

        # Game canvas
        self.canvas = tk.Canvas(
            self.root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
            bg="#2f3640", highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=10)
        self.canvas.bind("<Button-1>", self._click_canvas)

        # Bottom controls
        controls = tk.Frame(self.root, bg="#1e272e")
        controls.pack(pady=(0, 15))

        btn_style = dict(font=("Helvetica", 11, "bold"), bd=0, padx=14, pady=8,
                          activebackground="#40739e", cursor="hand2")

        tk.Button(controls, text="🔄 Restart", bg="#0984e3", fg="white",
                  command=lambda: self.restart(self.num_disks), **btn_style).grid(row=0, column=0, padx=6)

        tk.Button(controls, text="🔢 Change # of disks", bg="#00b894", fg="white",
                  command=self._ask_num_disks, **btn_style).grid(row=0, column=1, padx=6)

        tk.Button(controls, text="🤖 Auto-solve", bg="#6c5ce7", fg="white",
                  command=self._auto_solve, **btn_style).grid(row=0, column=2, padx=6)

        tk.Button(controls, text="↩️ Undo", bg="#636e72", fg="white",
                  command=self._undo, **btn_style).grid(row=0, column=3, padx=6)

        self._clock_tick()

    # ---------------------------------------------------------
    # Custom modal dialog (replaces messagebox / simpledialog)
    # ---------------------------------------------------------
    def _open_dialog(self, width=380):
        """Creates a borderless, styled modal window centered over the main one.
        The height auto-fits the content (computed in _finalize_dialog)."""
        dlg = tk.Toplevel(self.root)
        dlg.overrideredirect(True)
        dlg.configure(bg="#0b0e11")

        # Colored outer border + dark inner card (accented "card" effect)
        border = tk.Frame(dlg, bg="#6c5ce7", padx=2, pady=2)
        border.pack(fill="both", expand=True)
        card = tk.Frame(border, bg="#232833")
        card.pack(fill="both", expand=True)

        # Invisible spacer: sets a minimum width without forcing a fixed height,
        # so the actual content determines the height and nothing gets squished.
        tk.Frame(card, width=width, height=1, bg="#232833").pack()

        return dlg, card

    def _finalize_dialog(self, dlg):
        """Computes the real size based on content, centers the window, and
        safely activates the 'grab' (avoids the Tkinter error if the window
        isn't visible yet)."""
        dlg.update_idletasks()
        width = dlg.winfo_reqwidth()
        height = dlg.winfo_reqheight()
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        dlg.geometry(f"{width}x{height}+{x}+{y}")

        def _safe_grab():
            try:
                dlg.grab_set()
            except tk.TclError:
                pass  # the window wasn't visible yet; harmless, just ignore it

        dlg.after(30, _safe_grab)

    def _dialog_button(self, parent, text, command, bg="#6c5ce7", fg="white"):
        btn = tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            font=("Helvetica", 11, "bold"), bd=0, padx=18, pady=9,
            activebackground="#40739e", cursor="hand2", relief="flat"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self._lighten(bg)))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    @staticmethod
    def _lighten(hex_color):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (min(255, int(c * 1.2 + 15)) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _show_victory(self, moves, total_time, is_perfect):
        dlg, card = self._open_dialog(width=380)

        tk.Label(card, text="🏆", font=("Helvetica", 40), bg="#232833").pack(pady=(24, 4))
        tk.Label(
            card, text="You did it!", font=("Helvetica", 20, "bold"),
            bg="#232833", fg="#f5f6fa"
        ).pack()

        stats = tk.Frame(card, bg="#232833")
        stats.pack(pady=16)

        for label, value in [("Moves", str(moves)), ("Time", f"{total_time:.1f}s")]:
            col = tk.Frame(stats, bg="#2f3542", padx=18, pady=10)
            col.pack(side="left", padx=8)
            tk.Label(col, text=value, font=("Helvetica", 16, "bold"),
                     bg="#2f3542", fg="#00cec9").pack()
            tk.Label(col, text=label, font=("Helvetica", 9),
                     bg="#2f3542", fg="#a4b0be").pack()

        if is_perfect:
            tk.Label(
                card, text="✨ Minimum possible moves! Perfect score ✨",
                font=("Helvetica", 10, "bold"), bg="#232833", fg="#feca57", wraplength=340
            ).pack(pady=(0, 10))

        self._dialog_button(card, "Continue", dlg.destroy).pack(pady=(6, 22))
        self._finalize_dialog(dlg)

    def _show_disk_selector(self):
        dlg, card = self._open_dialog(width=380)

        tk.Label(card, text="🔢", font=("Helvetica", 34), bg="#232833").pack(pady=(22, 2))
        tk.Label(
            card, text="Choose the number of disks", font=("Helvetica", 15, "bold"),
            bg="#232833", fg="#f5f6fa"
        ).pack(pady=(0, 4))

        current_value = tk.IntVar(value=self.num_disks)
        lbl_value = tk.Label(
            card, textvariable=current_value, font=("Helvetica", 26, "bold"),
            bg="#232833", fg="#00cec9"
        )
        lbl_value.pack(pady=(6, 0))

        slider = tk.Scale(
            card, from_=3, to=8, orient="horizontal", variable=current_value,
            length=260, bg="#232833", fg="#f5f6fa", troughcolor="#2f3542",
            highlightthickness=0, bd=0, sliderrelief="flat",
            activebackground="#6c5ce7", showvalue=False
        )
        slider.pack(pady=10)

        def confirm():
            self.restart(current_value.get())
            dlg.destroy()

        buttons = tk.Frame(card, bg="#232833")
        buttons.pack(pady=(6, 22))
        self._dialog_button(buttons, "Cancel", dlg.destroy, bg="#57606f").pack(side="left", padx=6)
        self._dialog_button(buttons, "Apply", confirm).pack(side="left", padx=6)
        self._finalize_dialog(dlg)

    # ---------------------------------------------------------
    # Game logic
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
        tower_width = self.CANVAS_WIDTH / 3
        index = int(x // tower_width)
        if 0 <= index <= 2:
            return index
        return None

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

    # ---------------------------------------------------------
    # Drawing
    # ---------------------------------------------------------
    def _draw(self):
        self.canvas.delete("all")
        tower_width = self.CANVAS_WIDTH / 3
        base_y = self.CANVAS_HEIGHT - 30

        for i in range(3):
            center_x = tower_width * i + tower_width / 2

            # Pole
            self.canvas.create_rectangle(
                center_x - 5, base_y - (self.num_disks + 1) * self.DISK_HEIGHT,
                center_x + 5, base_y,
                fill="#57606f", outline=""
            )
            # Base
            base_color = "#f39c12" if self.selection == i else "#535c68"
            self.canvas.create_rectangle(
                center_x - tower_width / 2 + 20, base_y,
                center_x + tower_width / 2 - 20, base_y + self.BASE_HEIGHT,
                fill=base_color, outline=""
            )
            # Label
            self.canvas.create_text(
                center_x, base_y + self.BASE_HEIGHT + 18,
                text=f"Tower {self.tower_names[i]}",
                fill="#f5f6fa", font=("Helvetica", 12, "bold")
            )

            # Disks
            for level, size in enumerate(self.towers[i]):
                disk_width = 30 + size * (tower_width - 60) / max(self.num_disks, 1)
                y0 = base_y - (level + 1) * self.DISK_HEIGHT
                y1 = base_y - level * self.DISK_HEIGHT
                is_top = level == len(self.towers[i]) - 1
                color = self.DISK_COLORS[(size - 1) % len(self.DISK_COLORS)]
                outline = "#f6e58d" if (is_top and self.selection == i) else ""
                border_width = 3 if outline else 0
                self.canvas.create_rectangle(
                    center_x - disk_width / 2, y0,
                    center_x + disk_width / 2, y1 - 3,
                    fill=color, outline=outline, width=border_width
                )
                self.canvas.create_text(
                    center_x, (y0 + y1) / 2 - 1, text=str(size),
                    fill="white", font=("Helvetica", 10, "bold")
                )

    def _flash_error(self):
        self.canvas.configure(bg="#c0392b")
        self.root.after(150, lambda: self.canvas.configure(bg="#2f3640"))

    def _update_info(self):
        self.lbl_moves.config(text=f"Moves: {self.moves}")

    def _clock_tick(self):
        if self.game_active and self.start_time:
            elapsed = time.time() - self.start_time
            self.lbl_time.config(text=f"Time: {elapsed:.1f}s")
        self.root.after(200, self._clock_tick)


def main():
    root = tk.Tk()
    TowerOfHanoi(root, num_disks=5)
    root.mainloop()


if __name__ == "__main__":
    main()
