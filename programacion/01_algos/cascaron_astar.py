import pygame

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
AZUL = (50, 50, 235)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

# Pesos
G = 10
G_D = 14

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.h = 0
        self.g = 0
        self.f = 0
        self.padre = None

    def set_h(self, h):
        self.h = h

    def get_h(self):
        return self.h

    def set_g(self, g):
        self.g = g

    def get_g(self):
        return self.g

    def set_f(self, f):
        self.f = f

    def get_f(self):
        return self.f

    def get_padre(self):
        return self.padre
    
    def set_padre(self, celda):
        self.padre = celda

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def es_visitado(self):
        return self.color == GRIS

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_visitado(self):
        self.color = GRIS
    
    def hacer_actual(self):
        self.color = VERDE

    def hacer_posible(self):
        self.color = AZUL

    def to_string(self):
        return f"Posicion:{self.fila}-{self.col}, g:{self.g}, h:{self.h}, f:{self.f}"

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

# ALGORITMO A* -----------------------------------------------
def calcula_h(inicio, fin):
    x1, y1 = inicio.get_pos()
    x2, y2 = fin.get_pos()
    return max(abs(x2 - x1), abs(y2 - y1)) * G

def calcular_costo_movimiento(actual, vecino): 
    actual_x, actual_y = actual.get_pos()
    vecino_x, vecino_y = vecino.get_pos()

    dx = abs(vecino_x - actual_x) * G
    dy = abs(vecino_y - actual_y) * G

    if dx == G and dy == G:
        return G_D
    else:
        return G

def calcular_pesos_vecinos(actual, vecinos):
    pesos_vecinos = {}
    costo_g_actual = actual.get_g()

    for vecino in vecinos:
        costo_movimiento = calcular_costo_movimiento(actual, vecino)

        nuevo_g = costo_g_actual + costo_movimiento

        if vecino.get_g() is None or nuevo_g < vecino.get_g():
            pesos_vecinos[vecino] = nuevo_g
            vecino.set_padre(actual)

    return pesos_vecinos

def actualizar_vecino(vecino, actual, fin):
    costo_movimiento = calcular_costo_movimiento(actual, vecino)
    nuevo_g = actual.get_g() + costo_movimiento

    if vecino.get_g() == 0 or nuevo_g < vecino.get_g():
        vecino.set_g(nuevo_g)
        vecino.set_h(calcula_h(vecino, fin))
        vecino.set_f(vecino.get_g() + vecino.get_h())
        vecino.set_padre(actual)
        vecino.hacer_posible()

        return True

    return False

def calcula_vecinos(actual, grid, fin):
    lista_vecinos = []
    actual_x, actual_y = actual.get_pos()
    filas = len(grid)
    columnas = len(grid[0]) if filas > 0 else 0
    
    # Las 8 direcciones incluyendo diagonales
    direcciones = [
        (-1, -1), (-1, 0), (-1, 1),  # fila superior
        (0, -1),           (0, 1),   # fila actual (izq, der)
        (1, -1),  (1, 0),  (1, 1)    # fila inferior
    ]
    
    for dx, dy in direcciones:
        vecino_x = actual_x + dx
        vecino_y = actual_y + dy
        
        # Verificar límites
        if 0 <= vecino_x < filas and 0 <= vecino_y < columnas:
            vecino = grid[vecino_x][vecino_y]
            
            if vecino is not None and not vecino.es_pared() and not vecino.es_visitado():
                if actualizar_vecino(vecino, actual, fin):
                    #print("Vecino actualizado")
                    #print(f"Vecino: {vecino.get_pos()}: h={vecino.get_h()}, g={vecino.get_g()}, f={vecino.get_f()}")
                    lista_vecinos.append(vecino)
                    vecino.hacer_posible()
    
    return lista_vecinos

def ordena_peso(peso):
    return peso.get_f()

def astar(inicio, fin, grid):
    f = 0
    g = 0
    h = 0

    inicio.hacer_visitado()

    actual = inicio
    vecinos = calcula_vecinos(actual, grid, fin)
    vecinos.sort(key=ordena_peso)

    actual = vecinos.pop()
    while actual is not fin:
        vecinos = calcula_vecinos(actual, grid, fin)
        vecinos.sort(key=ordena_peso)

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    astar(inicio, fin, grid)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
