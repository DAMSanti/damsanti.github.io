# game.py
import pygame
import sys
from recursos.player import Player
from recursos.escritorios import Escritorios
from modulos.unidad1.MiniGame1 import MiniGame1
from modulos.unidad1.MiniGame2 import MiniGame2
from modulos.unidad1.MiniGame3 import MiniGame3
from modulos.unidad1.MiniGame4 import MiniGame4
from modulos.unidad1.MiniGame5 import MiniGame5
from modulos.unidad1.MiniGame6 import MiniGame6
from modulos.unidad1.MiniGame7 import MiniGame7
from config import *
sys.path.append('_internal')

class Game:
    def __init__(self):
        pygame.init()
        self.init_game()

    def init_game(self):
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.game_over = False       
        self.score = 0
        self.max_score = 0       
        self.background_x = 0
        self.objects = []
        self.vidas = 3
        self.pantalla = 6 # Modifica la pantallad e inicio
        
    def run(self):
        while not self.game_over:
            self.handle_events()
            self.render_game()
            self.update_game()
            self.clock.tick(60)  
            pygame.display.update()
        pygame.quit()
        sys.exit()
 
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.player.blocked:
                    space_pressed = True
                    self.player.interactua_object()
                    
    def render_game(self): 
        self.pinta_pantalla()
        self.draw_lives()
        
        # Renderizar el texto con sombra
        score_text = digi_font.render(f"Distancia: {self.max_score}", True, (0, 0, 0))  # Sombrero de color
        screen.blit(score_text, (12, 12))
    
        score_text = digi_font.render(f"Distancia: {self.max_score}", True, color_active)
        screen.blit(score_text, (10, 10))
                      
    def update_game(self):
        space_pressed = False
        if self.player.blocked and not space_pressed:
            screen.blit(interactua_text, (SCREEN_WIDTH // 2 - interactua_text.get_width() // 2, SCREEN_HEIGHT // 2 - interactua_text.get_height() // 2))
            
    def pinta_pantalla(self):
        self.background_x -= self.player.background_speed
        if self.background_x < -background_image.get_width():
            self.background_x = 0
            
        screen.blit(background_image, (self.background_x, 0))
        screen.blit(background_image, (self.background_x + background_image.get_width(), 0))
        
        self.player.control_personaje()
        self.update_objects(screen)
        self.player.draw(screen)  

    def draw_lives(self):
        for i in range(max_vidas):
            pos_vidas = [SCREEN_WIDTH - 100 - (i * 70), 40]
            if i < self.vidas:
                heart_image = pygame.image.load(ruta_corazonlleno).convert_alpha()
            else:
                heart_image = pygame.image.load(ruta_corazonvacio).convert_alpha()
            heart_image = pygame.transform.scale(heart_image, (60, 60))
            screen.blit(heart_image, (pos_vidas[0], pos_vidas[1]))   

    def create_new_object(self, x, y):
        new_object = Escritorios(x, y, self.player)
        self.objects.append(new_object)

    def update_objects(self, screen):
        for obj in self.objects:
            obj.update(self.player.background_speed * 2)
            if obj.rect.x < self.player.rect.x + player_width / 2:
                self.player.blocked = True
            if not obj.is_on_screen():
                self.objects.remove(obj)
            obj.draw(screen)
        # Generar un nuevo objeto si es necesario
        if len(self.objects) == 0:
            self.create_new_object(SCREEN_WIDTH*1.5, SCREEN_HEIGHT - 270)
            
    def escogeJuego(self):
        if self.pantalla == 0:
            self.minigame = MiniGame1(self)
        elif self.pantalla == 1:
            self.minigame = MiniGame2(self)
        elif self.pantalla == 2:
            self.minigame = MiniGame3(self)
        elif self.pantalla == 3:
            self.minigame = MiniGame4(self)
        elif self.pantalla == 4:
            self.minigame = MiniGame5(self)
        elif self.pantalla == 5:
            self.minigame = MiniGame6(self)
        elif self.pantalla == 6:
            self.minigame = MiniGame7(self)
        self.minigame.start_game()
                               
    def borra_objects(self):
        self.objects = []

if __name__ == "__main__":
    game = Game()
    game.run()
