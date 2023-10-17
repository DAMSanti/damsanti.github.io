# game.py
import pygame
import sys
import random
from player import Player
from escritorios import Escritorios


class Game:
    def __init__(self):
        pygame.init()
        # Definimos los objetos escritorio
        self.objects = []
        # Definimos el tamaño y titulo de la ventana
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Juego de Programación en Java")
        #  Inicializamos el reloj y algunas variables para el juego
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.background_x = 0
        self.background_speed = 0
        self.score = 0
        self.max_score = 0
        self.space_pressed = False # Variable para rastrear la bara espaciadora
        # Definimos la imagen de fondo
        self.background_image = pygame.image.load('fondo.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        # Creamos los objetos de clase player y minijuego1
        self.player = Player(self)
        self.minigame = None
 
    def borra_objects(self):
        self.objects = []
        
    def update_objects(self):
        for obj in self.objects:
            obj.update(self.background_speed * 2)
            if obj.rect.x < self.player.rect.x + self.player.width / 3:
                self.player.blocked = True
            if not obj.is_on_screen(self.screen_width):
                self.objects.remove(obj)
            obj.draw(self.screen)
        # Generar un nuevo objeto si es necesario
        if len(self.objects) == 0:
            self.create_new_object(self.screen_width, self.screen_height - 270)
            
    def create_new_object(self, x, y):
        image_path = 'escritorio.png'  # Ruta a la imagen del objeto
        new_object = Escritorios(x, y, image_path)
        self.objects.append(new_object)

    def interactua_object(self):     
        self.minigame = MiniGame1(self)       
        self.minigame.start()
        
    def pinta_pantalla(self):
        self.background_x -= self.background_speed
        if self.background_x < -self.background_image.get_width():
            self.background_x = 0
        self.screen.blit(self.background_image, (self.background_x, 0))
        self.screen.blit(self.background_image, (self.background_x + self.background_image.get_width(), 0))
        self.player.control_personaje()
        self.player.draw(self.screen)        
        
    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.blocked:
                        self.space_pressed = True  # Marcar la bara espaciadora
                        if self.minigame is None:
                            # Iniciar el minijuego correspondiente
                            self.interactua_object()  # Implementa esta función

            pygame.display.update()
            self.pinta_pantalla()
            self.update_objects()
            font = pygame.font.Font(None, 36)
            text = font.render(f"Distancia: {self.max_score}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            if self.player.blocked and not self.space_pressed:
                font = pygame.font.Font(None, 36)
                text = font.render("Pulsa la barra espaciadora", True, (255, 255, 255))
                self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - text.get_height() // 2))
            if self.space_pressed:
                self.space_pressed = False  # Restablecer la variable
                self.interactua_object()  # Abrir Minijuego
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
     
     
     
     
                












        

class MiniGame1:
    def __init__(self, game):
        self.game = game
        self.panel_width = int(1920 * 0.8)
        self.panel_height = int(1080 * 0.8)
        self.panel_x = (1920 - self.panel_width) // 2
        self.panel_y = (1080 - self.panel_height) // 2
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
        self.background_image = pygame.image.load("pantalla.png")
        self.button_color = (0, 128, 0)
        self.hover_color = (0, 160, 0)
        self.clicked_color = (0, 100, 0)
        self.button_clicked = False
        self.button_hovered = False
        self.waiting = False
        self.button_font = pygame.font.Font(None, 36)

        play_button_x = (self.panel_x + self.panel_width // 2) - (200 // 2)
        play_button_y = self.panel_y + self.panel_height - 300
        self.button_rect = pygame.Rect(play_button_x, play_button_y, 200, 50)

        self.variable_types = ["byte", "short", "int", "long", "double", "float", "char", "boolean"]
        self.values_types = [3, 2.287, True, 'A']
        self.variables = []
        self.values = []
        self.lives = 3
        self.success = 0
        
        dragging_variable = None  # Cuadro de tipo de variable que se está arrastrando
        dragging_offset = (0, 0)  # Desplazamiento de la posición del mouse al cuadro

        
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
        
        while self.waiting:
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
                        self.button_clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.button_clicked = False
                        if self.button_rect.collidepoint(event.pos):
                            self.clear_panel()
                            self.start_game()
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
        self.values = random.sample(self.values_types, len(self.values_types))

        while self.variables == self.values:
            self.values = random.sample(self.variable_types, len(self.variable_types))

        # Dibuja los tipos de variables en la parte inferior de la pantalla
        var_x = self.panel_x + 230
        for var_type in self.variables:
            var_rect = pygame.Rect(var_x, self.panel_y + self.panel_height - 250, 150, 150)
            self.draw_variable(var_type, var_rect)
            var_x += 140

        # Dibuja los valores en la mitad superior de la pantalla
        val_x = self.panel_x
        val_y = self.panel_y + 50
        for val_type in self.values:
            val_rect = pygame.Rect(val_x, val_y, 100, 50)
            self.draw_value(val_type, val_rect)
            val_x += 100

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

    def draw_value(self, val_type, rect):
        if isinstance(val_type, int):
            val_type_str = str(val_type)
        elif isinstance(val_type, float):
            val_type_str = f"{val_type:.3f}"
        elif isinstance(val_type, bool):
            val_type_str = "True" if val_type else "False"
        elif isinstance(val_type, str):
            val_type_str = f"'{val_type}'"

        pygame.draw.rect(self.game.screen, (255, 0, 0), rect)
        val_text = self.button_font.render(str(val_type_str), True, self.text_color)
        val_text_rect = val_text.get_rect(center=rect.center)
        self.game.screen.blit(val_text, val_text_rect)

    def play_game(self):
        dragging_variable = None  # Declarar dragging_variable como local
        while self.lives > 0 and self.success < len(self.variable_types):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        clicked_rect = pygame.Rect(x, y, 1, 1)
                        for i, var_type in enumerate(self.variables):
                            variable_rect = pygame.Rect(self.panel_x + i * 100, self.panel_y + 50, 100, 50)

                            # Si el cursor está sobre el cuadro de tipo de variable y no se está arrastrando uno ya
                            if clicked_rect.colliderect(variable_rect) and dragging_variable is None:
                                dragging_variable = var_type
                                dragging_offset = (x - variable_rect.x, y - variable_rect.y)

                if event.type == pygame.MOUSEMOTION:
                    if dragging_variable is not None:
                        x, y = event.pos
                        
                        # Limita la posición de la caja arrastrada para que no se acerque a menos de 200 píxeles del borde
                        x = max(self.panel_x + 300, min(self.panel_x + self.panel_width - 300, x))
                        y = max(self.panel_y + 150, min(self.panel_y + self.panel_height - 150, y))

                        variable_rect = pygame.Rect(x - dragging_offset[0], y - dragging_offset[1], 100, 50)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if dragging_variable is not None:
                            for i, var_type in enumerate(self.variables):
                                variable_rect = pygame.Rect(self.panel_x + i * 100, self.panel_y + 50, 100, 50)
                                if variable_rect.colliderect(variable_rect):
                                    if var_type == dragging_variable:
                                        self.success += 1
                                        if self.success == len(self.variable_types):
                                            self.end(True)
                                    else:
                                        self.lives -= 1
                                        if self.lives == 0:
                                            self.end(False)
                                dragging_variable = None
                                
            self.pinta_panel()
            
            # Dibuja los tipos de variables en la parte inferior de la pantalla
            var_x = self.panel_x + 200
            for var_type in self.variables:
                var_rect = pygame.Rect(var_x, self.panel_y + self.panel_height - 280, 150, 150)
                self.draw_variable(var_type, var_rect)
                var_x += 140

            # Dibuja los valores en la mitad superior de la pantalla
            val_x = self.panel_x
            val_y = self.panel_y + 50
            for val_type in self.values:
                val_rect = pygame.Rect(val_x, val_y, 100, 50)
                self.draw_value(val_type, val_rect)
                val_x += 100            

            # Renderizar el cuadro de tipo de variable arrastrado
            if dragging_variable is not None:
                dragged_value = self.values[self.variables.index(dragging_variable)]
                pygame.draw.rect(self.game.screen, (255, 0, 0), variable_rect)
                val_text = self.button_font.render(str(dragged_value), True, self.text_color)
                val_text_rect = val_text.get_rect(center=variable_rect.center)
                self.game.screen.blit(val_text, val_text_rect)


            pygame.display.update()


    def end(self, success):
        if success:
            print("¡Has ganado!")
        else:
            print("¡Has perdido!")

        # Limpia la pantalla
        self.game.borra_objects()
        self.waiting = False


if __name__ == "__main__":
    game = Game()
    game.run()
