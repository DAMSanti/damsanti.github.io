# player.py
import pygame


class Escritorios:
    def __init__(self, x, y, image_path):
        self.width = 500
        self.height = 400
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 150
        
    def update(self, speed):
        self.rect.x -= speed

    def is_on_screen(self, screen_width):
        return self.rect.right > 0   
             
    def draw(self, screen):
        screen.blit(self.image, self.rect)


