import pygame
import random
from pygame.locals import RLEACCEL

class Meteor(pygame.sprite.Sprite):
    def __init__(self, canvas_size):
        super(Meteor, self).__init__()
        rand_size = random.randint(20, 50)
        rand_rotate = random.randint(0,12)*30
        img = pygame.image.load("Assets/meteor.png")
        scaled_img = pygame.transform.scale(img, (rand_size, rand_size))
        rotated_img = pygame.transform.rotate(scaled_img, rand_rotate)

        self.surf = rotated_img.convert_alpha()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(canvas_size[0] + 20 , canvas_size[0] + 100),
                random.randint(0, canvas_size[1])
            )
        )
        self.speed = random.randint(5,15)
        self.health = 3

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
    
    def damage(self, value):
        self.health -= value
        if self.health < 1:
            self.kill()