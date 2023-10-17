# player.py
import pygame

class Player:
    def __init__(self, game):
        self.game = game  # Referencia a la instancia de Game
        self.x = self.game.screen_width // 2 - 360 // 2
        self.y = self.game.screen_height - 400 - 10
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

    def control_personaje(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.move_left()
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not self.blocked:
            if self.x < self.game.screen_width // 2 - self.width // 2:
                self.move_right()
            else:
                self.game.background_speed = self.speed
        else:
            self.game.background_speed = 0
            self.stop()

        # Desplazar el fondo horizontalmente
        self.game.background_x -= self.game.background_speed

        # Calcular la puntuación basada en la distancia recorrida
        self.game.score += self.game.background_speed
        if self.game.score > self.game.max_score:
            self.game.max_score = self.game.score

        # Si el fondo se desplaza más allá de su ancho, lo reiniciamos
        if self.game.background_x < -self.game.background_image.get_width():
            self.game.background_x = 0