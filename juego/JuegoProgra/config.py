# config.py
import pygame
import os
pygame.init()

# Obtén información sobre la pantalla actual
screen_info = pygame.display.Info()
# SCREEN_WIDTH = int(screen_info.current_w * 0.9)
# SCREEN_HEIGHT = int(screen_info.current_h * 0.9)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
# Medidas de los objetos escritorio
ESCRITORIO_WIDTH = SCREEN_WIDTH * 0.25
ESCRITORIO_HEIGHT = SCREEN_HEIGHT * 0.38

max_vidas = 3
pantalla = 2 # Modifica la pantallad e inicio
idle_animation_frames = []
walk_animation_frames = []
frame_change_interval = 1
speed = int(SCREEN_WIDTH * 0.006)
panel_width = int(SCREEN_WIDTH * 0.8)
panel_height = int(SCREEN_HEIGHT * 0.8)
panel_x = (SCREEN_WIDTH - panel_width) // 2
panel_y = (SCREEN_HEIGHT - panel_height) // 2
play_button_x = (panel_x + panel_width // 2) - (200 // 2)
play_button_y = panel_y + panel_height - SCREEN_HEIGHT * 0.2
click_lock_duration = 0.5   

variable_types = ["byte", "short", "int", "long", "double", "float", "char"]
values_types = {
            3: "byte",
            27: "byte",
            54: "byte",
            -111: "byte",
            -4: "byte",
            25: "byte",
            19: "byte",
            92: "byte",
            -45: "byte",
            -99: "byte",
            312: "short",
            -1125: "short",
            2563: "short",
            1194: "short",
            -26325: "short",
            14215: "short",
            652: "short",
            -666: "short",
            -30000: "short",
            26854: "short",
            367549: "int",
            652365985: "int",
            '4x10^7': "int",
            '1 millon': "int",
            '9.99x10^8': "int",
            '80000/2': "int",
            555555 : "int",
            696969: "int",
            0.15: "float",
            3/4: "float",
            '3.451x10^2': "float",
            7/5: "float",
            2.287: "float",
            'π': "double",
            '√2': "double",
            'A': "char",
            'J': "char",
            '#': "char",
            '@': "char",
            'i': "char",
            'x': "char"
        }
        
player_y = SCREEN_HEIGHT - SCREEN_HEIGHT * 0.5
player_width = SCREEN_WIDTH * 0.25
player_height = SCREEN_HEIGHT * 0.5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Programación en Java")

game_font = pygame.font.Font(None, 36)

interactua_text = game_font.render("Pulsa la barra espaciadora", True, (255, 255, 255))
description_0 = "Minijuego 1: \n\nAsigna los tipos de variables correctos a cada uno de los datos mostrados. \nDeberas introducir el tipo que mas se ajuste en cada caso."
description_1 = "Minijuego 2: \n\nAsigna los tipos de variables correctos a cada uno de los datos mostrados. \nDeberas introducir el tipo que mas se ajuste en cada caso."
description_2 = "Minijuego 3: \n\nAsigna los tipos de variables correctos a cada uno de los datos mostrados. \nDeberas introducir el tipo que mas se ajuste en cada caso."

text_color = (255, 255, 255)
panel_image = pygame.image.load("pantalla.png")
hover_color = (0, 160, 0)
clicked_color = (0, 100, 0)

# Definimos la imagen de fondo
escritorio_image = pygame.image.load('escritorio.png').convert_alpha()
escritorio_image = pygame.transform.scale(escritorio_image, (ESCRITORIO_WIDTH, ESCRITORIO_HEIGHT))
background_image = pygame.image.load('fondo.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
corazonlleno_image = "corazon.png"
corazonvacio_image = "corazonvacio.png"
# Ruta de la carpeta que contiene las imágenes PNG
folder_path = 'anim/idle'
folder_path_walk = 'anim/run'
# Listar todos los archivos en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        image = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
        image = pygame.transform.scale(image, (player_width, player_height))
        idle_animation_frames.append(image)

for filename in os.listdir(folder_path_walk):
    if filename.endswith('.png'):
        image = pygame.image.load(os.path.join(folder_path_walk, filename)).convert_alpha()
        image = pygame.transform.scale(image, (player_width, player_height))
        walk_animation_frames.append(image)    
        