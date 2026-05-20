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
    matriz[5][11], matriz[4][11], matriz[3][11] = matriz[6][3], matriz[7][3], matriz[8][3]
    matriz[6][3], matriz[7][3], matriz[8][3] = matriz[3][3], matriz[4][3], matriz[5][3]
    matriz[3][3], matriz[4][3], matriz[5][3] = u0, u1, u2

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

import kociemba

def to_kociemba(matriz):
    # En ESTADO_RESUELTO, los centros están en:
    # U: (1,4)
    # R: (4,7)
    # F: (4,4)
    # D: (7,4)
    # L: (4,1)
    # B: (4,10)
    
    # Validar que no haya cuadros vacíos
    centros = [
        matriz[1][4], matriz[4][7], matriz[4][4],
        matriz[7][4], matriz[4][1], matriz[4][10]
    ]
    if any(c == "" for c in centros):
        raise ValueError("El cubo tiene colores incompletos en los centros.")
        
    color_to_face = {
        matriz[1][4]: 'U',
        matriz[4][7]: 'R',
        matriz[4][4]: 'F',
        matriz[7][4]: 'D',
        matriz[4][1]: 'L',
        matriz[4][10]: 'B'
    }
    
    s = ""
    try:
        # U face (0..2, 3..5)
        for r in range(0, 3):
            for c in range(3, 6):
                s += color_to_face[matriz[r][c]]
        # R face (3..5, 6..8)
        for r in range(3, 6):
            for c in range(6, 9):
                s += color_to_face[matriz[r][c]]
        # F face (3..5, 3..5)
        for r in range(3, 6):
            for c in range(3, 6):
                s += color_to_face[matriz[r][c]]
        # D face (6..8, 3..5)
        for r in range(6, 9):
            for c in range(3, 6):
                s += color_to_face[matriz[r][c]]
        # L face (3..5, 0..2)
        for r in range(3, 6):
            for c in range(0, 3):
                s += color_to_face[matriz[r][c]]
        # B face (3..5, 9..11)
        for r in range(3, 6):
            for c in range(9, 12):
                s += color_to_face[matriz[r][c]]
    except KeyError:
        raise ValueError("Hay colores en las piezas que no coinciden con ningún centro.")
        
    return s

def mapear_movimientos_kociemba(koc_solution):
    # Kociemba devuelve algo como: "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    if not koc_solution.strip():
        return []
        
    moves = koc_solution.strip().split()
    path = []
    
    mapa_caras = {
        'R': 'x', 'L': 'x',
        'U': 'y', 'D': 'y',
        'F': 'z', 'B': 'z'
    }
    
    mapa_eje_cara = {
        'R': 'r', 'L': 'l',
        'U': 'u', 'D': 'd',
        'F': 'f', 'B': 'b'
    }
    
    for m in moves:
        cara = m[0]
        eje = mapa_caras[cara]
        sub = mapa_eje_cara[cara]
        
        turns = 1
        if len(m) > 1:
            if m[1] == '2':
                turns = 2
            elif m[1] == "'":
                turns = 3
                
        movimiento_final = f"{eje}{turns}{sub}"
        path.append(movimiento_final)
        
    return path

def resolver_cubo(estado_inicial, progress_callback=None):
    if es_estado_final(estado_inicial):
        if progress_callback: progress_callback(100, 100)
        return []
        
    if progress_callback:
        progress_callback(10, 100)
        
    s = to_kociemba(estado_inicial)
    
    if progress_callback:
        progress_callback(50, 100)
        
    try:
        # Resolvemos con kociemba
        koc_solution = kociemba.solve(s)
    except ValueError as e:
        raise ValueError("Estado del cubo inválido o irresoluble. Verifica los colores.")
        
    if progress_callback:
        progress_callback(90, 100)
        
    path = mapear_movimientos_kociemba(koc_solution)
    
    if progress_callback:
        progress_callback(100, 100)
        
    return path