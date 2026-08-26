"""
Torre de Hanoi - Juego interactivo y dinámico
================================================
Requiere: Python 3 con tkinter (viene incluido en la instalación estándar de Python).

Cómo jugar:
- Haz clic en una torre para seleccionar el disco superior (se resalta en amarillo).
- Haz clic en otra torre para moverlo ahí (si el movimiento es válido).
- Objetivo: mover toda la pila de discos desde la Torre A hasta la Torre C,
  usando la Torre B como apoyo, sin poner nunca un disco más grande sobre uno más chico.
- Puedes cambiar el número de discos, reiniciar la partida o pedirle a la
  computadora que resuelva el juego automáticamente (modo demostración).
"""

import tkinter as tk
import time


class TorreHanoi:
    # ---------- Configuración visual ----------
    ANCHO_CANVAS = 760
    ALTO_CANVAS = 420
    ALTO_DISCO = 28
    ALTO_BASE = 20
    COLORES_DISCOS = [
        "#e74c3c", "#e67e22", "#f1c40f", "#2ecc71",
        "#1abc9c", "#3498db", "#9b59b6", "#e84393",
        "#16a085", "#d35400",
    ]

    def __init__(self, root, num_discos=5):
        self.root = root
        self.root.title("Torre de Hanoi")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e272e")

        self.num_discos = num_discos
        self.torres = [[], [], []]  # listas de tamaños de disco, la última es la superior
        self.nombres_torres = ["A", "B", "C"]
        self.seleccion = None  # índice de la torre seleccionada (0,1,2) o None
        self.movimientos = 0
        self.tiempo_inicio = None
        self.juego_activo = True
        self.resolviendo = False

        self._crear_widgets()
        self.reiniciar(num_discos)

    # ---------------------------------------------------------
    # Construcción de la interfaz
    # ---------------------------------------------------------
    def _crear_widgets(self):
        titulo = tk.Label(
            self.root, text="🗼 Torre de Hanoi", font=("Helvetica", 22, "bold"),
            bg="#1e272e", fg="#f5f6fa"
        )
        titulo.pack(pady=(12, 0))

        subtitulo = tk.Label(
            self.root,
            text="Haz clic en una torre para elegir un disco, luego en otra para moverlo",
            font=("Helvetica", 11), bg="#1e272e", fg="#a4b0be"
        )
        subtitulo.pack(pady=(0, 8))

        # Barra de información
        info_frame = tk.Frame(self.root, bg="#1e272e")
        info_frame.pack(fill="x", padx=20)

        self.lbl_movimientos = tk.Label(
            info_frame, text="Movimientos: 0", font=("Helvetica", 13, "bold"),
            bg="#1e272e", fg="#f5f6fa"
        )
        self.lbl_movimientos.pack(side="left")

        self.lbl_minimo = tk.Label(
            info_frame, text="", font=("Helvetica", 13),
            bg="#1e272e", fg="#a4b0be"
        )
        self.lbl_minimo.pack(side="left", padx=20)

        self.lbl_tiempo = tk.Label(
            info_frame, text="Tiempo: 0.0s", font=("Helvetica", 13, "bold"),
            bg="#1e272e", fg="#f5f6fa"
        )
        self.lbl_tiempo.pack(side="right")

        # Lienzo del juego
        self.canvas = tk.Canvas(
            self.root, width=self.ANCHO_CANVAS, height=self.ALTO_CANVAS,
            bg="#2f3640", highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=10)
        self.canvas.bind("<Button-1>", self._click_canvas)

        # Controles inferiores
        controles = tk.Frame(self.root, bg="#1e272e")
        controles.pack(pady=(0, 15))

        estilo_btn = dict(font=("Helvetica", 11, "bold"), bd=0, padx=14, pady=8,
                           activebackground="#40739e", cursor="hand2")

        tk.Button(controles, text="🔄 Reiniciar", bg="#0984e3", fg="white",
                  command=lambda: self.reiniciar(self.num_discos), **estilo_btn).grid(row=0, column=0, padx=6)

        tk.Button(controles, text="🔢 Cambiar # discos", bg="#00b894", fg="white",
                  command=self._pedir_num_discos, **estilo_btn).grid(row=0, column=1, padx=6)

        tk.Button(controles, text="🤖 Resolver automáticamente", bg="#6c5ce7", fg="white",
                  command=self._resolver_automatico, **estilo_btn).grid(row=0, column=2, padx=6)

        tk.Button(controles, text="↩️ Deshacer", bg="#636e72", fg="white",
                  command=self._deshacer, **estilo_btn).grid(row=0, column=3, padx=6)

        self._tick_reloj()

    # ---------------------------------------------------------
    # Diálogo modal personalizado (reemplaza messagebox / simpledialog)
    # ---------------------------------------------------------
    def _abrir_dialogo(self, ancho=380):
        """Crea una ventana modal sin bordes, estilizada, centrada sobre la principal.
        La altura se autoajusta al contenido (se calcula en _finalizar_dialogo)."""
        dlg = tk.Toplevel(self.root)
        dlg.overrideredirect(True)
        dlg.configure(bg="#0b0e11")

        # Borde exterior de color + tarjeta interior oscura (efecto "card" con acento)
        borde = tk.Frame(dlg, bg="#6c5ce7", padx=2, pady=2)
        borde.pack(fill="both", expand=True)
        tarjeta = tk.Frame(borde, bg="#232833")
        tarjeta.pack(fill="both", expand=True)

        # Espaciador invisible: fija el ancho mínimo sin forzar una altura fija,
        # así el contenido real determina el alto y nada queda comprimido.
        tk.Frame(tarjeta, width=ancho, height=1, bg="#232833").pack()

        return dlg, tarjeta

    def _finalizar_dialogo(self, dlg):
        """Calcula el tamaño real según el contenido, centra la ventana y
        activa el 'grab' de forma segura (evita el error de Tkinter si la
        ventana aún no es visible)."""
        dlg.update_idletasks()
        ancho = dlg.winfo_reqwidth()
        alto = dlg.winfo_reqheight()
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - ancho) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - alto) // 2
        dlg.geometry(f"{ancho}x{alto}+{x}+{y}")

        def _grab_seguro():
            try:
                dlg.grab_set()
            except tk.TclError:
                pass  # la ventana todavía no era visible; no pasa nada, se ignora

        dlg.after(30, _grab_seguro)

    def _boton_dialogo(self, parent, texto, comando, bg="#6c5ce7", fg="white"):
        btn = tk.Button(
            parent, text=texto, command=comando, bg=bg, fg=fg,
            font=("Helvetica", 11, "bold"), bd=0, padx=18, pady=9,
            activebackground="#40739e", cursor="hand2", relief="flat"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self._aclarar(bg)))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    @staticmethod
    def _aclarar(color_hex):
        color_hex = color_hex.lstrip("#")
        r, g, b = (int(color_hex[i:i + 2], 16) for i in (0, 2, 4))
        r, g, b = (min(255, int(c * 1.2 + 15)) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _mostrar_victoria(self, movimientos, tiempo_total, es_perfecto):
        dlg, tarjeta = self._abrir_dialogo(ancho=380)

        tk.Label(tarjeta, text="🏆", font=("Helvetica", 40), bg="#232833").pack(pady=(24, 4))
        tk.Label(
            tarjeta, text="¡Lo lograste!", font=("Helvetica", 20, "bold"),
            bg="#232833", fg="#f5f6fa"
        ).pack()

        stats = tk.Frame(tarjeta, bg="#232833")
        stats.pack(pady=16)

        for etiqueta, valor in [("Movimientos", str(movimientos)), ("Tiempo", f"{tiempo_total:.1f}s")]:
            col = tk.Frame(stats, bg="#2f3542", padx=18, pady=10)
            col.pack(side="left", padx=8)
            tk.Label(col, text=valor, font=("Helvetica", 16, "bold"),
                     bg="#2f3542", fg="#00cec9").pack()
            tk.Label(col, text=etiqueta, font=("Helvetica", 9),
                     bg="#2f3542", fg="#a4b0be").pack()

        if es_perfecto:
            tk.Label(
                tarjeta, text="✨ ¡Número mínimo de movimientos! Puntuación perfecta ✨",
                font=("Helvetica", 10, "bold"), bg="#232833", fg="#feca57", wraplength=340
            ).pack(pady=(0, 10))

        self._boton_dialogo(tarjeta, "Continuar", dlg.destroy).pack(pady=(6, 22))
        self._finalizar_dialogo(dlg)

    def _mostrar_selector_discos(self):
        dlg, tarjeta = self._abrir_dialogo(ancho=380)

        tk.Label(tarjeta, text="🔢", font=("Helvetica", 34), bg="#232833").pack(pady=(22, 2))
        tk.Label(
            tarjeta, text="Elige el número de discos", font=("Helvetica", 15, "bold"),
            bg="#232833", fg="#f5f6fa"
        ).pack(pady=(0, 4))

        valor_actual = tk.IntVar(value=self.num_discos)
        lbl_valor = tk.Label(
            tarjeta, textvariable=valor_actual, font=("Helvetica", 26, "bold"),
            bg="#232833", fg="#00cec9"
        )
        lbl_valor.pack(pady=(6, 0))

        slider = tk.Scale(
            tarjeta, from_=3, to=8, orient="horizontal", variable=valor_actual,
            length=260, bg="#232833", fg="#f5f6fa", troughcolor="#2f3542",
            highlightthickness=0, bd=0, sliderrelief="flat",
            activebackground="#6c5ce7", showvalue=False
        )
        slider.pack(pady=10)

        def confirmar():
            self.reiniciar(valor_actual.get())
            dlg.destroy()

        botones = tk.Frame(tarjeta, bg="#232833")
        botones.pack(pady=(6, 22))
        self._boton_dialogo(botones, "Cancelar", dlg.destroy, bg="#57606f").pack(side="left", padx=6)
        self._boton_dialogo(botones, "Aplicar", confirmar).pack(side="left", padx=6)
        self._finalizar_dialogo(dlg)

    # ---------------------------------------------------------
    # Lógica del juego
    # ---------------------------------------------------------
    def reiniciar(self, num_discos):
        self.num_discos = num_discos
        self.torres = [list(range(num_discos, 0, -1)), [], []]
        self.seleccion = None
        self.movimientos = 0
        self.historial = []
        self.tiempo_inicio = time.time()
        self.juego_activo = True
        self.resolviendo = False
        self.victoria_mostrada = False
        minimo = 2 ** num_discos - 1
        self.lbl_minimo.config(text=f"Mínimo posible: {minimo} movimientos")
        self._actualizar_info()
        self._dibujar()

    def _pedir_num_discos(self):
        self._mostrar_selector_discos()

    def _click_canvas(self, event):
        if not self.juego_activo or self.resolviendo:
            return

        torre_clic = self._torre_desde_click(event.x)
        if torre_clic is None:
            return

        if self.seleccion is None:
            # Seleccionar torre de origen (debe tener al menos un disco)
            if self.torres[torre_clic]:
                self.seleccion = torre_clic
                self._dibujar()
        else:
            if torre_clic == self.seleccion:
                # Clic en la misma torre: deseleccionar
                self.seleccion = None
                self._dibujar()
            else:
                self._mover(self.seleccion, torre_clic, registrar=True)
                self.seleccion = None

    def _torre_desde_click(self, x):
        ancho_torre = self.ANCHO_CANVAS / 3
        indice = int(x // ancho_torre)
        if 0 <= indice <= 2:
            return indice
        return None

    def _movimiento_valido(self, origen, destino):
        if not self.torres[origen]:
            return False
        if self.torres[destino] and self.torres[destino][-1] < self.torres[origen][-1]:
            return False
        return True

    def _mover(self, origen, destino, registrar=True):
        if not self._movimiento_valido(origen, destino):
            self._flash_error()
            return False

        disco = self.torres[origen].pop()
        self.torres[destino].append(disco)
        self.movimientos += 1
        if registrar:
            self.historial.append((origen, destino))

        self._actualizar_info()
        self._dibujar()
        self._revisar_victoria()
        return True

    def _deshacer(self):
        if not self.historial or self.resolviendo:
            return
        origen, destino = self.historial.pop()
        # Revertir: mover el disco de vuelta de destino a origen
        disco = self.torres[destino].pop()
        self.torres[origen].append(disco)
        self.movimientos += 1
        self.seleccion = None
        self._actualizar_info()
        self._dibujar()

    def _revisar_victoria(self):
        if self.victoria_mostrada:
            return
        if len(self.torres[2]) == self.num_discos:
            self.victoria_mostrada = True
            self.juego_activo = False
            tiempo_total = time.time() - self.tiempo_inicio
            minimo = 2 ** self.num_discos - 1
            es_perfecto = self.movimientos == minimo
            self._mostrar_victoria(self.movimientos, tiempo_total, es_perfecto)

    # ---------------------------------------------------------
    # Resolución automática (algoritmo recursivo clásico)
    # ---------------------------------------------------------
    def _resolver_automatico(self):
        if self.resolviendo:
            return
        self.reiniciar(self.num_discos)
        self.resolviendo = True
        self.juego_activo = False
        self.seleccion = None

        self._pasos = []
        self._generar_pasos(self.num_discos, 0, 2, 1)
        self._ejecutar_pasos_animados()

    def _generar_pasos(self, n, origen, destino, auxiliar):
        if n == 0:
            return
        self._generar_pasos(n - 1, origen, auxiliar, destino)
        self._pasos.append((origen, destino))
        self._generar_pasos(n - 1, auxiliar, destino, origen)

    def _ejecutar_pasos_animados(self):
        if not self._pasos:
            self.resolviendo = False
            self.juego_activo = True
            self._revisar_victoria()
            return
        origen, destino = self._pasos.pop(0)
        self._mover(origen, destino, registrar=False)
        self.root.after(400, self._ejecutar_pasos_animados)

    # ---------------------------------------------------------
    # Dibujo
    # ---------------------------------------------------------
    def _dibujar(self):
        self.canvas.delete("all")
        ancho_torre = self.ANCHO_CANVAS / 3
        base_y = self.ALTO_CANVAS - 30

        for i in range(3):
            centro_x = ancho_torre * i + ancho_torre / 2

            # Poste
            self.canvas.create_rectangle(
                centro_x - 5, base_y - (self.num_discos + 1) * self.ALTO_DISCO,
                centro_x + 5, base_y,
                fill="#57606f", outline=""
            )
            # Base
            color_base = "#f39c12" if self.seleccion == i else "#535c68"
            self.canvas.create_rectangle(
                centro_x - ancho_torre / 2 + 20, base_y,
                centro_x + ancho_torre / 2 - 20, base_y + self.ALTO_BASE,
                fill=color_base, outline=""
            )
            # Etiqueta
            self.canvas.create_text(
                centro_x, base_y + self.ALTO_BASE + 18,
                text=f"Torre {self.nombres_torres[i]}",
                fill="#f5f6fa", font=("Helvetica", 12, "bold")
            )

            # Discos
            for nivel, tam in enumerate(self.torres[i]):
                ancho_disco = 30 + tam * (ancho_torre - 60) / max(self.num_discos, 1)
                y0 = base_y - (nivel + 1) * self.ALTO_DISCO
                y1 = base_y - nivel * self.ALTO_DISCO
                es_superior = nivel == len(self.torres[i]) - 1
                color = self.COLORES_DISCOS[(tam - 1) % len(self.COLORES_DISCOS)]
                outline = "#f6e58d" if (es_superior and self.seleccion == i) else ""
                ancho_borde = 3 if outline else 0
                self.canvas.create_rectangle(
                    centro_x - ancho_disco / 2, y0,
                    centro_x + ancho_disco / 2, y1 - 3,
                    fill=color, outline=outline, width=ancho_borde
                )
                self.canvas.create_text(
                    centro_x, (y0 + y1) / 2 - 1, text=str(tam),
                    fill="white", font=("Helvetica", 10, "bold")
                )

    def _flash_error(self):
        self.canvas.configure(bg="#c0392b")
        self.root.after(150, lambda: self.canvas.configure(bg="#2f3640"))

    def _actualizar_info(self):
        self.lbl_movimientos.config(text=f"Movimientos: {self.movimientos}")

    def _tick_reloj(self):
        if self.juego_activo and self.tiempo_inicio:
            transcurrido = time.time() - self.tiempo_inicio
            self.lbl_tiempo.config(text=f"Tiempo: {transcurrido:.1f}s")
        self.root.after(200, self._tick_reloj)


def main():
    root = tk.Tk()
    TorreHanoi(root, num_discos=5)
    root.mainloop()


if __name__ == "__main__":
    main()
