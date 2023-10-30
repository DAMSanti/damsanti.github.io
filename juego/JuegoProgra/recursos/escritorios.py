# player.py
import pygame
from config import *

class Escritorios:
    def __init__(self, x, y, player):    
        self.player = player
        self.rect = escritorio_image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT * 0.5
        
    def update(self, speed):
        self.rect.x -= speed

    def is_on_screen(self):
        return self.rect.right > 0   
             
    def draw(self, screen):
        screen.blit(escritorio_image, self.rect)
      
