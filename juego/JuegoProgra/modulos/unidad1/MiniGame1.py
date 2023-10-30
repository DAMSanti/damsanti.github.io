# player.py
import pygame
import sys
import random       
from config import *
from modulos.MiniGames import MiniGames

class MiniGame1:
    def __init__(self, game):
        self.game = game
        self.vidas = 3
        self.acertadas = []
        self.variables = []
        self.values = []
        self.success = 0
        self.dragging_variable = None  # Cuadro de tipo de variable que se está arrastrando
        self.dragging_offset = (0, 0)  # Desplazamiento de la posición del mouse al cuadro
        self.dragging_value_index = None  # Índice del valor que se está arrastrando
        
    def start_game(self):
        self.minijuego = self
        self.variables = random.sample(variable_types, len(variable_types))
        values = list(values_types.keys())
        self.values = random.sample(values, len(variable_types))
        while self.variables == self.values:
            self.values = random.sample(variable_types, len(variable_types))
        pygame.display.update()
        self.play_game()

    def play_game(self):
        while self.vidas > 0 and self.success < len(variable_types):
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.click_lock = False  # Desactivar el bloqueo cuando expire el temporizador    
                self.eventQuit(event)
                self.eventListenerDown(event)
                self.eventListenerMove(event)
                self.eventListenerUp(event)
                MiniGames.pinta_panel(self)
                MiniGames.draw_lives(self)
                self.pintaValores()
                pygame.display.update()
                
    def eventQuit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
            
    def eventListenerDown(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                MiniGames.handle_mouse_click(self)
                x, y = event.pos
                clicked_rect = pygame.Rect(x, y, 1, 1)
                self.dragging_variable = None  # Inicializa la variable de arrastre como nula
                for i, value in enumerate(self.values):
                    value_rect = pygame.Rect(panel_x + SCREEN_WIDTH * 0.13 + i * (SCREEN_WIDTH * 0.09) * 0.9, panel_y + SCREEN_HEIGHT * 0.1, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.06)
                    if clicked_rect.colliderect(value_rect) and self.dragging_variable is None:
                        self.dragging_variable = value
                        self.dragging_offset = (x - value_rect.x, y - value_rect.y)
                        self.dragging_value_index = i  
                        self.value_rect = value_rect
                            
    def eventListenerMove(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.dragging_variable is not None:
                x, y = event.pos
                # Limita la posición de la caja arrastrada para que no se acerque a menos de 200 píxeles del borde
                x = max(panel_x + 300, min(panel_x + panel_width - 300, x))
                y = max(panel_y + 150, min(panel_y + panel_height - 150, y))
                # Actualiza la posición de self.value_rect en lugar de crear uno nuevo
                self.value_rect.x = x - self.dragging_offset[0]
                self.value_rect.y = y - self.dragging_offset[1]                         
                                               
    def eventListenerUp(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                MiniGames.handle_mouse_click(self)
                if self.dragging_variable is not None:
                    processed = False
                    for i, var_type in enumerate(self.variables):
                        var_rect = pygame.Rect((panel_x + SCREEN_WIDTH * 0.12) + i * (SCREEN_WIDTH * 0.09) * 0.88, panel_y + panel_height - SCREEN_HEIGHT * 0.23, SCREEN_WIDTH * 0.07, SCREEN_HEIGHT * 0.12)
                        if self.value_rect.colliderect(var_rect):
                            if not processed:
                                if self.dragging_variable in values_types:
                                    expected_type = values_types[self.dragging_variable]
                                    selected_type = self.variables[i]
                                if expected_type == selected_type:
                                    self.success += 1
                                    # Agrega el índice del valor a la lista de aciertos
                                    self.acertadas.append(self.dragging_value_index)
                                    if self.success == len(variable_types):
                                        pygame.time.delay(1000)
                                        MiniGames.end(self, True)
                                else:
                                    self.vidas -= 1
                                    if self.vidas == 0:
                                        pygame.time.delay(1000)
                                        MiniGames.end(self, False)
                                processed = True
                    self.dragging_variable = None
                    self.dragging_value_index = None   

    def draw_variable(self, var_type, rect):
        cesta_image = pygame.image.load(ruta_cesta).convert_alpha()
        cesta_image = pygame.transform.scale(cesta_image, (rect.width, rect.height)) 
        screen.blit(cesta_image, rect)
        
        # Ajusta la posición vertical del texto
        text_x = rect.centerx
        text_y = rect.y + int(rect.height * 0.4)  # Coloca el texto a 3/4 de la altura de la imagen
        
        # Crea una superficie con el texto sombreado
        var_text = game_font.render(var_type, True, text_color)
        shadow_text = game_font.render(var_type, True, (0, 0, 0))  # Color de sombra

        # Ajusta la posición de la sombra
        shadow_x = text_x + 2  # Desplazamiento horizontal para la sombra
        shadow_y = text_y + 2  # Desplazamiento vertical para la sombra

        # Dibuja la sombra
        shadow_rect = shadow_text.get_rect(center=(shadow_x, shadow_y))
        screen.blit(shadow_text, shadow_rect)
    
        var_text = game_font.render(var_type, True, (255,255,255))
        text_rect = var_text.get_rect(center=(text_x, text_y))
        screen.blit(var_text, text_rect)

    def draw_value(self, val_type, rect, value_index):
        if value_index in self.acertadas:
                return  # No dibujar valores ya adivinados

        # Cargar la imagen "numeros.png" y escalarla al tamaño del rectángulo
        numeros_image = pygame.image.load(ruta_numeros).convert_alpha()
        numeros_image = pygame.transform.scale(numeros_image, (SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.08))
        screen.blit(numeros_image, rect)

        # Ajusta la posición vertical del texto
        text_x = rect.centerx + 15
        text_y = rect.y + int(rect.height * 3/4)  # Coloca el texto a 3/4 de la altura de la imagen
        
        # Crea una superficie con el texto sombreado
        val_text = game_font.render(str(val_type), True, text_color)
        shadow_text = game_font.render(str(val_type), True, (0, 0, 0))  # Color de sombra

        # Ajusta la posición de la sombra
        shadow_x = text_x + 2  # Desplazamiento horizontal para la sombra
        shadow_y = text_y + 2  # Desplazamiento vertical para la sombra

        # Dibuja la sombra
        shadow_rect = shadow_text.get_rect(center=(shadow_x, shadow_y))
        screen.blit(shadow_text, shadow_rect)
    
        val_text = game_font.render(str(val_type), True, text_color)
        text_rect = val_text.get_rect(center=(text_x, text_y))
        screen.blit(val_text, text_rect)
                    
    def pintaValores(self):
        # Dibuja los tipos de variables en la parte inferior de la pantalla
        var_x = panel_x + SCREEN_WIDTH * 0.12
        for var_type in self.variables:
            var_rect = pygame.Rect(var_x, panel_y + panel_height - SCREEN_HEIGHT * 0.23, SCREEN_WIDTH * 0.07, SCREEN_HEIGHT * 0.12)
            self.draw_variable(var_type, var_rect)
            var_x += (SCREEN_WIDTH * 0.09) * 0.88

        # Dibuja los valores en la mitad superior de la pantalla
        val_x = panel_x + SCREEN_WIDTH * 0.13
        val_y = panel_y + SCREEN_HEIGHT * 0.1
        for i, val_type in enumerate(self.values):
            if self.dragging_value_index is None or i != self.dragging_value_index:
                val_rect = pygame.Rect(val_x, val_y, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.06)
                self.draw_value(val_type, val_rect, i)
            val_x += (SCREEN_WIDTH * 0.09) * 0.9          

        # Renderiza el cuadro de tipo de variable arrastrado
        if self.dragging_variable is not None:
            dragged_value = self.values[self.dragging_value_index]
            numeros_image = pygame.image.load(ruta_numeros).convert_alpha()
            numeros_image = pygame.transform.scale(numeros_image, (SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.08))
            screen.blit(numeros_image, self.value_rect)
                    
            # Ajusta la posición vertical del texto
            text_x = self.value_rect.centerx + 15
            text_y = self.value_rect.y + int(self.value_rect.height * 3/4)  # Coloca el texto a 3/4 de la altura de la imagen

            # Crea una superficie con el texto sombreado
            shadow_text = game_font.render(str(dragged_value), True, (0, 0, 0))  # Color de sombra

            # Ajusta la posición de la sombra
            shadow_x = text_x + 2  # Desplazamiento horizontal para la sombra
            shadow_y = text_y + 2  # Desplazamiento vertical para la sombra

            # Dibuja la sombra
            shadow_rect = shadow_text.get_rect(center=(shadow_x, shadow_y))
            screen.blit(shadow_text, shadow_rect)

            val_text = game_font.render(str(dragged_value), True, text_color)
            text_rect = val_text.get_rect(center=(text_x, text_y))
            screen.blit(val_text, text_rect)

            
            
            