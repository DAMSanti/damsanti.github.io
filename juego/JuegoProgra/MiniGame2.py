import pygame
import sys
import random        
from config import *
from MiniGames import MiniGames

class MiniGame2:
    def __init__(self, game):
        self.game = game
        self.button_clicked = False
        self.button_hovered = False
        self.button_color = (0, 128, 0)  
        self.waiting = False
        self.vidas = 3
        self.success = 0
        self.button_font = pygame.font.Font(None, 36)
        self.click_lock = False  # Variable de bloqueo
        self.click_lock_duration = 0.5
        self.number_types = ["Int", "Float", "Short","Double"]

    def start_game(self):
        self.crea_problemas() 
        self.play_game()  

    def play_game(self):
        while self.vidas > 0 and self.success < 7:
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
                if -32768 <= resultado <= 32767:
                    clasificacion = "Short"
                else:
                    clasificacion = "Int"
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
            num1, operador, num2, resultado, clasificacion = problema

            # Definir la posición del cuadro
            x_pos = panel_x + panel_width * 0.15
            y_pos = panel_y + panel_height * 0.2

            # Combinar "resultado" y "clasificación" en dos líneas de texto
            resultado_text = self.button_font.render(f"{resultado}", True, text_color)
            clasificacion_text = self.button_font.render(f"{clasificacion}", True, text_color)

            # Calcular la altura del cuadro para acomodar ambas líneas
            cuadro_height = panel_height *0.2

            # Dibuja el cuadro con espacio para dos líneas de texto
            cuadro_rect = pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(screen, self.button_color, cuadro_rect, 0)

            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = cuadro_rect.centerx - resultado_text.get_width() // 2
            y_centered = cuadro_rect.centery - resultado_text.get_height() // 2
            resultado_text_rect = resultado_text.get_rect(topleft=(x_centered, y_centered))

            y_offset = resultado_text.get_height() + 10
            x_centered = cuadro_rect.centerx - clasificacion_text.get_width() // 2
            clasificacion_text_rect = clasificacion_text.get_rect(topleft=(x_centered, y_pos + y_offset))

            screen.blit(resultado_text, resultado_text_rect)
            screen.blit(clasificacion_text, clasificacion_text_rect)
            
            # Dibujar el cuadro para el operador
            x_pos =  panel_x + panel_width * 0.3
            y_pos = panel_y + panel_height * 0.25

            igual_text = self.button_font.render(f"=", True, text_color)
            igual_rect =  pygame.Rect(x_pos, y_pos, panel_width * 0.05, cuadro_height*0.5)
            pygame.draw.rect(screen, (0, 0, 0), igual_rect, 0)
            
            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = igual_rect.centerx - igual_text.get_width() // 2
            y_centered = igual_rect.centery - igual_text.get_height() // 2
            igual_text_rect = igual_text.get_rect(topleft=(x_centered, y_centered))
            
            screen.blit(igual_text, igual_text_rect)

            # Dibujar el cuadro para el operador
            x_pos =  panel_x + panel_width * 0.37
            y_pos = panel_y + panel_height * 0.2

            espacio_text = self.button_font.render(f"", True, text_color)
            espacio_rect =  pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(screen, self.button_color, espacio_rect, 0)
            
            screen.blit(espacio_text, espacio_rect)


            # Dibujar el cuadro para num1
            x_pos =  panel_x + panel_width * 0.518
            y_pos = panel_y + panel_height * 0.2

            num1_text = self.button_font.render(f"{num1}", True, text_color)
            num1_rect = pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(screen, self.button_color, num1_rect, 0)
            
            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = num1_rect.centerx - num1_text.get_width() // 2
            y_centered = num1_rect.centery - num1_text.get_height() // 2
            num1_text_rect = num1_text.get_rect(topleft=(x_centered, y_centered))
                        
            screen.blit(num1_text, num1_text_rect)


            # Dibujar el cuadro para el operador
            x_pos =  panel_x + panel_width * 0.66
            y_pos = panel_y + panel_height * 0.25

            operador_text = self.button_font.render(f"{operador}", True, text_color)
            operador_rect =  pygame.Rect(x_pos, y_pos, panel_width * 0.05, cuadro_height*0.5)
            pygame.draw.rect(screen, (0, 0, 0), operador_rect, 0)
            
            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = operador_rect.centerx - operador_text.get_width() // 2
            y_centered = operador_rect.centery - operador_text.get_height() // 2
            operador_text_rect = operador_text.get_rect(topleft=(x_centered, y_centered))
            
            screen.blit(operador_text, operador_text_rect)

            # Dibujar el cuadro para num2
            x_pos = panel_x + panel_width * 0.73
            y_pos = panel_y + panel_height * 0.2

            num2_text = self.button_font.render(f"{num2}", True, text_color)
            num2_rect = pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(screen, self.button_color, num2_rect, 0)
            
            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = num2_rect.centerx - num2_text.get_width() // 2
            y_centered = num2_rect.centery - num2_text.get_height() // 2
            num2_text_rect = num2_text.get_rect(topleft=(x_centered, y_centered))
            
            
            screen.blit(num2_text, num2_text_rect)

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

            # Define el color del botón basado en la lista de colores
            button_color = button_colors[index]

            # Modifica el color cuando se hace hover
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_color = (min(button_color[0] + 20, 255), min(button_color[1] + 20, 255), min(button_color[2] + 20, 255))

            # Dibuja el botón con el color asignado
            pygame.draw.rect(screen, button_color, button_rect)

            # Dibuja el texto en el botón
            button_text = self.button_font.render(tipo, True, text_color)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)

            # Actualiza la posición para el próximo botón
            start_x += button_width + button_spacing
            self.button_rects.append(button_rect)

        pygame.display.update()

    def corrige(self, index, clasificacion):      
        if index == 0 and clasificacion == "Int":
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
            self.lives-=1
            self.pinta_panel() 
            if self.lives == 0:
                pygame.time.delay(1000)
                MiniGames.end(self, False)
        if self.success >=7 :
            pygame.time.delay(1000)
            MiniGames.end(self, True)