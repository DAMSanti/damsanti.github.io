import subprocess
import pygame
from pygame.locals import *
import sys
import random        
from config import *
from modulos.MiniGames import MiniGames

class MiniGame4:
    def __init__(self, game):
        self.game = game
        self.button_clicked = False
        self.button_hovered = False
        self.waiting = False
        self.vidas = 3
        self.success = 0
        self.click_lock = False  # Variable de bloqueo
        self.click_lock_duration = 0.5
        self.transparent_color = (0, 128, 0, 128)
        self.input_rect = pygame.Rect(panel_x + panel_width * 0.58, panel_y + panel_height * 0.24, 50, 30)
        self.color_inactive = (0, 128, 0)  
        self.color_active = (0, 128, 128)  
        self.color = self.color_inactive
        self.button_font = pygame.font.Font(None, 36)
        self.input_text = ""
        self.active = False

    def start_game(self):
        self.crea_problemas()
        self.play_game()

    def play_game(self):
        while self.vidas > 0 and self.success < 7:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            self.combinar_y_ejecutar_codigo_java(self.input_text, self.success)
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            if len(self.input_text) < 3:
                                self.input_text += event.unicode
            MiniGames.pinta_panel(self)
            self.draw_problemas(self.success)
            self.recopilar_texto_usuario()
            pygame.display.flip()                              
            MiniGames.draw_lives(self)

    def crea_problemas(self):
        self.numeros_generados = [self.genera_numeros() for _ in range(20)]
        self.grupos_numeros = [self.numeros_generados[i:i + 2] for i in range(0, len(self.numeros_generados), 2)]
        self.operadores = ["+", "-", "*", "/", "%"]
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
            elif operador == "%":
                resultado = num1 % num2
       
            self.resultados.append((num1, operador, num2, resultado))        

    def genera_numeros(self):
        self.variables = random.uniform(1,150)
        if random.random() <= 0.2:
            self.variables = round(self.variables,2)
        else:
            self.variables = int(self.variables)
        return self.variables  
    
    def recopilar_texto_usuario(self):
        # Puedes usar las funciones de pygame para obtener el texto ingresado por el usuario en las áreas de entrada de texto.
        txt_surface = game_font.render(self.input_text, True, self.color)
        width = max(50, txt_surface.get_width()+10)
        self.input_rect.w = width

        # Renderiza las áreas de entrada de texto
        screen.blit(txt_surface, (self.input_rect.x+5, self.input_rect.y+5))
        pygame.draw.rect(screen, self.color, self.input_rect, 2)
        
        

    def combinar_y_ejecutar_codigo_java(self, texto_usuario1, problema_index):
        # Combina el texto del usuario con un programa Java en un formato válido.
        problema = self.resultados[problema_index]
        num1, operador, num2, resultado = problema
        codigo_java = f"""
public class MiClase {{
    public static void main(String[] args) {{
        double num1 = {num1};
        double num2 = {num2};
        double resultado = {resultado};

        double res = num1 {texto_usuario1} num2;
        System.out.println(res);
    }}
}}
"""
        # Guarda el código Java en un archivo temporal
        with open("MiClase.java", "w") as archivo_java:
            archivo_java.write(codigo_java)

        # Compila y ejecuta el código Java
        subprocess.run(["javac", "MiClase.java"])  # Compilar el código
        output = subprocess.run(["java", "MiClase"], stdout=subprocess.PIPE, text=True)  # Ejecutar el código

        print(output.stdout)  # Muestra la salida del código Java
        java_output = output.stdout
        
        # Parse the value from the Java output
        try:
            parsed_value = float(java_output)  # Assuming the output format is "Tu solucion <value>"
            print(f"Parsed value: {parsed_value}", resultado)
            if parsed_value == resultado:
                print("Acertaste!!")

            # Now you can use parsed_value in your Python code for further processing
        except (IndexError, ValueError):
            print("Error parsing the value from Java output")

        return parsed_value  # You can return the value if needed
        
    def draw_problemas(self, problema_index):
        if 0 <= problema_index < len(self.resultados):
            problema = self.resultados[problema_index]
            num1, operador, num2, resultado = problema

            # Definir la posición del cuadro
            x_pos = panel_x + panel_width * 0.25
            y_pos = panel_y + panel_height * 0.205

            # Crear una fuente con un tamaño máximo
            max_font_size = 30  # Tamaño de fuente máximo en píxeles
            font = pygame.font.Font(None, max_font_size)

            # Combinar "resultado" y "clasificación" en dos líneas de texto
            resultado_text = font.render(f"{resultado}", True, text_color)
            ancho_resultado, alto_resultado = resultado_text.get_size()

            cuadro_width = 200  # Tamaño del cuadro en píxeles
            cuadro_height = 100
            cuadro_transparente = pygame.Surface((cuadro_width, cuadro_height), pygame.SRCALPHA)
            
            # Dibuja el cuadro con espacio para dos líneas de texto
            cuadro_rect = pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(cuadro_transparente, self.transparent_color, cuadro_rect, 0)
            
            # Redimensionar la fuente para ajustar el texto al cuadro
            while ancho_resultado > cuadro_width - 30 or alto_resultado > cuadro_height:
                max_font_size -= 1
                font = pygame.font.Font(None, max_font_size)
                resultado_text = font.render(f"{resultado}", True, (255, 255, 255))
                ancho_resultado, alto_resultado = resultado_text.get_size()

            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = cuadro_rect.centerx - resultado_text.get_width() // 2
            y_centered = cuadro_rect.centery - resultado_text.get_height() // 2
            resultado_text_rect = resultado_text.get_rect(topleft=(x_centered, y_centered))

            screen.blit(resultado_text, resultado_text_rect)
            
            # Dibujar el cuadro para el operador
            x_pos =  panel_x + panel_width * 0.35
            y_pos = panel_y + panel_height * 0.23

            igual_text = self.button_font.render(f"=", True, text_color)
            igual_rect =  pygame.Rect(x_pos, y_pos, panel_width * 0.05, cuadro_height*0.5)
            pygame.draw.rect(cuadro_transparente, self.transparent_color, igual_rect, 0)
            
            # Calcula las posiciones centradas para el texto
            x_centered = igual_rect.centerx - igual_text.get_width() // 2
            y_centered = igual_rect.centery - igual_text.get_height() // 2
            igual_text_rect = igual_text.get_rect(topleft=(x_centered, y_centered))
            
            screen.blit(igual_text, igual_text_rect)

            # Dibujar el cuadro para num1
            x_pos =  panel_x + panel_width * 0.45
            y_pos = panel_y + panel_height * 0.205

            num1_text = self.button_font.render(f"{num1}", True, text_color)
            num1_rect = pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(cuadro_transparente, self.transparent_color, num1_rect, 0)
            
            # Calcula las posiciones centradas parael texto
            x_centered = num1_rect.centerx - num1_text.get_width() // 2
            y_centered = num1_rect.centery - num1_text.get_height() // 2
            num1_text_rect = num1_text.get_rect(topleft=(x_centered, y_centered))
                        
            screen.blit(num1_text, num1_text_rect)

            # Dibujar el cuadro para num2
            x_pos = panel_x + panel_width * 0.65
            y_pos = panel_y + panel_height * 0.205

            num2_text = self.button_font.render(f"{num2}", True, text_color)
            num2_rect = pygame.Rect(x_pos, y_pos, panel_width * 0.12, cuadro_height)
            pygame.draw.rect(cuadro_transparente, self.transparent_color, num2_rect, 0)
            
            # Calcula las posiciones centradas para las dos líneas de texto
            x_centered = num2_rect.centerx - num2_text.get_width() // 2
            y_centered = num2_rect.centery - num2_text.get_height() // 2
            num2_text_rect = num2_text.get_rect(topleft=(x_centered, y_centered))
            
            
            screen.blit(num2_text, num2_text_rect)