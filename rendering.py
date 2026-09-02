"""
UI construction and canvas drawing.

RenderingMixin is meant to be combined with the main game class via
multiple inheritance, so `self` here refers to the same instance that
holds `self.root`, `self.towers`, `self.canvas`, etc.
"""

import tkinter as tk
import time

try:
    from . import constants as C
except ImportError:
    import constants as C


class RenderingMixin:
    # ---------------------------------------------------------
    # UI construction
    # ---------------------------------------------------------
    def _create_widgets(self):
        title = tk.Label(
            self.root, text="🗼 Tower of Hanoi", font=("Helvetica", 22, "bold"),
            bg=C.BG_MAIN, fg=C.FG_TEXT
        )
        title.pack(pady=(12, 0))

        subtitle = tk.Label(
            self.root,
            text="Click a tower to pick a disk, then click another to move it",
            font=("Helvetica", 11), bg=C.BG_MAIN, fg=C.FG_TEXT_MUTED
        )
        subtitle.pack(pady=(0, 8))

        # Info bar
        info_frame = tk.Frame(self.root, bg=C.BG_MAIN)
        info_frame.pack(fill="x", padx=20)

        self.lbl_moves = tk.Label(
            info_frame, text="Moves: 0", font=("Helvetica", 13, "bold"),
            bg=C.BG_MAIN, fg=C.FG_TEXT
        )
        self.lbl_moves.pack(side="left")

        self.lbl_minimum = tk.Label(
            info_frame, text="", font=("Helvetica", 13),
            bg=C.BG_MAIN, fg=C.FG_TEXT_MUTED
        )
        self.lbl_minimum.pack(side="left", padx=20)

        self.lbl_time = tk.Label(
            info_frame, text="Time: 0.0s", font=("Helvetica", 13, "bold"),
            bg=C.BG_MAIN, fg=C.FG_TEXT
        )
        self.lbl_time.pack(side="right")

        # Game canvas
        self.canvas = tk.Canvas(
            self.root, width=C.CANVAS_WIDTH, height=C.CANVAS_HEIGHT,
            bg=C.BG_CANVAS, highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=10)
        self.canvas.bind("<Button-1>", self._click_canvas)

        # Bottom controls
        controls = tk.Frame(self.root, bg=C.BG_MAIN)
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
    # Drawing
    # ---------------------------------------------------------
    def _draw(self):
        self.canvas.delete("all")
        tower_width = C.CANVAS_WIDTH / 3
        base_y = C.CANVAS_HEIGHT - 30

        for i in range(3):
            center_x = tower_width * i + tower_width / 2

            # Pole
            self.canvas.create_rectangle(
                center_x - 5, base_y - (self.num_disks + 1) * C.DISK_HEIGHT,
                center_x + 5, base_y,
                fill=C.TOWER_POLE_COLOR, outline=""
            )
            # Base
            base_color = C.TOWER_BASE_SELECTED_COLOR if self.selection == i else C.TOWER_BASE_COLOR
            self.canvas.create_rectangle(
                center_x - tower_width / 2 + 20, base_y,
                center_x + tower_width / 2 - 20, base_y + C.BASE_HEIGHT,
                fill=base_color, outline=""
            )
            # Label
            self.canvas.create_text(
                center_x, base_y + C.BASE_HEIGHT + 18,
                text=f"Tower {self.tower_names[i]}",
                fill=C.FG_TEXT, font=("Helvetica", 12, "bold")
            )

            # Disks
            for level, size in enumerate(self.towers[i]):
                disk_width = 30 + size * (tower_width - 60) / max(self.num_disks, 1)
                y0 = base_y - (level + 1) * C.DISK_HEIGHT
                y1 = base_y - level * C.DISK_HEIGHT
                is_top = level == len(self.towers[i]) - 1
                color = C.DISK_COLORS[(size - 1) % len(C.DISK_COLORS)]
                outline = C.DISK_SELECTED_OUTLINE if (is_top and self.selection == i) else ""
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
        self.canvas.configure(bg=C.BG_CANVAS_ERROR)
        self.root.after(150, lambda: self.canvas.configure(bg=C.BG_CANVAS))

    def _update_info(self):
        self.lbl_moves.config(text=f"Moves: {self.moves}")

    def _clock_tick(self):
        if self.game_active and self.start_time:
            elapsed = time.time() - self.start_time
            self.lbl_time.config(text=f"Time: {elapsed:.1f}s")
        self.root.after(200, self._clock_tick)
