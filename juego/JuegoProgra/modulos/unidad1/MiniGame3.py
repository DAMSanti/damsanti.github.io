import pygame
import sys
import random        
from config import *
from modulos.MiniGames import MiniGames

class MiniGame3:
    def __init__(self, game):
        self.game = game
        self.button_clicked = False
        self.button_hovered = False
        self.waiting = False
        self.vidas = 3
        self.success = 0
        self.click_lock = False  # Variable de bloqueo
        self.click_lock_duration = 0.5
        # Define el tamaño de la cuadrícula del laberinto
        self.GRID_SIZE = 10
        self.CELL_SIZE = panel_width * 0.3 // self.GRID_SIZE
        self.mov_types = ["/n", "/r", "/t","/b"]
        # Crea una cuadrícula para el laberinto
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.cuadro_x, self.cuadro_y = 0, 1  
        self.cuadro_size = panel_width * 0.3 // self.GRID_SIZE

    def start_game(self):
        self.genera_laberinto(1,1)
        self.play_game()

    def play_game(self):
        self.pinta_laberinto()
        self.pinta_cuadro()
        while self.vidas > 0 and self.success < 7:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for index, rect in enumerate(self.button_rects):
                            if rect.collidepoint(event.pos):
                                if index == 0:
                                    self.move_cuadro(0, 1)
                                elif index == 1:
                                    self.move_cuadro(0, -1)
                                elif index == 2:
                                    self.move_cuadro(1, 0)
                                elif index == 3:
                                    self.move_cuadro(-1, 0)        
            self.draw_botones()
            pygame.display.flip()                              
            MiniGames.draw_lives(self)
        
    def genera_laberinto(self, x, y):
        self.grid[y][x] = 1  # Marca la celda actual como parte del camino

        # Direcciones posibles en un orden aleatorio
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy  # Calcula la posición de la celda vecina

            if 0 <= nx < self.GRID_SIZE - 1 and 0 <= ny < self.GRID_SIZE and self.grid[ny][nx] == 0:
                # Elimina la pared entre la celda actual y la celda vecina
                self.grid[y + dy][x + dx] = 1
                self.genera_laberinto(nx, ny)
                
        # Marca la entrada y la salida
        self.grid[1][0] = 2
        self.grid[self.GRID_SIZE - 1][self.GRID_SIZE - 2] = 3
                         
    def pinta_laberinto(self):
        panel_laberinto_x = panel_x * 3.9
        panel_laberinto_y = panel_y * 2.2
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                cell_color = None
                if self.grid[y][x] == 1:
                    cell_color = (169, 169, 169)  # Pared
                elif self.grid[y][x] == 0:
                    cell_color = (139, 69, 19)  # Camino
                elif self.grid[y][x] == 2 or self.grid[y][x] == 3:
                    cell_color = (0, 0, 255)  # Entrada o salida

                if cell_color is not None:
                    rect = pygame.Rect(
                        panel_laberinto_x + x * self.CELL_SIZE, panel_laberinto_y + y * self.CELL_SIZE,
                        self.CELL_SIZE, self.CELL_SIZE
                    )
                    pygame.draw.rect(screen, cell_color, rect)
        pygame.display.update()
                  
    def draw_botones(self):
        # Define una lista de colores para los botones
        button_colors = [(211, 70, 40), (57, 176, 72), (0, 0, 255), (147, 50, 164)]  # Ejemplos de colores diferentes

        # Calcula el ancho de un botón y el espacio entre ellos
        button_width = panel_width * 5 / 8 // len(self.mov_types)
        button_spacing = button_width * 0.15

        # Calcula la posición inicial en la parte inferior del panel
        start_x = panel_x * 2.2
        start_y = panel_y + panel_height - panel_height * 0.3  # Altura del botón

        self.button_rects = []
        
        for index, tipo in enumerate(self.mov_types):
            # Crea un rectángulo para el botón
            button_rect = pygame.Rect(start_x, start_y, button_width, panel_height * 0.1)

            # Define el color del botón basado en la lista de colores
            button_color = button_colors[index]

            # Modifica el color cuando se hace hover
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_color = (min(button_color[0] + 20, 255), min(button_color[1] + 20, 255), min(button_color[2] + 20, 255))

            # Dibuja el botón con el color asignado
            pygame.draw.rect(screen, button_color, button_rect)

            # Dibuja el texto en el botón
            button_text = game_font.render(tipo, True, text_color)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)

            # Actualiza la posición para el próximo botón
            start_x += button_width + button_spacing
            self.button_rects.append(button_rect)

        pygame.display.update()

    def move_cuadro(self, dx, dy):
        new_x = self.cuadro_x + dx
        new_y = self.cuadro_y + dy

        if 0 <= new_x < len(self.grid[0]) and 0 <= new_y < len(self.grid):
            new_cell = self.grid[new_y][new_x]
            if new_cell in [1, 2, 3]:
                self.cuadro_x, self.cuadro_y = new_x, new_y
                if new_cell == 3:
                    pygame.time.delay(1000)
                    MiniGames.end(self, True)
        self.pinta_laberinto()
        self.pinta_cuadro()
                    
    def pinta_cuadro(self):
        x = panel_x * 3.9 + self.cuadro_x * self.CELL_SIZE
        y = panel_y * 2.2 + self.cuadro_y * self.CELL_SIZE
        pygame.draw.rect(screen, (255, 255, 255), (x, y, self.cuadro_size, self.cuadro_size))

