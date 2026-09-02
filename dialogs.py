"""
Custom modal dialogs (replaces messagebox / simpledialog).

DialogsMixin is meant to be combined with the main game class via
multiple inheritance, so `self` here refers to the same instance that
holds `self.root`, `self.num_disks`, etc.
"""

import tkinter as tk


class DialogsMixin:
    # ---------------------------------------------------------
    # Generic modal dialog scaffolding
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

    # ---------------------------------------------------------
    # Specific dialogs
    # ---------------------------------------------------------
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
