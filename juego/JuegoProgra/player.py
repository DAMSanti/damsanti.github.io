# player.py
import pygame
from MiniGames import MiniGames
from config import *

class Player:
    def __init__(self, game):
        self.minigame = None
        self.game = game  # Referencia a la instancia de Game
        self.player_x = SCREEN_WIDTH * 0.9 // 2 - SCREEN_WIDTH * 0.3 // 2
        self.background_speed = 0
        self.current_frame = 0
        self.animation_timer = 0
        self.rect = image.get_rect()
        self.rect.x = self.player_x
        self.rect.y = player_y
        self.flipped = False
        self.blocked = False

    def interactua_object(self):  
        if self.minigame is None:
            self.minigame = MiniGames(self.game)
        if self.minigame:
            self.minigame.start(self.game.pantalla) 
            
    def move_left(self):
        if not self.flipped:
            self.flipped = True
        if self.player_x > 0:
            self.player_x -= speed
        else:
            self.player_x = 1
        self.rect.x = self.player_x

    def move_right(self):
        if not self.blocked:
            if self.flipped:
                self.flipped = False
            if self.player_x < SCREEN_WIDTH // 2 - player_width // 2:
                self.player_x += speed
            self.rect.x = self.player_x  # Actualiza la posición X del rectángulo

    def stop(self):
        self.blocked = False

    def draw(self, screen):
        if self.flipped:
            screen.blit(pygame.transform.flip(self.current_animation[self.current_frame], True, False), (self.player_x, player_y + 20))
        else:
            screen.blit(self.current_animation[self.current_frame], (self.player_x, player_y + 20))

    def control_personaje(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.move_left()
            self.current_animation = walk_animation_frames
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not self.blocked:
            if self.player_x < SCREEN_WIDTH // 2 - player_width // 2:
                self.move_right()
                self.current_animation = walk_animation_frames
            else:
                self.background_speed = speed
                self.current_animation = walk_animation_frames
        else:
            self.background_speed = 0
            self.stop()
            self.current_animation = idle_animation_frames
        self.updateAnim()
        self.calculaPuntuacion()
        self.controlaFondo()
        
    def updateAnim(self):        
        # Actualizar la animación
        self.animation_timer += 1
        if self.animation_timer >= frame_change_interval:
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            self.animation_timer = 0
            
    def calculaPuntuacion(self):        
        # Calcular la puntuación BACKGROUND_SPEED en la distancia recorrida
        self.game.score += self.background_speed
        if self.game.score > self.game.max_score:
            self.game.max_score = self.game.score   

    def controlaFondo(self):
        # Desplazar el fondo horizontalmente
        self.game.background_x -= self.background_speed
        # Si el fondo se desplaza más allá de su ancho, lo reiniciamos
        if self.game.background_x < -background_image.get_width():
            self.game.background_x = 0  
