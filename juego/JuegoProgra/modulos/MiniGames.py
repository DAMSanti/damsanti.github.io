# player.py
import pygame
import sys
from config import *

class MiniGames:
    def __init__(self, game):
        self.game = game
        self.click_lock = False  # Variable de bloqueo
        self.button_color = (0, 128, 0)  
        self.button_clicked = False
        self.button_hovered = False
        self.waiting = False
        self.button_rect = pygame.Rect(play_button_x, play_button_y, 200, 50)
    
    def start(self, i):
        self.juego = i
        self.pinta_panel(self)
        self.display_description(self.juego)
        self.waiting = True
        self.wait_for_play()
    
    @staticmethod            
    def pinta_panel(self):
        image_width, image_height = panel_image.get_size()
        scale_factor = min(panel_width / image_width, panel_height / image_height)
        scaled_width = int(image_width * scale_factor)
        scaled_height = int(image_height * scale_factor)
        x_offset = (panel_width - scaled_width) // 2 + panel_x
        y_offset = (panel_height - scaled_height) // 2 + panel_y
        scaled_background = pygame.transform.scale(panel_image, (scaled_width, scaled_height))
        screen.blit(scaled_background, (x_offset, y_offset))
        
    def clear_panel(self):
        self.pinta_panel(self)
        pygame.display.update()  
     
    def display_description(self, i):
        lines = f"description_{i}"
        if lines in globals():
            description = globals()[lines]
            lines = description.split('\n')
        y = panel_height // 2 - len(lines) * game_font.get_linesize() // 2
        for line in lines:
            text = game_font.render(line, True, text_color)
            text_rect = text.get_rect(center=(panel_x + panel_width // 2, y))
            screen.blit(text, text_rect)
            y += game_font.get_linesize()

    def handle_mouse_click(self):
        if not self.click_lock:
            self.click_lock = True  # Activar el bloqueo
            pygame.time.set_timer(pygame.USEREVENT, int(click_lock_duration * 1000))
         
    def wait_for_play(self):
        waiting = True
        while waiting:
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
                            self.game.escogeJuego()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.handle_mouse_click()
                        self.waiting = False
                        self.clear_panel()
                        self.game.escogeJuego()
                if event.type == pygame.USEREVENT:
                    self.click_lock = False  # Desactivar el bloqueo cuando expire el temporizador
                    
            if self.button_clicked:
                button_color = clicked_color
            elif self.button_hovered:
                button_color = hover_color
            else:
                button_color = self.button_color
            self.pintaJugar(button_color)
            pygame.display.update()
            
    def pintaJugar(self, boton):
        pygame.draw.rect(screen, boton, self.button_rect, border_radius=10)
        button_text = game_font.render("JUGAR!", True, text_color)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        screen.blit(button_text, button_text_rect)
        
    def draw_lives(self):
        for i in range(max_vidas):
            x = panel_x + panel_width - panel_width * 0.15 - (i * panel_width * 0.017)
            y = panel_y + panel_height * 0.02
            if i < self.vidas:
                heart_image = pygame.image.load(ruta_corazonlleno).convert_alpha()
            else:
                heart_image = pygame.image.load(ruta_corazonvacio).convert_alpha()
            heart_image = pygame.transform.scale(heart_image, (panel_width * 0.015, panel_width * 0.015))
            screen.blit(heart_image, (x, y))   
            
    def end(self, success):
        if success:
            self.game.borra_objects()
            self.game.minigame = None
            self.game.space_pressed = False
            self.game.pantalla += 1
            self.game.run()
        else:   
            self.game.vidas-=1       
            self.game.minigame = None
            self.game.space_pressed = False
            self.game.run()   
            
    def pinta(x, y, texto, lineas, color=(47, 252, 2)):
        cuadro_width = 200  # Tamaño del cuadro en píxeles
        cuadro_height = 100
        cuadro_transparente = pygame.Surface((cuadro_width, cuadro_height), pygame.SRCALPHA)
        if lineas == 1 :
            igual_text = digi_font.render(texto, True, color)
            igual_rect =  pygame.Rect(x, y, panel_width * 0.05, cuadro_height*0.5)
            pygame.draw.rect(cuadro_transparente, transparent_color, igual_rect, 0)
                
            # Calcula las posiciones centradas para el texto
            y_centered = igual_rect.centery - igual_text.get_height() // 2
            igual_text_rect = igual_text.get_rect(topleft=(igual_rect.centerx, y_centered))
            igual_text2 = digi_font.render(texto, True, (0,0,0))
            igual_text_rect2 = igual_text.get_rect(topleft=(igual_rect.centerx+2, y_centered+2))
              
            screen.blit(igual_text2, igual_text_rect2)  
            screen.blit(igual_text, igual_text_rect)
        else:
            # Crear una fuente con un tamaño máximo
            max_font_size = 30  # Tamaño de fuente máximo en píxeles
            font = pygame.font.Font(fuente, max_font_size)

            # Combinar "Resultado Esperado" y "resultado" en una cadena con un carácter de retorno de línea
            texto_combinado = texto

            # Dividir la cadena en dos líneas
            lineas = texto_combinado.split("\n")
            linea1 = lineas[0]
            linea2 = lineas[1]

            # Renderizar las dos líneas de texto
            texto_linea1 = font.render(linea1, True, color)
            texto_linea2 = font.render(linea2, True, color)

            # Obtener el ancho y alto de ambas líneas
            ancho_linea1, alto_linea1 = texto_linea1.get_size()
            ancho_linea2, alto_linea2 = texto_linea2.get_size()

            # Dibuja el cuadro con espacio para dos líneas de texto
            cuadro_rect = pygame.Rect(x, y, panel_width * 0.12, max(alto_linea1, alto_linea2))
            pygame.draw.rect(cuadro_transparente, transparent_color, cuadro_rect, 0)

            # Calcula las posiciones centradas para ambas líneas de texto
            y_centered_linea1 = cuadro_rect.centery - alto_linea1 // 2
            y_centered_linea2 = y_centered_linea1 + alto_linea1 + 20  # 20 píxeles por debajo de la primera línea
            x_centered_linea1 = cuadro_rect.centerx - ancho_linea1 // 2
            x_centered_linea2 = cuadro_rect.centerx - ancho_linea2 // 2

            # Establecer las posiciones para ambas líneas de texto
            texto_linea1_rect = texto_linea1.get_rect(topleft=(x_centered_linea1, y_centered_linea1))
            texto_linea2_rect = texto_linea2.get_rect(topleft=(x_centered_linea2, y_centered_linea2))
            
            # Renderizar las dos líneas de texto
            texto_linea12 = font.render(linea1, True, (0,0,0))
            texto_linea22 = font.render(linea2, True, (0,0,0))
            
            texto_linea1_rect2 = texto_linea1.get_rect(topleft=(x_centered_linea1 + 2, y_centered_linea1 + 2))
            texto_linea2_rect2 = texto_linea2.get_rect(topleft=(x_centered_linea2 + 2, y_centered_linea2 + 2))

            screen.blit(texto_linea12, texto_linea1_rect2)
            screen.blit(texto_linea22, texto_linea2_rect2)
            
            # Pintar las dos líneas de texto en sus respectivas posiciones
            screen.blit(texto_linea1, texto_linea1_rect)
            screen.blit(texto_linea2, texto_linea2_rect)
            