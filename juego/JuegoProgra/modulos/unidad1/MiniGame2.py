import pygame
import sys
import random        
from config import *
from modulos.MiniGames import MiniGames

class MiniGame2:
    def __init__(self, game):
        self.game = game
        self.button_clicked = False
        self.button_hovered = False
        self.button_color = (0, 128, 0)  
        self.transparent_color = (0, 128, 0, 128)
        self.waiting = False
        self.vidas = 3
        self.success = 0
        self.button_font = pygame.font.Font(None, 36)
        self.click_lock = False  # Variable de bloqueo
        self.click_lock_duration = 0.5
        self.number_types = ["Byte", "Float", "Short","Double"]

    def start_game(self):
        self.crea_problemas()
        self.play_game()  

    def play_game(self):
        while self.vidas > 0 and self.success < 10:
            for event in pygame.event.get():
                self.eventQuit(event)
                self.eventListenerUp(event)   
                if event.type == pygame.USEREVENT:
                    self.click_lock = False  # Desactivar el bloqueo cuando expire el temporizador              
            self.draw_botones()   
            self.draw_problemas(self.success)
            MiniGames.draw_lives(self)
            pygame.display.update() 

    def eventQuit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
                                        
    def eventListenerUp(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for index, rect in enumerate(self.button_rects):
                    if rect.collidepoint(event.pos):
                        problema = self.resultados[self.success]
                        _, _, _, _, clasificacion = problema
                        self.corrige(index, clasificacion)  

    def crea_problemas(self):
        self.numeros_generados = [self.genera_numeros() for _ in range(20)]
        self.grupos_numeros = [self.numeros_generados[i:i + 2] for i in range(0, len(self.numeros_generados), 2)]
        self.operadores = ["+", "-", "*", "/"]
        self.resultados = []
        
        for grupo in self.grupos_numeros:
            num1, num2 = grupo
            operador = random.choice(self.operadores)
            # Realiza la operación
            if operador == "+":
                resultado = num1 + num2
            elif operador == "-":
                resultado = num1 - num2
            elif operador == "*":
                resultado = num1 * num2
            elif operador == "/":
                resultado = num1 / num2  # Asegúrate de manejar la división por cero si es posible

            if int(resultado) == resultado:
                if -128 <= resultado <= 127:
                    clasificacion = "Byte"
                else:
                    clasificacion = "Short"
            else:
                epsilon = sys.float_info.epsilon
                if abs(resultado - round(resultado, 4)) <= epsilon:
                    clasificacion = "Float"
                else:
                    clasificacion = "Double"            
            self.resultados.append((num1, operador, num2, resultado, clasificacion))
        
    def genera_numeros(self):
        self.variables = random.uniform(1,150)
        if random.random() <= 0.2:
            self.variables = round(self.variables,2)
        else:
            self.variables = int(self.variables)
        return self.variables  

    def draw_problemas(self, problema_index):
        button_width = panel_width *5/8 // len(self.number_types)
        if 0 <= problema_index < len(self.resultados):
            problema = self.resultados[problema_index]
            num1, operador, num2, resultado, _ = problema

            # Definir la posición del cuadro
            x_pos = panel_x + panel_width * 0.2
            y_pos = panel_y + panel_height * 0.24
            MiniGames.pinta(x_pos, y_pos, f"{resultado}\n", 0)
            x_pos =  panel_x + panel_width * 0.35
            y_pos = panel_y + panel_height * 0.23
            MiniGames.pinta(x_pos, y_pos, f"=", 1)
            x_pos =  panel_x + panel_width * 0.38
            MiniGames.pinta(x_pos, y_pos, f"(", 1)
            x_pos =  panel_x + panel_width * 0.52
            MiniGames.pinta(x_pos, y_pos, f")", 1)
            x_pos =  panel_x + panel_width * 0.54
            MiniGames.pinta(x_pos, y_pos, f"(", 1)
            x_pos =  panel_x + panel_width * 0.58
            MiniGames.pinta(x_pos, y_pos, f"{num1}", 1)
            x_pos =  panel_x + panel_width * 0.65
            MiniGames.pinta(x_pos, y_pos, f"{operador}", 1)     
            x_pos =  panel_x + panel_width * 0.69
            MiniGames.pinta(x_pos, y_pos, f"{num2}", 1)
            x_pos =  panel_x + panel_width * 0.76
            MiniGames.pinta(x_pos, y_pos, f")", 1)
            
            
            self.espacio_rect = pygame.Rect(panel_x + panel_width * 0.43, panel_y + panel_height * 0.24, 150, 30)
            pygame.draw.rect(screen, self.button_color, self.espacio_rect, 2)

    def draw_botones(self):
        # Define una lista de colores para los botones
        button_colors = [(211, 70, 40), (57, 176, 72), (0, 0, 255), (147, 50, 164)]  # Ejemplos de colores diferentes

        # Calcula el ancho de un botón y el espacio entre ellos
        button_width = panel_width * 5 / 8 // len(self.number_types)
        button_spacing = button_width * 0.15

        # Calcula la posición inicial en la parte inferior del panel
        start_x = panel_x * 2.2
        start_y = panel_y + panel_height - panel_height * 0.4  # Altura del botón

        self.button_rects = []
        
        for index, tipo in enumerate(self.number_types):
            # Crea un rectángulo para el botón
            button_rect = pygame.Rect(start_x, start_y, button_width, panel_height * 0.2)

            # Calcula el rectángulo de sombra detrás del botón
            shadow_rect = button_rect.copy()
            shadow_rect.move_ip(5, 5)  # Ajusta las coordenadas para la sombra
            
            # Define el color del botón y el color de la sombra
            button_color = button_colors[index]
            shadow_color = (100, 100, 100)  # Color de la sombra (puedes ajustar el color según tus preferencias)
    
    
            # Modifica el color cuando se hace hover
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_color = (min(button_color[0] + 20, 255), min(button_color[1] + 20, 255), min(button_color[2] + 20, 255))

            # Dibuja la sombra detrás del botón
            pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=10)
    
            # Dibuja el botón con el color asignado
            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

            # Dibuja el texto en el botón
            button_text = self.button_font.render(tipo, True, text_color)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)

            # Actualiza la posición para el próximo botón
            start_x += button_width + button_spacing
            self.button_rects.append(button_rect)

        pygame.display.update()

    def corrige(self, index, clasificacion):      
        if index == 0 and clasificacion == "Byte":
            self.success+=1
            MiniGames.pinta_panel(self)
        elif index == 1 and clasificacion == "Float":
            self.success+=1
            MiniGames.pinta_panel(self)
        elif index == 2 and clasificacion == "Short":
            self.success+=1
            MiniGames.pinta_panel(self)
        elif index == 3 and clasificacion == "Double":
            self.success+=1
            MiniGames.pinta_panel(self)
        else:
            self.vidas-=1
            MiniGames.pinta_panel(self) 
            if self.vidas == 0:
                pygame.time.delay(1000)
                MiniGames.end(self, False)
        if self.success >=10 :
            pygame.time.delay(1000)
            MiniGames.end(self, True)