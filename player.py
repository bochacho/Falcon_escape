import pygame
from lazer import Lazer

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self, canvas_size, health):
        super(Player, self).__init__()
        self.surf = pygame.image.load('Assets/falcon.png').convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                canvas_size[0]/10, 
                canvas_size[1]/2
            )
        )
        self.speed = 5
        self.health = health                    #10
        self.canvas_size = canvas_size

    #sets the starting position of the player
    def set_cent(self,coordinates):
        self.rect.center = coordinates
    
    #Updates the position of the player character with the key pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        #Setting the boundary
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.canvas_size[0]:
            self.rect.right = self.canvas_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.canvas_size[1]:
            self.rect.bottom = self.canvas_size[1]         

    def damage(self, value):
        self.health -= value
        if self.health < 0:
            self.kill()
            return False
        return True
    
    def shoot(self):
        lazer = Lazer(self.canvas_size, self.rect.center, 'blue', -1, 10)
        return lazer