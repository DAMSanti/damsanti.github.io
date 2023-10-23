# game.py
import pygame
import sys
from player import Player
from escritorios import Escritorios
from MiniGame1 import MiniGame1
from MiniGame2 import MiniGame2
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.init_game()

    def init_game(self):
        self.objects = []
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Creamos los objetos de clase player y minijuego1
        self.player = Player(self)
        self.minigame = None
        self.vidas = 3
        self.lives = 3
        
    def borra_objects(self):
        self.objects = []
        
    def update_objects(self):
        for obj in self.objects:
            obj.update(self.background_speed * 2)
            if obj.rect.x < self.player.rect.x + self.player.width / 3:
                self.player.blocked = True
            if not obj.is_on_screen():
                self.objects.remove(obj)
            obj.draw(self.screen)
        # Generar un nuevo objeto si es necesario
        if len(self.objects) == 0:
            self.create_new_object(SCREEN_WIDTH, SCREEN_HEIGHT - 270)
            
    def create_new_object(self, x, y):
        image_path = 'escritorio.png'  # Ruta a la imagen del objeto
        new_object = Escritorios(x, y, image_path)
        self.objects.append(new_object)

    def interactua_object(self):  
        if self.player.pantalla == 0:
            self.minigame = MiniGame1(self, self.player)
        elif self.player.pantalla == 1:
            self.minigame = MiniGame2(self, self.player)
        else:
            self.minigame = None  # Por ejemplo, si no hay pantalla específica

        if self.minigame:
            self.minigame.start() 
            
        # self.minigame = MiniGame1(self)  
        # self.minigame = MiniGame2(self)     
        # self.minigame.start()
        
    def pinta_pantalla(self):
        self.background_x -= self.background_speed
        if self.background_x < -self.background_image.get_width():
            self.background_x = 0
        self.screen.blit(self.background_image, (self.background_x, 0))
        self.screen.blit(self.background_image, (self.background_x + self.background_image.get_width(), 0))
        self.player.control_personaje()
        self.update_objects()
        self.player.draw(self.screen)        
        
    def run(self):
        while not self.game_over:
            self.handle_events()
            self.render_game()
            self.update_game()
            pygame.display.update()
            # self.clock.tick(6)  
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.blocked:
                    self.space_pressed = True  # Marcar la bara espaciadora
                    if self.minigame is None:
                        # Iniciar el minijuego correspondiente
                        self.interactua_object()  # Implementa esta función
                   
    def update_game(self):
        if self.player.blocked and not self.space_pressed:
            font = pygame.font.Font(None, 36)
            text = font.render("Pulsa la barra espaciadora", True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        if self.space_pressed:
            self.space_pressed = False  # Restablecer la variable
            self.interactua_object()  # Abrir Minijuego
                 
    def render_game(self): 
        self.pinta_pantalla()
        self.draw_lives()       
        font = pygame.font.Font(None, 36)
        text = font.render(f"Distancia: {self.max_score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
                       
    def draw_lives(self):
        for i in range(self.lives):
            x = SCREEN_WIDTH - 100 - (i * 70)
            y = 40
            if i < self.vidas:
                heart_image = pygame.image.load("corazon.png").convert_alpha()
            else:
                heart_image = pygame.image.load("corazonvacio.png").convert_alpha()
            heart_image = pygame.transform.scale(heart_image, (60, 60))
            self.screen.blit(heart_image, (x, y))       
            
            

if __name__ == "__main__":
    game = Game()
    game.run()
