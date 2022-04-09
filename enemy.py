import pygame
from pygame.locals import RLEACCEL
import random
from lazer import Lazer

move_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']
padding = 10


class Enemy(pygame.sprite.Sprite):

    def __init__(self, canvas_size, health, start_place):
        super(Enemy, self).__init__()
        img = pygame.image.load("Assets/Tie.png")
        self.surf = img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                start_place[0],
                start_place[1]
            )
        )
        self.speedX = -2
        self.speedY = 3*random.choice([-1,1])
        self.health = health

    def update_x(self, max_x):
        if (self.rect.right < max_x & self.rect.right > max_x - padding ) or self.rect.left < max_x/2:
            self.speedX = self.speedX*-1
        self.rect.move_ip(self.speedX, 0)

    def update_y(self, max_y):
        if self.rect.bottom > max_y - padding or self.rect.top < padding: 
            self.speedY = self.speedY*-1
        self.rect.move_ip(0, self.speedY)

    def damage(self, value):
        self.health -= value
        if self.health < 1:
            self.kill()
        
    def shoot(self):
        lazer = Lazer(self, self.anvas_size, self.rect.center, 'red', 1, 10)
        return lazer