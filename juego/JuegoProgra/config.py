# config.py
import pygame

pygame.init()

# Obtén información sobre la pantalla actual
screen_info = pygame.display.Info()
SCREEN_WIDTH = int(screen_info.current_w * 0.9)
SCREEN_HEIGHT = int(screen_info.current_h * 0.9)

# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
