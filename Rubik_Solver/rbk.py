import copy
from collections import deque

ESTADO_RESUELTO = [
    ["", "", "", "W", "W", "W", "", "", "", "", "", ""],
    ["", "", "", "W", "W", "W", "", "", "", "", "", ""],
    ["", "", "", "W", "W", "W", "", "", "", "", "", ""],
    
    ["O", "O", "O", "G", "G", "G", "R", "R", "R", "B", "B", "B"],
    ["O", "O", "O", "G", "G", "G", "R", "R", "R", "B", "B", "B"],
    ["O", "O", "O", "G", "G", "G", "R", "R", "R", "B", "B", "B"],
    
    ["", "", "", "Y", "Y", "Y", "", "", "", "", "", ""],
    ["", "", "", "Y", "Y", "Y", "", "", "", "", "", ""],
    ["", "", "", "Y", "Y", "Y", "", "", "", "", "", ""]
]

def es_estado_final(cubo):
    return cubo == ESTADO_RESUELTO

def rotar_cara(matriz, r, c):
    # Transponer y reverse para rotar 90 grados horario una cara 3x3
    temp = [
        [matriz[r][c], matriz[r][c+1], matriz[r][c+2]],
        [matriz[r+1][c], matriz[r+1][c+1], matriz[r+1][c+2]],
        [matriz[r+2][c], matriz[r+2][c+1], matriz[r+2][c+2]]
    ]
    matriz[r][c] = temp[2][0]
    matriz[r][c+1] = temp[1][0]
    matriz[r][c+2] = temp[0][0]
    
    matriz[r+1][c] = temp[2][1]
    matriz[r+1][c+1] = temp[1][1]
    matriz[r+1][c+2] = temp[0][1]
    
    matriz[r+2][c] = temp[2][2]
    matriz[r+2][c+1] = temp[1][2]
    matriz[r+2][c+2] = temp[0][2]

def turn_U(matriz):
    rotar_cara(matriz, 0, 3)
    temp = [matriz[3][c] for c in range(0, 3)]
    matriz[3][0], matriz[3][1], matriz[3][2] = matriz[3][3], matriz[3][4], matriz[3][5]
    matriz[3][3], matriz[3][4], matriz[3][5] = matriz[3][6], matriz[3][7], matriz[3][8]
    matriz[3][6], matriz[3][7], matriz[3][8] = matriz[3][9], matriz[3][10], matriz[3][11]
    matriz[3][9], matriz[3][10], matriz[3][11] = temp[0], temp[1], temp[2]

def turn_D(matriz):
    rotar_cara(matriz, 6, 3)
    temp = [matriz[5][c] for c in range(0, 3)]
    matriz[5][0], matriz[5][1], matriz[5][2] = matriz[5][9], matriz[5][10], matriz[5][11]
    matriz[5][9], matriz[5][10], matriz[5][11] = matriz[5][6], matriz[5][7], matriz[5][8]
    matriz[5][6], matriz[5][7], matriz[5][8] = matriz[5][3], matriz[5][4], matriz[5][5]
    matriz[5][3], matriz[5][4], matriz[5][5] = temp[0], temp[1], temp[2]

def turn_L(matriz):
    rotar_cara(matriz, 3, 0)
    u0, u1, u2 = matriz[0][3], matriz[1][3], matriz[2][3]
    matriz[0][3], matriz[1][3], matriz[2][3] = matriz[5][11], matriz[4][11], matriz[3][11]
    matriz[5][11], matriz[4][11], matriz[3][11] = matriz[8][3], matriz[7][3], matriz[6][3]
    matriz[8][3], matriz[7][3], matriz[6][3] = matriz[5][3], matriz[4][3], matriz[3][3]
    matriz[5][3], matriz[4][3], matriz[3][3] = u0, u1, u2

def turn_R(matriz):
    rotar_cara(matriz, 3, 6)
    u0, u1, u2 = matriz[0][5], matriz[1][5], matriz[2][5]
    matriz[0][5], matriz[1][5], matriz[2][5] = matriz[3][5], matriz[4][5], matriz[5][5]
    matriz[3][5], matriz[4][5], matriz[5][5] = matriz[6][5], matriz[7][5], matriz[8][5]
    matriz[6][5], matriz[7][5], matriz[8][5] = matriz[5][9], matriz[4][9], matriz[3][9]
    matriz[5][9], matriz[4][9], matriz[3][9] = u0, u1, u2

def turn_F(matriz):
    rotar_cara(matriz, 3, 3)
    u0, u1, u2 = matriz[2][3], matriz[2][4], matriz[2][5]
    matriz[2][3], matriz[2][4], matriz[2][5] = matriz[5][2], matriz[4][2], matriz[3][2]
    matriz[5][2], matriz[4][2], matriz[3][2] = matriz[6][5], matriz[6][4], matriz[6][3]
    matriz[6][5], matriz[6][4], matriz[6][3] = matriz[3][6], matriz[4][6], matriz[5][6]
    matriz[3][6], matriz[4][6], matriz[5][6] = u0, u1, u2

def turn_B(matriz):
    rotar_cara(matriz, 3, 9)
    u0, u1, u2 = matriz[0][5], matriz[0][4], matriz[0][3]
    matriz[0][5], matriz[0][4], matriz[0][3] = matriz[5][8], matriz[4][8], matriz[3][8]
    matriz[5][8], matriz[4][8], matriz[3][8] = matriz[8][3], matriz[8][4], matriz[8][5]
    matriz[8][3], matriz[8][4], matriz[8][5] = matriz[3][0], matriz[4][0], matriz[5][0]
    matriz[3][0], matriz[4][0], matriz[5][0] = u0, u1, u2

def mover(m, cubo):
    nuevo_cubo = copy.deepcopy(cubo)
    
    if not m or len(m) < 3:
        return nuevo_cubo

    turns = int(m[1])
    face = m[2]
    
    for _ in range(turns):
        if face == 'r': turn_R(nuevo_cubo)
        elif face == 'l': turn_L(nuevo_cubo)
        elif face == 'u': turn_U(nuevo_cubo)
        elif face == 'd': turn_D(nuevo_cubo)
        elif face == 'f': turn_F(nuevo_cubo)
        elif face == 'b': turn_B(nuevo_cubo)

    return nuevo_cubo

class Nodo:
    def __init__(self, estado, padre=None, movimiento=None, costo=0):
        self.estado = estado
        self.padre = padre
        self.movimiento = movimiento
        self.costo = costo

def obtener_hijos(nodo_actual):
    hijos = []
    # Generamos todos los movimientos posibles para los 3 ejes (x, y, z)
    # Formato: [eje][cantidad de giros][cara]
    # x: r (right), l (left)
    # y: u (up), d (down)
    # z: f (front), b (back)
    movimientos_posibles = [
        'x1r', 'x2r', 'x3r', 'x1l', 'x2l', 'x3l',
        'y1u', 'y2u', 'y3u', 'y1d', 'y2d', 'y3d',
        'z1f', 'z2f', 'z3f', 'z1b', 'z2b', 'z3b'
    ]
    
    for m in movimientos_posibles:
        estado_hijo = mover(m, nodo_actual.estado)
        hijo = Nodo(estado=estado_hijo, padre=nodo_actual, movimiento=m, costo=nodo_actual.costo + 1)
        hijos.append((m, hijo))
        
    return hijos

def bfs(estado_inicial, progress_callback=None, max_nodos=150000):
    # NODO <- Guardar CUBO como nodo
    nodo_inicial = Nodo(estado_inicial)
    
    # Q <- creamos una estructura de datos de tipo QUEUE
    q = deque()
    
    # V <- crear un SET que sea la memoria de estados visitados (visitados = set())
    visitados = set()
    
    # Q, V <- agregar NODO a Q y CUBO a V
    q.append(nodo_inicial)
    
    # Convertimos la matriz a tupla de tuplas y luego sacamos su hash para optimizar memoria en el SET
    estado_tupla = tuple(tuple(fila) for fila in nodo_inicial.estado)
    visitados.add(hash(estado_tupla))
    
    nodo_ganador = None
    nodos_visitados = 0
    
    # Iterar mientras que Q tenga elementos:
    while q:
        # actual <- retirar el siguiente elemento de Q (nodo)
        actual = q.popleft()
        nodos_visitados += 1
        
        if progress_callback and nodos_visitados % 1000 == 0:
            progress_callback(nodos_visitados, max_nodos)
            
        if nodos_visitados >= max_nodos:
            break
        
        # validar si actual es el estado ganador -> break
        if es_estado_final(actual.estado):
            nodo_ganador = actual
            break
            
        # movimiento + hijos <- obtener los hijos de actual
        movimiento_y_hijos = obtener_hijos(actual)
        
        # Iteramos hijos en la variable hijo:
        for movimiento, hijo in movimiento_y_hijos:
            estado_hijo_tupla = tuple(tuple(fila) for fila in hijo.estado)
            estado_hash = hash(estado_hijo_tupla)
            
            # validar si hijo está en visitados:
            if estado_hash in visitados:
                # SI ESTÁ: SKIP
                continue
            else:
                # NO ESTÁ:
                # -> agregar hijo a Q
                q.append(hijo)
                # -> agregar hijo a V
                visitados.add(estado_hash)
                
    # Recuperar el PATH con actual
    path = []
    if nodo_ganador is not None:
        actual = nodo_ganador
        while actual.padre is not None:
            path.append(actual.movimiento)
            actual = actual.padre
        path.reverse()
        
    return path