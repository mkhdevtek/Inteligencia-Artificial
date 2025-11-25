import pygame
import math

# Configuraciones iniciales
ANCHO_VENTANA = 400
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización A*")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
AZUL = (50, 50, 235)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
TURQUESA = (64, 224, 208)

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
        self.h = 0
        self.g = 0
        self.f = 0
        self.padre = None

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

    def hacer_camino(self):
        self.color = TURQUESA

    def to_string(self):
        return f"Posicion:{self.fila}-{self.col}, g:{self.g}, h:{self.h}, f:{self.f}"

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def set_font(self, ventana):
        pygame.font.init()
        if self.f is not None and self.g is not None and self.h is not None:
            f = int(self.f)
            g = int(self.g)
            h = int(self.h)
            fuente = pygame.font.SysFont("Arial", 12)
            txt_f = fuente.render(f"f:{f}", True, (0,0,0))
            txt_g = fuente.render(f"g:{g}", True, (0,0,0))
            txt_h = fuente.render(f"h:{h}", True, (0,0,0))

            ventana.blit(txt_f, (self.x + 15, self.y + 2))
            ventana.blit(txt_g, (self.x + 10, self.y + 18))
            ventana.blit(txt_h, (self.x + 10, self.y + 32))


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
    return (abs(x2 - x1) + abs(y2 - y1)) * G

def calcular_costo_movimiento(actual, vecino): 
    actual_x, actual_y = actual.get_pos()
    vecino_x, vecino_y = vecino.get_pos()

    dx = abs(vecino_x - actual_x)
    dy = abs(vecino_y - actual_y)

    # Movimiento diagonal
    if dx == 1 and dy == 1:
        return G_D
    # Movimiento horizontal o vertical
    else:
        return G

def calcula_vecinos(actual, grid, fin, lista_abierta, lista_cerrada):
    vecinos_actualizados = []
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
            
            # Ignorar paredes y nodos en lista cerrada
            if vecino.es_pared() or vecino in lista_cerrada:
                continue
            
            # Calcular nuevo g
            costo_movimiento = calcular_costo_movimiento(actual, vecino)
            nuevo_g = actual.get_g() + costo_movimiento
            
            # Si el vecino no está en lista abierta o encontramos un mejor camino
            if vecino not in lista_abierta:
                vecino.set_g(nuevo_g)
                vecino.set_h(calcula_h(vecino, fin))
                vecino.set_f(vecino.get_g() + vecino.get_h())
                vecino.set_padre(actual)
                lista_abierta.append(vecino)
                vecinos_actualizados.append(vecino)
                if not vecino.es_fin():
                    vecino.hacer_posible()
            elif nuevo_g < vecino.get_g():
                # Encontramos un mejor camino
                vecino.set_g(nuevo_g)
                vecino.set_f(vecino.get_g() + vecino.get_h())
                vecino.set_padre(actual)
                vecinos_actualizados.append(vecino)
    
    return vecinos_actualizados

def reconstruir_camino(nodo_fin, draw):
    camino = []
    actual = nodo_fin
    while actual.get_padre() is not None:
        actual = actual.get_padre()
        if not actual.es_inicio():
            actual.hacer_camino()
        camino.append(actual)
        draw()
    return camino

def astar(draw, inicio, fin, grid):
    # Listas abierta y cerrada
    lista_abierta = []
    lista_cerrada = []
    
    # Inicializar nodo inicial
    inicio.set_g(0)
    inicio.set_h(calcula_h(inicio, fin))
    inicio.set_f(inicio.get_g() + inicio.get_h())
    lista_abierta.append(inicio)
    
    while lista_abierta:
        # Ordenar lista abierta por f (menor a mayor)
        lista_abierta.sort(key=lambda nodo: nodo.get_f())
        
        # Tomar el nodo con menor f (primero de la lista)
        actual = lista_abierta.pop(0)
        
        # Agregar a lista cerrada
        lista_cerrada.append(actual)
        
        # Marcar como visitado (excepto inicio y fin)
        if not actual.es_inicio() and not actual.es_fin():
            actual.hacer_visitado()
        
        # ¿Llegamos al objetivo?
        if actual == fin:
            print("¡Camino encontrado!")
            reconstruir_camino(fin, draw)
            fin.hacer_fin()  # Restaurar color del nodo final
            return True
        
        # Explorar vecinos
        calcula_vecinos(actual, grid, fin, lista_abierta, lista_cerrada)
        
        # Actualizar visualización
        draw()
        
        # Pequeña pausa para visualizar el proceso
        #pygame.time.delay(50)
    
    print("No se encontró camino")
    return False

def main(ventana, ancho):
    FILAS = 11
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
                if event.key == pygame.K_SPACE and inicio and fin:
                    # Limpiar grid antes de ejecutar
                    for fila in grid:
                        for nodo in fila:
                            if not nodo.es_inicio() and not nodo.es_fin() and not nodo.es_pared():
                                nodo.restablecer()
                    
                    astar(lambda: dibujar(ventana, grid, FILAS, ancho), inicio, fin, grid)
                
                if event.key == pygame.K_c:  # Limpiar todo
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, ancho)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
