import pygame
import sys
import time

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Juego de Programación en Java")

        self.clock = pygame.time.Clock()
        self.game_over = False

        self.background_x = 0
        self.background_speed = 0
        self.score = 0
        self.max_score = 0

        self.background_image = pygame.image.load('fondo.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.player = Player(self, self.screen_width // 2 - 360 // 2, self.screen_height - 400 - 10)
        self.objects = []
        
        self.space_pressed = False  # Variable para rastrear si la barra espaciadora ha sido presionada


    def update_objects(self):
        for obj in self.objects:
            obj.update(self.background_speed * 2)
            if obj.rect.x < self.player.rect.x + self.player.width / 3:
                self.player.blocked = True
            if not obj.is_on_screen(self.screen_width):
                self.objects.remove(obj)
                
            # Imprime los valores de los rectángulos
            print(f"Rectángulo del jugador: {self.player.rect} {self.player.blocked} {self.space_pressed}")
            print(f"Rectángulo del objeto: {obj.rect}")

            obj.draw(self.screen)

        # Generar un nuevo objeto si es necesario
        if len(self.objects) == 0:
            self.create_new_object(self.screen_width, self.screen_height - 270)
            
            
    def create_new_object(self, x, y):
        image_path = 'escritorio.png'  # Ruta a la imagen del objeto
        new_object = GameObject(x, y, image_path)
        self.objects.append(new_object)
        
    def control_personaje(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not self.player.blocked:
            if self.player.x < self.screen_width // 2 - self.player.width // 2:
                self.player.move_right()
            else:
                character_speed = 10
                self.background_speed = character_speed
        else:
            self.background_speed = 0
            self.player.stop()
            
        # Desplazar el fondo horizontalmente
        self.background_x -= self.background_speed

        # Calcular la puntuación basada en la distancia recorrida hacia la derecha
        self.score += self.background_speed
        if self.score > self.max_score:
            self.max_score = self.score

        # Si el fondo se desplaza más allá de su ancho, lo reiniciamos
        if self.background_x < -self.background_image.get_width():
            self.background_x = 0

    def run(self):
        while not self.game_over:          
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.blocked:
                        print("Barra espaciadora presionada!!")
                        self.space_pressed = True  # Marcar la barra espaciadora como presionada
                          
            pygame.display.update()
            self.background_x -= self.background_speed
        
            if self.background_x < -self.background_image.get_width():
                self.background_x = 0

            self.screen.blit(self.background_image, (self.background_x, 0))
            self.screen.blit(self.background_image, (self.background_x + self.background_image.get_width(), 0))
            self.screen.blit(self.background_image, (self.background_x - self.background_image.get_width(), 0))

           
            self.control_personaje()
            
            
            self.player.draw(self.screen)
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
                self.interactua_object()  # Llamar a la función para eliminar un objeto
                
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def interactua_object(self):
        # Eliminar el objeto más cercano al jugador
        if self.objects:
            closest_object = min(self.objects, key=lambda obj: abs(self.player.rect.centerx - obj.rect.centerx))
            self.objects.remove(closest_object)
            
class Player:
    def __init__(self, game, x, y):
        self.game = game  # Referencia a la instancia de Game
        self.x = x
        self.y = y
        self.width = 360
        self.height = 400
        self.speed = 10
        self.image = pygame.image.load('person.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x  # Asegura que self.rect.x sea igual a self.x
        self.rect.y = self.y
        self.flipped = False
        self.blocked = False

    def move_left(self):
        if not self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = True
        if self.x > 0:
            self.x -= self.speed
        else:
            self.x = 1
        self.rect.x = self.x

    def move_right(self):
        if not self.blocked:
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = False
            if self.x < self.game.screen_width // 2 - self.width // 2:
                self.x += self.speed
            self.rect.x = self.x  # Actualiza la posición X del rectángulo

    def stop(self):
        self.blocked = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y + 20))

class GameObject:
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

if __name__ == "__main__":
    time.sleep(5)
    game = Game()
    game.run()
