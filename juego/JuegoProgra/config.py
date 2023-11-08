# config.py
import pygame
import os
import sys
pygame.init()
pygame.display.set_caption("Juego de Programación en Java")

# Obtén información sobre la pantalla actual
screen_info = pygame.display.Info()
# SCREEN_WIDTH = int(screen_info.current_w * 0.9)
# SCREEN_HEIGHT = int(screen_info.current_h * 0.9)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
# Medidas de los objetos escritorio
ESCRITORIO_WIDTH = SCREEN_WIDTH * 0.45
ESCRITORIO_HEIGHT = SCREEN_HEIGHT * 0.5
"""
# Rutas a imagenes
ruta_fondo = '_internal/imgs/oficina.png'
ruta_escritorios = '_internal/imgs/escritorio1.png'
ruta_idle = '_internal/anim/idle'
ruta_walk = '_internal/anim/run'
ruta_corazonlleno = "_internal/imgs/corazon.png"
ruta_corazonvacio = "_internal/imgs/corazonvacio.png"
ruta_panel = "_internal/imgs/pantalla1.png"    
ruta_numeros = "_internal/imgs/numeros.png"
ruta_cesta = '_internal/imgs/cesta2.png'
tile_pared = pygame.image.load("_internal/imgs/tile.png")
tile_camino = pygame.image.load("_internal/imgs/tile_suelo.png")
tile_entrada = pygame.image.load("_internal/imgs/tile_entrada.png")
tile_salida = pygame.image.load("_internal/imgs/tile_salida.png")
imagen_person = pygame.image.load("_internal/imgs/person.png")

"""
# Rutas a imagenes
ruta_fondo = os.path.join("imgs", "oficina.jpg")
ruta_escritorios = os.path.join("imgs", "escritorio21.png")
ruta_idle = 'anim/idle'
ruta_walk = 'anim/run'
ruta_corazonlleno = os.path.join("imgs", "corazon.png")
ruta_corazonvacio = os.path.join("imgs", "corazonvacio.png")
ruta_panel = os.path.join("imgs", "pantalla1.png") 
ruta_numeros = os.path.join("imgs", "numeros.png")
ruta_cesta = os.path.join("imgs", "cesta2.png")
tile_pared = os.path.join("imgs", "tile.png")
tile_camino = os.path.join("imgs", "tile_suelo.png")
tile_entrada = os.path.join("imgs", "tile_entrada.png")
tile_salida = os.path.join("imgs", "tile_salida.png")
imagen_person = os.path.join("imgs", "person.png")
    
# Variables generales
max_vidas = 3
pantalla = 2 # Modifica la pantallad e inicio
frame_change_interval = 1
speed = int(SCREEN_WIDTH * 0.01)
panel_width = int(SCREEN_WIDTH * 0.8)
panel_height = int(SCREEN_HEIGHT * 0.8)
panel_x = (SCREEN_WIDTH - panel_width) // 2
panel_y = (SCREEN_HEIGHT - panel_height) // 2
play_button_x = (panel_x + panel_width // 2) - (200 // 2)
play_button_y = panel_y + panel_height - SCREEN_HEIGHT * 0.2
click_lock_duration = 0.5   
player_y = SCREEN_HEIGHT * 0.335
player_width = SCREEN_WIDTH * 0.4
player_height = SCREEN_HEIGHT * 0.7
text_color = (255, 255, 255)
panel_image = pygame.image.load(ruta_panel)
hover_color = (0, 160, 0)
clicked_color = (0, 100, 0)
transparent_color = (0, 128, 0, 128)
color_inactive = (200, 220, 220)  
color_active = (47, 252, 2) 
GRID_SIZE = 10
CELL_SIZE = panel_width * 0.3 // GRID_SIZE

# Carga las imágenes con pygame.image.load
tile_pared = pygame.image.load(tile_pared)
tile_camino = pygame.image.load(tile_camino)
tile_entrada = pygame.image.load(tile_entrada)
tile_salida = pygame.image.load(tile_salida)
imagen_person = pygame.image.load(imagen_person)

# Escala las imágenes al tamaño de la celda
tile_pared = pygame.transform.scale(tile_pared, (CELL_SIZE, CELL_SIZE))
tile_camino = pygame.transform.scale(tile_camino, (CELL_SIZE, CELL_SIZE))
tile_entrada = pygame.transform.scale(tile_entrada, (CELL_SIZE, CELL_SIZE))
tile_salida = pygame.transform.scale(tile_salida, (CELL_SIZE, CELL_SIZE))
imagen_person = pygame.transform.scale(imagen_person, (CELL_SIZE, CELL_SIZE))     

fuente="font/LLPIXEL3.ttf"
digi_font = pygame.font.Font(fuente, 36)
game_font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

interactua_text = digi_font.render("Pulsa la barra espaciadora", True, (47, 252, 2))
description_0 = "Minijuego 1: \n\nAsigna los tipos de variables correctos a cada uno de los datos mostrados. \nDeberas introducir el tipo que mas se ajuste en cada caso.\nSi arrastras un valor a un tipo de variable equivocado, perderas una vida."
description_1 = "Minijuego 2: \n\nHaz el cast necesario para obtener el resultado deseado.\n No siempre sera necesario hacer un cast,\npero aun asi debes seleccionar la opcion correcta. \nSi fallas, perderás una vida."
description_2 = "Minijuego 3: \n\nUtiliza los botones en pantalla para navegar por el laberinto.\nEn Java no existe ninguna secuencia de escape que nos devuelva a la linea anterior\npor lo tanto en este minijuego se ha tomado la 'decision artistica'\n de escoger '\ r' como instruccion 'ARRIBA'"
description_3 = "Minijuego 4: \n\nCompleta los problemas con el operador necesario.\nLos operadores utilizados son +, -, *, /, %.\nCada fallo hará que pierdas una vida."
description_4 = "Minijuego 5: \n\nCompleta los problemas con el operador necesario.\nLos operadores utilizados son <, >, >=, <=, ==.\nCada fallo hará que pierdas una vida."
description_5 = "Minijuego 6: \n\nDebes obtener el valor indicado, desde el valor inicial usando unarios.\nRecuerda, los unarios son los operadores x++, x--, --x, ++x.\nPerderás una vida por cada fallo que cometas."

# Definimos la imagen de fondo
escritorio_image = pygame.image.load(ruta_escritorios).convert_alpha()
escritorio_image = pygame.transform.scale(escritorio_image, (ESCRITORIO_WIDTH, ESCRITORIO_HEIGHT))

background_image = pygame.image.load(ruta_fondo)
background_image = pygame.transform.scale(background_image, (4500, SCREEN_HEIGHT))

# Lista de frames de las animaciones
idle_animation_frames = []
walk_animation_frames = []

# Listar todos los archivos en la carpeta
for filename in os.listdir(ruta_idle):
    if filename.endswith('.png'):
        image = pygame.image.load(os.path.join(ruta_idle, filename)).convert_alpha()
        image = pygame.transform.scale(image, (player_width, player_height))
        idle_animation_frames.append(image)

for filename in os.listdir(ruta_walk):
    if filename.endswith('.png'):
        image = pygame.image.load(os.path.join(ruta_walk, filename)).convert_alpha()
        image = pygame.transform.scale(image, (player_width, player_height))
        walk_animation_frames.append(image)   

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