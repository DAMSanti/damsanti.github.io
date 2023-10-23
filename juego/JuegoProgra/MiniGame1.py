# player.py
import pygame
import sys
import random        
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class MiniGame1:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.panel_width = int(SCREEN_WIDTH * 0.8)
        self.panel_height = int(SCREEN_HEIGHT * 0.8)
        self.panel_x = (SCREEN_WIDTH - self.panel_width) // 2
        self.panel_y = (SCREEN_HEIGHT - self.panel_height) // 2
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
        self.background_image = pygame.image.load("pantalla.png")
        self.button_color = (0, 128, 0)
        self.hover_color = (0, 160, 0)
        self.clicked_color = (0, 100, 0)
        self.button_clicked = False
        self.button_hovered = False
        self.waiting = False
        self.vidas = 3
        self.button_font = pygame.font.Font(None, 36)
        self.click_lock = False  # Variable de bloqueo
        self.click_lock_duration = 0.5
        self.acertadas = []

        play_button_x = (self.panel_x + self.panel_width // 2) - (200 // 2)
        play_button_y = self.panel_y + self.panel_height - SCREEN_HEIGHT * 0.2
        self.button_rect = pygame.Rect(play_button_x, play_button_y, 200, 50)

        self.variable_types = ["byte", "short", "int", "long", "double", "float", "char"]
        self.variables = []
        self.values = []
        self.values_types = {
            3: "byte",
            27: "byte",
            54: "byte",
            -111: "byte",
            -4: "byte",
            25: "byte",
            19: "byte",
            92: "byte",
            -45: "byte",
            -99: "byte",
            312: "short",
            -1125: "short",
            2563: "short",
            1194: "short",
            -26325: "short",
            14215: "short",
            652: "short",
            -666: "short",
            -30000: "short",
            26854: "short",
            367549: "int",
            652365985: "int",
            '4x10^7': "int",
            '1 millon': "int",
            '9.99x10^8': "int",
            '80000/2': "int",
            555555 : "int",
            696969: "int",
            0.15: "float",
            3/4: "float",
            '3.451x10^2': "float",
            7/5: "float",
            2.287: "float",
            'π': "double",
            '√2': "double",
            'A': "char",
            'J': "char",
            '#': "char",
            '@': "char",
            'i': "char",
            'x': "char"
        }
        
        self.lives = 3
        self.success = 0
        
        dragging_variable = None  # Cuadro de tipo de variable que se está arrastrando
        dragging_offset = (0, 0)  # Desplazamiento de la posición del mouse al cuadro
  
    def handle_mouse_click(self):
        if not self.click_lock:
            # Procesar el clic
            self.click_lock = True  # Activar el bloqueo
            # Configurar un temporizador para desactivar el bloqueo después de un tiempo
            pygame.time.set_timer(pygame.USEREVENT, int(self.click_lock_duration * 1000))
         
    def clear_panel(self):
        self.pinta_panel()
        pygame.display.update()  
          
    def pinta_panel(self):
        image_width, image_height = self.background_image.get_size()
        scale_factor = min(self.panel_width / image_width, self.panel_height / image_height)
        scaled_width = int(image_width * scale_factor)
        scaled_height = int(image_height * scale_factor)
        x_offset = (self.panel_width - scaled_width) // 2 + self.panel_x
        y_offset = (self.panel_height - scaled_height) // 2 + self.panel_y

        scaled_background = pygame.transform.scale(self.background_image, (scaled_width, scaled_height))
        self.game.screen.blit(scaled_background, (x_offset, y_offset))
     
    def start(self):
        self.pinta_panel()
        self.display_description()
        pygame.display.update()
        self.waiting = True
        self.wait_for_play()

    def display_description(self):
        description = "Minijuego 1: \n\nAsigna los tipos de variables correctos a cada uno de los datos mostrados. \nDeberas introducir el tipo que mas se ajuste en cada caso."
        lines = description.split('\n')
        y = self.panel_height // 2 - len(lines) * self.font.get_linesize() // 2
        for line in lines:
            text = self.font.render(line, True, self.text_color)
            text_rect = text.get_rect(center=(self.panel_x + self.panel_width // 2, y))
            self.game.screen.blit(text, text_rect)
            y += self.font.get_linesize()
        pygame.display.update()

    def wait_for_play(self):
        waiting = True
        while waiting and self.game.minigame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if self.button_rect.collidepoint(event.pos):
                        self.button_hovered = True
                    else:
                        self.button_hovered = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.button_rect.collidepoint(event.pos):
                        self.handle_mouse_click()
                        self.button_clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.button_clicked = False
                        if self.button_rect.collidepoint(event.pos):
                            self.handle_mouse_click()
                            self.waiting = False
                            self.clear_panel()
                            self.start_game()
                if event.type == pygame.USEREVENT:
                    self.click_lock = False  # Desactivar el bloqueo cuando expire el temporizador
                    
            if self.button_clicked:
                button_color = self.clicked_color
                pygame.draw.rect(self.game.screen, button_color, self.button_rect)
                button_text = self.button_font.render("JUGAR!", True, self.text_color)
                button_text_rect = button_text.get_rect(center=self.button_rect.center)
                self.game.screen.blit(button_text, button_text_rect)
            elif self.button_hovered:
                button_color = self.hover_color
                pygame.draw.rect(self.game.screen, button_color, self.button_rect)
                button_text = self.button_font.render("JUGAR!", True, self.text_color)
                button_text_rect = button_text.get_rect(center=self.button_rect.center)
                self.game.screen.blit(button_text, button_text_rect)
            else:
                button_color = self.button_color
                pygame.draw.rect(self.game.screen, button_color, self.button_rect)
                button_text = self.button_font.render("JUGAR!", True, self.text_color)
                button_text_rect = button_text.get_rect(center=self.button_rect.center)
                self.game.screen.blit(button_text, button_text_rect)
            
            pygame.display.update()

    def start_game(self):
        self.variables = random.sample(self.variable_types, len(self.variable_types))
        values = list(self.values_types.keys())
        self.values = random.sample(values, len(self.variable_types))

        while self.variables == self.values:
            self.values = random.sample(self.variable_types, len(self.variable_types))

        pygame.display.update()
        self.play_game()

    def draw_variable(self, var_type, rect):
        cesta_image = pygame.image.load('cesta.png').convert_alpha()
        cesta_image = pygame.transform.scale(cesta_image, (rect.width, rect.height))
        self.game.screen.blit(cesta_image, rect)
        
        # Ajusta la posición vertical del texto
        text_x = rect.centerx
        text_y = rect.y + int(rect.height * 12/20)  # Coloca el texto a 3/4 de la altura de la imagen
        
        # Crea una superficie con el texto sombreado
        var_text = self.button_font.render(var_type, True, self.text_color)
        shadow_text = self.button_font.render(var_type, True, (0, 0, 0))  # Color de sombra

        # Ajusta la posición de la sombra
        shadow_x = text_x + 2  # Desplazamiento horizontal para la sombra
        shadow_y = text_y + 2  # Desplazamiento vertical para la sombra

        # Dibuja la sombra
        shadow_rect = shadow_text.get_rect(center=(shadow_x, shadow_y))
        self.game.screen.blit(shadow_text, shadow_rect)
    
        var_text = self.button_font.render(var_type, True, (255,255,255))
        text_rect = var_text.get_rect(center=(text_x, text_y))
        self.game.screen.blit(var_text, text_rect)

    def draw_value(self, val_type, rect, value_index):
        if value_index in self.acertadas:
                return  # No dibujar valores ya adivinados

        # Cargar la imagen "numeros.png" y escalarla al tamaño del rectángulo
        numeros_image = pygame.image.load("numeros.png").convert_alpha()
        numeros_image = pygame.transform.scale(numeros_image, (SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.08))
        self.game.screen.blit(numeros_image, rect)

        # Ajusta la posición vertical del texto
        text_x = rect.centerx + 15
        text_y = rect.y + int(rect.height * 3/4)  # Coloca el texto a 3/4 de la altura de la imagen
        
        # Crea una superficie con el texto sombreado
        val_text = self.button_font.render(str(val_type), True, self.text_color)
        shadow_text = self.button_font.render(str(val_type), True, (0, 0, 0))  # Color de sombra

        # Ajusta la posición de la sombra
        shadow_x = text_x + 2  # Desplazamiento horizontal para la sombra
        shadow_y = text_y + 2  # Desplazamiento vertical para la sombra

        # Dibuja la sombra
        shadow_rect = shadow_text.get_rect(center=(shadow_x, shadow_y))
        self.game.screen.blit(shadow_text, shadow_rect)
    
        val_text = self.button_font.render(str(val_type), True, self.text_color)
        text_rect = val_text.get_rect(center=(text_x, text_y))
        self.game.screen.blit(val_text, text_rect)


    def play_game(self):
        dragging_variable = None  # Declarar dragging_variable como local
        dragging_value_index = None  # Índice del valor que se está arrastrando
        while self.vidas > 0 and self.success < len(self.variable_types):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_click()
                        x, y = event.pos
                        clicked_rect = pygame.Rect(x, y, 1, 1)
                        for i, value in enumerate(self.values):
                            # print(i, value, self.values)
                            value_rect = pygame.Rect(self.panel_x + SCREEN_WIDTH * 0.13 + i * (SCREEN_WIDTH * 0.09) * 0.9 , self.panel_y + SCREEN_HEIGHT * 0.1, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.06)
                            # Si el cursor está sobre el cuadro de tipo de variable y no se está arrastrando uno ya
                            if clicked_rect.colliderect(value_rect) and dragging_variable is None:
                                dragging_variable = value
                                dragging_offset = (x - value_rect.x, y - value_rect.y)
                                dragging_value_index = i

                if event.type == pygame.MOUSEMOTION:
                    if dragging_variable is not None:
                        x, y = event.pos
                        # Limita la posición de la caja arrastrada para que no se acerque a menos de 200 píxeles del borde
                        x = max(self.panel_x + 300, min(self.panel_x + self.panel_width - 300, x))
                        y = max(self.panel_y + 150, min(self.panel_y + self.panel_height - 150, y))
                        value_rect = pygame.Rect(x - dragging_offset[0], y - dragging_offset[1], SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.06)
                        

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.handle_mouse_click()
                        if dragging_variable is not None:
                            for i, var_type in enumerate(self.variables):
                                var_rect = pygame.Rect((self.panel_x + SCREEN_WIDTH * 0.12) + i * (SCREEN_WIDTH * 0.09) * 0.88, self.panel_y + self.panel_height - SCREEN_HEIGHT * 0.26, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.15) 
                                if value_rect.colliderect(var_rect):                                        
                                    if dragging_variable in self.values_types:
                                        expected_type = self.values_types[dragging_variable]
                                        selected_type = self.variables[i]
                                    if expected_type == selected_type:
                                        self.success += 1
                                        # Agrega el índice del valor a la lista de aciertos
                                        self.acertadas.append(dragging_value_index)
                                        if self.success == len(self.variable_types):
                                            pygame.time.delay(1000)
                                            self.end(True)
                                    else:
                                        self.lives -= 1
                                        if self.lives == 0:
                                            pygame.time.delay(1000)
                                            self.end(False)

                            dragging_variable = None
                            dragging_value_index = None
                            
                if event.type == pygame.USEREVENT:
                    self.click_lock = False  # Desactivar el bloqueo cuando expire el temporizador
                             
                self.pinta_panel()
                self.draw_lives()
                
                # Dibuja los tipos de variables en la parte inferior de la pantalla
                var_x = self.panel_x + SCREEN_WIDTH * 0.12
                for var_type in self.variables:
                    var_rect = pygame.Rect(var_x, self.panel_y + self.panel_height - SCREEN_HEIGHT * 0.26, SCREEN_WIDTH * 0.09, SCREEN_HEIGHT * 0.15)
                    self.draw_variable(var_type, var_rect)
                    var_x += (SCREEN_WIDTH * 0.09) * 0.88

                # Dibuja los valores en la mitad superior de la pantalla
                val_x = self.panel_x + SCREEN_WIDTH * 0.13
                val_y = self.panel_y + SCREEN_HEIGHT * 0.1
                for i, val_type in enumerate(self.values):
                    if dragging_value_index is None or i != dragging_value_index:
                        val_rect = pygame.Rect(val_x, val_y, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.06)
                        self.draw_value(val_type, val_rect, i)
                    val_x += (SCREEN_WIDTH * 0.09) * 0.9          

                # Renderiza el cuadro de tipo de variable arrastrado
                if dragging_variable is not None:
                    dragged_value = self.values[dragging_value_index]
                    numeros_image = pygame.image.load("numeros.png").convert_alpha()
                    numeros_image = pygame.transform.scale(numeros_image, (SCREEN_WIDTH * 0.06, SCREEN_HEIGHT * 0.08))
                    self.game.screen.blit(numeros_image, value_rect)
                    
                    # Ajusta la posición vertical del texto
                    text_x = value_rect.centerx + 15
                    text_y = value_rect.y + int(value_rect.height * 3/4)  # Coloca el texto a 3/4 de la altura de la imagen

                    # Crea una superficie con el texto sombreado
                    shadow_text = self.button_font.render(str(dragged_value), True, (0, 0, 0))  # Color de sombra

                    # Ajusta la posición de la sombra
                    shadow_x = text_x + 2  # Desplazamiento horizontal para la sombra
                    shadow_y = text_y + 2  # Desplazamiento vertical para la sombra

                    # Dibuja la sombra
                    shadow_rect = shadow_text.get_rect(center=(shadow_x, shadow_y))
                    self.game.screen.blit(shadow_text, shadow_rect)

                    val_text = self.button_font.render(str(dragged_value), True, self.text_color)
                    text_rect = val_text.get_rect(center=(text_x, text_y))
                    self.game.screen.blit(val_text, text_rect)
                    


            pygame.display.update()

    def end(self, success):
        if success:
            self.game.borra_objects()
            self.game.minigame = None
            self.game.space_pressed = False
            self.player.pantalla += 1
            self.game.run()
        else:   
            self.game.vidas-=1       
            self.game.minigame = None
            self.game.space_pressed = False
            self.game.run()
           
    def draw_lives(self):
        for i in range(self.vidas):
            x = self.panel_x + self.panel_width - self.panel_width * 0.1 - (i * self.panel_width * 0.017)
            y = self.panel_y + self.panel_height * 0.04
            if i < self.lives:
                heart_image = pygame.image.load("corazon.png").convert_alpha()
            else:
                heart_image = pygame.image.load("corazonvacio.png").convert_alpha()
            heart_image = pygame.transform.scale(heart_image, (self.panel_width * 0.015, self.panel_width * 0.015))
            self.game.screen.blit(heart_image, (x, y))       
            
            
            
            