import pygame
import math
from queue import PriorityQueue

ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A* - Pathfinding")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)
TURQUESA = (64, 224, 208)
AMARILLO = (255, 255, 0)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA
    
    def es_abierto(self):
        return self.color == VERDE
    
    def es_cerrado(self):
        return self.color == ROJO
    
    def es_camino(self):
        return self.color == AMARILLO

    def restablecer(self):
        self.color = BLANCO

    def hacer_actual(self):
        self.color = AZUL

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA
    
    def hacer_abierto(self):
        self.color = VERDE
    
    def hacer_cerrado(self):
        self.color = ROJO
    
    def hacer_camino(self):
        self.color = AMARILLO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),  # Arriba-izquierda, arriba, arriba-derecha
            (0, -1),           (0, 1),   # Izquierda, derecha
            (1, -1),  (1, 0),  (1, 1)    # Abajo-izquierda, abajo, abajo-derecha
        ]
        
        for df, dc in direcciones:
            nueva_fila = self.fila + df
            nueva_col = self.col + dc
            
            if (0 <= nueva_fila < self.total_filas and 
                0 <= nueva_col < self.total_filas and 
                not grid[nueva_fila][nueva_col].es_pared()):
                self.vecinos.append(grid[nueva_fila][nueva_col])

def heuristica(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distancia_real(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
def reconstruir_camino(came_from, actual, dibujar_func):
    while actual in came_from:
        actual = came_from[actual]
        if not actual.es_inicio():
            actual.hacer_camino()
        dibujar_func()

def algoritmo_a_estrella(dibujar_func, grid, inicio, fin):
    contador = 0
    open_set = PriorityQueue()
    open_set.put((0, contador, inicio))
    came_from = {}
    
    # Inicializar costos
    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0
    
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())
    
    open_set_hash = {inicio}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        actual = open_set.get()[2]
        actual.hacer_actual()
        open_set_hash.remove(actual)
        
        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar_func)
            fin.hacer_fin()
            inicio.hacer_inicio()
            return True
        
        for vecino in actual.vecinos:
            # Calcular el costo real del movimiento
            temp_g_score = g_score[actual] + distancia_real(actual.get_pos(), vecino.get_pos())
            
            if temp_g_score < g_score[vecino]:
                came_from[vecino] = actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino.get_pos(), fin.get_pos())
                
                if vecino not in open_set_hash:
                    contador += 1
                    open_set.put((f_score[vecino], contador, vecino))
                    open_set_hash.add(vecino)
                    if not vecino.es_fin():
                        vecino.hacer_abierto()
        
        dibujar_func()
        
        if actual != inicio:
            actual.hacer_cerrado()
    
    return False

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

def main(ventana, ancho):
    FILAS = 11 # Aumentado para mejor visualización
    grid = crear_grid(FILAS, ancho)
    
    inicio = None
    fin = None
    
    corriendo = True
    
    print("Instrucciones:")
    print("- Click izquierdo: Colocar inicio (naranja), fin (morado), o paredes (negro)")
    print("- Click derecho: Borrar nodos")
    print("- Presiona ESPACIO para ejecutar el algoritmo A*")
    print("- Presiona C para limpiar la grid")

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                if fila < FILAS and col < FILAS:
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
                if fila < FILAS and col < FILAS:
                    nodo = grid[fila][col]
                    nodo.restablecer()
                    if nodo == inicio:
                        inicio = None
                    elif nodo == fin:
                        fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    # Actualizar vecinos para todos los nodos
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    
                    # Ejecutar algoritmo A*
                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), 
                                       grid, inicio, fin)

                if event.key == pygame.K_c:
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    main(VENTANA, ANCHO_VENTANA)
