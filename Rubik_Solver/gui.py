import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import copy
import random
import rbk

# Mapeo de letras a colores reales para la interfaz
COLORS = {
    'W': 'white',
    'O': '#FFA500', # Naranja
    'G': 'green',
    'R': 'red',
    'Y': 'yellow',
    'B': 'blue',
    '': '#E0E0E0' # Gris claro para celdas vacías
}

# El orden en el que rotarán los colores al hacer clic
ORDER = ['W', 'O', 'G', 'R', 'Y', 'B']

class RubikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik Solver GUI")
        self.root.configure(bg='#F0F0F0')
        
        self.buttons = {}
        self.selected_color = 'W' # Color seleccionado por defecto
        
        self.palette_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.palette_frame.pack(pady=10)
        self.build_palette()
        
        self.grid_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.grid_frame.pack(padx=20, pady=10)
        
        self.build_grid()
        
        self.solve_btn = tk.Button(self.root, text="Resolver Cubo", font=('Arial', 14, 'bold'), 
                                   bg='#4CAF50', fg='white', command=self.solve)
        self.solve_btn.pack(pady=10)
        
        self.shuffle_btn = tk.Button(self.root, text="Mezclar Cubo", font=('Arial', 12, 'bold'), 
                                     bg='#FF9800', fg='white', command=self.shuffle)
        self.shuffle_btn.pack(pady=5)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate', variable=self.progress_var)
        self.progress_bar.pack(pady=10)
        
        self.result_lbl = tk.Label(self.root, text="Ingresa el estado de tu cubo interactuando con los cuadros.", 
                                   font=('Arial', 12), bg='#F0F0F0', wraplength=450)
        self.result_lbl.pack(pady=20)

    def is_valid_cell(self, r, c):
        # Validar las dimensiones 9x12 en forma horizontal cruzada
        if 0 <= r <= 2 and 3 <= c <= 5: return True # ARRIBA
        if 3 <= r <= 5 and 0 <= c <= 11: return True # IZQUIERDA, FRENTE, DERECHA, ATRAS
        if 6 <= r <= 8 and 3 <= c <= 5: return True # ABAJO
        return False

    def build_grid(self):
        # Inicializar con la matriz resuelta
        estado_base = rbk.ESTADO_RESUELTO
        
        for r in range(9):
            for c in range(12):
                if self.is_valid_cell(r, c):
                    # Valor inicial
                    val = estado_base[r][c]
                    btn = tk.Button(self.grid_frame, width=4, height=2, bg=COLORS[val], 
                                    activebackground=COLORS[val], relief="groove",
                                    command=lambda r=r, c=c: self.change_color(r, c))
                    btn.grid(row=r, column=c, padx=1, pady=1)
                    
                    self.buttons[(r, c)] = {'widget': btn, 'color': val}
                else:
                    # Espacios sin piezas del cubo
                    lbl = tk.Frame(self.grid_frame, width=35, height=40, bg='#F0F0F0')
                    lbl.grid(row=r, column=c, padx=1, pady=1)

    def build_palette(self):
        lbl = tk.Label(self.palette_frame, text="Paleta de Colores:", bg='#F0F0F0', font=('Arial', 10, 'bold'))
        lbl.pack(side=tk.LEFT, padx=10)
        
        self.palette_buttons = {}
        for color_code in ORDER:
            btn = tk.Button(self.palette_frame, width=4, height=2, bg=COLORS[color_code],
                            activebackground=COLORS[color_code], 
                            relief="sunken" if color_code == self.selected_color else "raised",
                            bd=3 if color_code == self.selected_color else 1,
                            command=lambda c=color_code: self.select_color(c))
            btn.pack(side=tk.LEFT, padx=2)
            self.palette_buttons[color_code] = btn

    def select_color(self, color_code):
        self.selected_color = color_code
        for c, btn in self.palette_buttons.items():
            # Remarcar visualmente el color seleccionado
            btn.config(relief="sunken" if c == color_code else "raised", 
                       bd=3 if c == color_code else 1)

    def change_color(self, r, c):
        # Pintar el cuadro de la cruz con el color seleccionado
        self.buttons[(r, c)]['color'] = self.selected_color
        self.buttons[(r, c)]['widget'].configure(bg=COLORS[self.selected_color], activebackground=COLORS[self.selected_color])

    def solve(self):
        # Convertir la interfaz visual a la matriz 9x12
        matriz = []
        for r in range(9):
            fila = []
            for c in range(12):
                if self.is_valid_cell(r, c):
                    fila.append(self.buttons[(r, c)]['color'])
                else:
                    fila.append("")
            matriz.append(fila)
            
        self.result_lbl.config(text="Buscando solución... (Por favor espera, explorar el cubo puede tardar).", fg="black")
        self.solve_btn.config(state=tk.DISABLED)
        self.shuffle_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.root.update()
        
        # Ejecutar en hilo separado para no congelar la ventana
        import threading
        threading.Thread(target=self._run_bfs, args=(matriz,), daemon=True).start()

    def _update_progress(self, current, total):
        self.progress_var.set((current / total) * 100)
        self.root.update_idletasks()

    def _run_bfs(self, matriz):
        try:
            def prog_cb(curr, tot):
                self.root.after(0, self._update_progress, curr, tot)
                
            path = rbk.bfs(matriz, progress_callback=prog_cb)
            # Volver al hilo principal para actualizar UI
            self.root.after(0, self._on_bfs_done, path, matriz)
        except Exception as e:
            self.root.after(0, self._on_bfs_error, str(e))

    def _on_bfs_done(self, path, matriz):
        self.solve_btn.config(state=tk.NORMAL)
        self.shuffle_btn.config(state=tk.NORMAL)
        self.progress_var.set(100)
        if len(path) == 0:
            if rbk.es_estado_final(matriz):
                self.result_lbl.config(text="✅ ¡El cubo ya está resuelto!", fg="green")
            else:
                self.result_lbl.config(text="❌ No se encontró una solución (se alcanzó el límite de memoria).", fg="red")
        else:
            self.result_lbl.config(text=f"✅ Solución encontrada ({len(path)} movimientos):\n\n{' -> '.join(path)}", fg="green")

    def _on_bfs_error(self, error_msg):
        self.solve_btn.config(state=tk.NORMAL)
        self.shuffle_btn.config(state=tk.NORMAL)
        self.result_lbl.config(text=f"⚠️ Error al ejecutar BFS:\n{error_msg}", fg="red")

    def shuffle(self):
        matriz = copy.deepcopy(rbk.ESTADO_RESUELTO)
        movimientos = [
            'x1r', 'x2r', 'x3r', 'x1l', 'x2l', 'x3l',
            'y1u', 'y2u', 'y3u', 'y1d', 'y2d', 'y3d',
            'z1f', 'z2f', 'z3f', 'z1b', 'z2b', 'z3b'
        ]
        
        # Aplicar 20 movimientos aleatorios
        for _ in range(20):
            m = random.choice(movimientos)
            matriz = rbk.mover(m, matriz)
            
        # Actualizar la interfaz visual
        for r in range(9):
            for c in range(12):
                if self.is_valid_cell(r, c):
                    color = matriz[r][c]
                    self.buttons[(r, c)]['color'] = color
                    self.buttons[(r, c)]['widget'].configure(bg=COLORS[color], activebackground=COLORS[color])
                    
        self.result_lbl.config(text="Cubo mezclado con 20 movimientos aleatorios.", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = RubikApp(root)
    root.mainloop()
