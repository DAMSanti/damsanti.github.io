# player.py
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Escritorios:
    def __init__(self, x, y, image_path):
        self.width = SCREEN_WIDTH * 0.25
        self.height = SCREEN_HEIGHT * 0.38
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - SCREEN_HEIGHT * 0.38
        
    def update(self, speed):
        self.rect.x -= speed

    def is_on_screen(self):
        return self.rect.right > 0   
             
    def draw(self, screen):
        screen.blit(self.image, self.rect)


