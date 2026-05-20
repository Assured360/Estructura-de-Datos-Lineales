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

MAPA_TEXTO = {
    'x': {'r': 'Derecha', 'l': 'Izquierda'},
    'y': {'u': 'Arriba', 'd': 'Abajo'},
    'z': {'f': 'Frente', 'b': 'Atrás'}
}
DIR_TEXTO = {
    '1': 'Sentido Horario',
    '2': 'Doble giro (180°)',
    '3': 'Sentido Antihorario'
}

def traducir_movimiento(mov):
    if not mov or len(mov) < 3: return mov
    eje, giros, cara = mov[0], mov[1], mov[2]
    texto_cara = MAPA_TEXTO.get(eje, {}).get(cara, cara)
    texto_dir = DIR_TEXTO.get(giros, giros)
    return f"Cara {texto_cara} -> {texto_dir}"

class RubikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rubik Solver GUI - Motor BFS")
        self.root.configure(bg='#F0F0F0')
        self.root.state('zoomed') # Maximizar ventana
        
        self.buttons = {}
        self.selected_color = 'W' # Color seleccionado por defecto
        
        self.solucion_actual = []
        self.paso_actual = 0
        self.reproduciendo = False
        self.matriz_inicial = []
        
        self.palette_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.palette_frame.pack(pady=10)
        self.build_palette()
        
        self.grid_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.grid_frame.pack(padx=20, pady=10)
        
        self.build_grid()
        
        # Botones principales
        self.main_btns_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.main_btns_frame.pack(pady=5)
        
        self.solve_btn = tk.Button(self.main_btns_frame, text="Resolver Cubo", font=('Arial', 14, 'bold'), 
                                   bg='#4CAF50', fg='white', command=self.solve)
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        
        self.shuffle_btn = tk.Button(self.main_btns_frame, text="Mezclar Cubo", font=('Arial', 12, 'bold'), 
                                     bg='#FF9800', fg='white', command=self.shuffle)
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(self.main_btns_frame, text="Devolver a la Normalidad", font=('Arial', 12, 'bold'), 
                                     bg='#2196F3', fg='white', command=self.reset_cube)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Etiqueta de resultado ubicada debajo de los botones principales para que no se corte
        self.result_lbl = tk.Label(self.root, text="Ingresa el estado de tu cubo interactuando con los cuadros.\n(El algoritmo BFS ha sido activado exitosamente)", 
                                   font=('Arial', 12), bg='#F0F0F0', wraplength=450)
        self.result_lbl.pack(pady=5)
        
        # Controles de paso a paso (ocultos por defecto)
        self.controls_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.controls_frame.pack(pady=5)
        
        self.prev_btn = tk.Button(self.controls_frame, text="⏮ Anterior", font=('Arial', 12), command=self.paso_anterior)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_btn = tk.Button(self.controls_frame, text="▶️ Reproducir", font=('Arial', 12, 'bold'), bg='#9C27B0', fg='white', command=self.toggle_reproduccion)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(self.controls_frame, text="Siguiente ⏭", font=('Arial', 12), command=self.paso_siguiente)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.step_lbl = tk.Label(self.root, text="", font=('Arial', 14, 'bold'), bg='#F0F0F0', fg='#333333')
        self.step_lbl.pack(pady=5)
        
        # Botón para mostrar notación
        self.toggle_not_btn = tk.Button(self.root, text="Mostrar Notación Técnica", font=('Arial', 10), command=self.toggle_notacion)
        self.toggle_not_btn.pack(pady=5)
        
        self.notation_lbl = tk.Label(self.root, text="", font=('Arial', 10, 'italic'), bg='#F0F0F0', fg='#666666', wraplength=450)
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate', variable=self.progress_var)
        self.progress_bar.pack(pady=5)
        
        self.ocultar_controles()

    def ocultar_controles(self):
        self.controls_frame.pack_forget()
        self.step_lbl.pack_forget()
        self.toggle_not_btn.pack_forget()
        self.notation_lbl.pack_forget()
        self.reproduciendo = False

    def mostrar_controles(self):
        self.controls_frame.pack(before=self.progress_bar, pady=10)
        self.step_lbl.pack(before=self.progress_bar, pady=5)
        self.toggle_not_btn.pack(before=self.progress_bar, pady=5)
        self.toggle_not_btn.config(text="Mostrar Notación Técnica")
        self.notation_lbl.pack_forget() # Oculto por defecto
        
    def toggle_notacion(self):
        if self.notation_lbl.winfo_ismapped():
            self.notation_lbl.pack_forget()
            self.toggle_not_btn.config(text="Mostrar Notación Técnica")
        else:
            self.notation_lbl.pack(before=self.progress_bar, pady=5)
            self.toggle_not_btn.config(text="Ocultar Notación Técnica")

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
                    btn = tk.Button(self.grid_frame, width=3, height=1, bg=COLORS[val], 
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
            btn = tk.Button(self.palette_frame, width=3, height=1, bg=COLORS[color_code],
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
        self.ocultar_controles() # Al editar manualmente, cancelar solución activa
        # Pintar el cuadro de la cruz con el color seleccionado
        self.buttons[(r, c)]['color'] = self.selected_color
        self.buttons[(r, c)]['widget'].configure(bg=COLORS[self.selected_color], activebackground=COLORS[self.selected_color])

    def actualizar_cuadricula(self, matriz):
        for r in range(9):
            for c in range(12):
                if self.is_valid_cell(r, c):
                    color = matriz[r][c]
                    self.buttons[(r, c)]['color'] = color
                    self.buttons[(r, c)]['widget'].configure(bg=COLORS[color], activebackground=COLORS[color])

    def matriz_desde_botones(self):
        matriz = []
        for r in range(9):
            fila = []
            for c in range(12):
                if self.is_valid_cell(r, c):
                    fila.append(self.buttons[(r, c)]['color'])
                else:
                    fila.append("")
            matriz.append(fila)
        return matriz

    def solve(self):
        self.ocultar_controles()
        matriz = self.matriz_desde_botones()
            
        self.result_lbl.config(text="Buscando solución... (Por favor espera, explorar el cubo puede tardar).", fg="black")
        self.solve_btn.config(state=tk.DISABLED)
        self.shuffle_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.root.update()
        
        # Ejecutar en hilo separado para no congelar la ventana
        import threading
        threading.Thread(target=self._run_solver, args=(matriz,), daemon=True).start()

    def _update_progress(self, current, total):
        self.progress_var.set((current / total) * 100)
        self.root.update_idletasks()

    def _run_solver(self, matriz):
        try:
            def prog_cb(curr, tot):
                self.root.after(0, self._update_progress, curr, tot)
                
            path = rbk.resolver_cubo(matriz, progress_callback=prog_cb)
            # Volver al hilo principal para actualizar UI
            self.root.after(0, self._on_solver_done, path, matriz)
        except Exception as e:
            self.root.after(0, self._on_solver_error, str(e))

    def _on_solver_done(self, path, matriz):
        self.solve_btn.config(state=tk.NORMAL)
        self.shuffle_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)
        self.progress_var.set(100)
        
        if len(path) == 0:
            if rbk.es_estado_final(matriz):
                self.result_lbl.config(text="✅ ¡El cubo ya está resuelto!", fg="green")
            else:
                self.result_lbl.config(text="❌ No se encontró una solución (estado inválido).", fg="red")
        else:
            self.solucion_actual = path
            self.paso_actual = 0
            self.matriz_inicial = copy.deepcopy(matriz)
            
            self.result_lbl.config(text=f"✅ ¡Solución encontrada en {len(path)} movimientos!\nUsa los controles para ver el paso a paso.", fg="green")
            self.notation_lbl.config(text="Notación técnica: " + " -> ".join(path))
            self.mostrar_controles()
            self.actualizar_texto_paso()

    def _on_solver_error(self, error_msg):
        self.solve_btn.config(state=tk.NORMAL)
        self.shuffle_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)
        self.result_lbl.config(text=f"⚠️ Error al resolver:\n{error_msg}", fg="red")

    def shuffle(self):
        self.ocultar_controles()
        matriz = copy.deepcopy(rbk.ESTADO_RESUELTO)
        movimientos = [
            'x1r', 'x2r', 'x3r', 'x1l', 'x2l', 'x3l',
            'y1u', 'y2u', 'y3u', 'y1d', 'y2d', 'y3d',
            'z1f', 'z2f', 'z3f', 'z1b', 'z2b', 'z3b'
        ]
        
        # Aplicar 5 movimientos aleatorios
        for _ in range(5):
            m = random.choice(movimientos)
            matriz = rbk.mover(m, matriz)
            
        self.actualizar_cuadricula(matriz)
        self.result_lbl.config(text="Cubo mezclado con 5 movimientos aleatorios.", fg="black")

    def reset_cube(self):
        self.ocultar_controles()
        matriz = copy.deepcopy(rbk.ESTADO_RESUELTO)
        self.actualizar_cuadricula(matriz)
        self.result_lbl.config(text="Cubo devuelto a su estado resuelto (normalidad).", fg="black")
        self.progress_var.set(0)

    # Lógica de reproducción
    def actualizar_texto_paso(self):
        if self.paso_actual == 0:
            self.step_lbl.config(text="Estado Inicial")
        elif self.paso_actual > len(self.solucion_actual):
            self.step_lbl.config(text="¡Cubo Resuelto!")
        else:
            mov = self.solucion_actual[self.paso_actual - 1]
            desc = traducir_movimiento(mov)
            self.step_lbl.config(text=f"Paso {self.paso_actual}/{len(self.solucion_actual)}: {desc}")
            
        self.prev_btn.config(state=tk.NORMAL if self.paso_actual > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.paso_actual < len(self.solucion_actual) else tk.DISABLED)

    def calcular_estado_en_paso(self, paso):
        m = copy.deepcopy(self.matriz_inicial)
        for i in range(paso):
            m = rbk.mover(self.solucion_actual[i], m)
        return m

    def paso_siguiente(self):
        if self.paso_actual < len(self.solucion_actual):
            self.paso_actual += 1
            estado = self.calcular_estado_en_paso(self.paso_actual)
            self.actualizar_cuadricula(estado)
            self.actualizar_texto_paso()

    def paso_anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            estado = self.calcular_estado_en_paso(self.paso_actual)
            self.actualizar_cuadricula(estado)
            self.actualizar_texto_paso()

    def toggle_reproduccion(self):
        if self.reproduciendo:
            self.reproduciendo = False
            self.play_btn.config(text="▶️ Reproducir", bg='#9C27B0')
        else:
            if self.paso_actual >= len(self.solucion_actual):
                self.paso_actual = 0
                estado = self.calcular_estado_en_paso(0)
                self.actualizar_cuadricula(estado)
                self.actualizar_texto_paso()
            self.reproduciendo = True
            self.play_btn.config(text="⏸ Pausa", bg='#f44336')
            self._reproducir_step()

    def _reproducir_step(self):
        if not self.reproduciendo: return
        if self.paso_actual < len(self.solucion_actual):
            self.paso_siguiente()
            self.root.after(500, self._reproducir_step)
        else:
            self.reproduciendo = False
            self.play_btn.config(text="▶️ Reproducir", bg='#9C27B0')

if __name__ == "__main__":
    root = tk.Tk()
    app = RubikApp(root)
    root.mainloop()
